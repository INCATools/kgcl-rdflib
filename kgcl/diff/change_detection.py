import rdflib
from rdflib.namespace import (
    RDFS,
    RDF,
    OWL,
)
from rdflib import BNode, URIRef, Literal
from model.kgcl import (
    NodeRename,
    NodeObsoletion,
    NodeUnobsoletion,
    NodeDeletion,
    NodeMove,
    NodeDeepening,
    NodeShallowing,
    EdgeCreation,
    EdgeDeletion,
    PredicateChange,
    NodeCreation,
    ClassCreation,
    NewSynonym,
    RemovedNodeFromSubset,
)
from model.ontology_model import Edge
from diff.owlstar_sublanguage import (
    get_bnodes_2_atomic_existentials,
    get_bnodes_2_triple_annotations,
)
import time


def id_generator():
    """
    Returns a new ID for KGCL change operations.
    """
    id = 0
    while True:
        yield id
        id += 1


# initialise ID generator
id_gen = id_generator()

# TODO:
# obsoletion
# unobsoletion


def get_type(rdf_entity):
    if isinstance(rdf_entity, URIRef):
        return "uri"
    elif isinstance(rdf_entity, Literal):
        return "literal"
    else:
        return "Error"


def detect_renamings(added, deleted):
    """Given a diff represented by 'added' and 'deleted' triples,
    return an encoding in terms of
    (i) NodeRename instances,
    (ii) triples involved in (i), and
    (iii) nondeterministic choices.
    """

    covered = rdflib.Graph()

    # get labeling information
    added_labels = {}
    deleted_labels = {}

    for s, p, o in added.triples((None, RDFS.label, None)):
        if s not in added_labels:
            added_labels[s] = set()
        added_labels[s].add(o)

    for s, p, o in deleted.triples((None, RDFS.label, None)):
        if s not in deleted_labels:
            deleted_labels[s] = set()
        deleted_labels[s].add(o)

    # collect renamings
    nonDeterministic = []  # list of non-deterministic choices
    kgcl = []
    for subject in deleted_labels:
        if subject in added_labels:

            moved_from = deleted_labels[subject]
            moved_to = added_labels[subject]

            if len(moved_to) > 1 or len(moved_from) > 1:
                nonDeterministic.append((set(moved_from), set(moved_to)))

            shared = min(len(moved_to), len(moved_from))
            for x in range(shared):
                id = "test_id_" + str(next(id_gen))

                new = moved_to.pop()
                old = moved_from.pop()

                old_label = str(old)
                new_label = str(new)
                # get language tags
                old_language = old.language
                new_language = new.language

                node = NodeRename(
                    id=id,
                    about_node=subject,
                    old_value=old_label,
                    new_value=new_label,
                    old_language=old_language,
                    new_language=new_language,
                )
                kgcl.append(node)

                covered.add((subject, RDFS.label, new))
                covered.add((subject, RDFS.label, old))

    return kgcl, covered, nonDeterministic


def detect_node_moves(added, deleted):
    """Given a diff represented by 'added' and 'deleted' triples,
    return an encoding in terms of
    (i) NodeMove instances,
    (ii) triples involved in (i), and
    (iii) nondeterministic choices.
    """
    covered = rdflib.Graph()

    # map from subject 2 property (in added)
    s2p_added = {}
    for s, p, o in added:
        if s not in s2p_added:
            s2p_added[s] = set()
        s2p_added[s].add(p)

    # map from subject 2 property (in deleted)
    s2p_deleted = {}
    for s, p, o in deleted:
        if s not in s2p_deleted:
            s2p_deleted[s] = set()
        s2p_deleted[s].add(p)

    # identify triples that only differ wrt their object
    s2p_shared = {}
    for s in s2p_added:
        if s in s2p_deleted:
            s2p_shared[s] = s2p_added[s] & s2p_deleted[s]

    kgcl = []  # list of detected KGCL node modes
    nonDeterministic = []  # list of non-deterministic choices
    for subject in s2p_shared:
        for predicate in s2p_shared[subject]:

            # triples with the same subject and predicate
            moved_to = set()
            moved_from = set()
            for s, p, o in added.triples((subject, predicate, None)):
                if isinstance(o, URIRef):  # node move operates only on nodes
                    moved_to.add((s, p, o))
            for s, p, o in deleted.triples((subject, predicate, None)):
                if isinstance(o, URIRef):
                    moved_from.add((s, p, o))

            if len(moved_to) > 1 or len(moved_from) > 1:
                nonDeterministic.append((set(moved_from), set(moved_to)))

            # TODO: impose an order to make this deterministic
            shared = min(len(moved_to), len(moved_from))
            for x in range(shared):
                id = "test_id_" + str(next(id_gen))

                new = moved_to.pop()
                old = moved_from.pop()

                covered.add(new)
                covered.add(old)

                old_subject = str(old[0])
                old_predicate = str(old[1])
                old_object = str(old[2])
                new_object = str(new[2])

                edge = Edge(
                    subject=old_subject, predicate=old_predicate, object=old_object
                )

                # record entity type for KGCL rendering purposes
                old_object_type = get_type(old[2])
                new_object_type = get_type(new[2])

                node = NodeMove(
                    id=id,
                    about_edge=edge,
                    old_value=old_object,
                    new_value=new_object,
                    old_object_type=old_object_type,
                    new_object_type=new_object_type,
                )

                kgcl.append(node)

    return kgcl, covered, nonDeterministic


def detect_predicate_changes(added, deleted):
    """Given a diff represented by 'added' and 'deleted' triples,
    return an encoding in terms of
    (i) PredicateChange instances,
    (ii) triples involved in (i), and
    (iii) nondeterministic choices.
    """
    covered = rdflib.Graph()

    # maps from subjects to lists of objects
    s_2_os_deleted = {}
    s_2_os_added = {}

    for s, p, o in added:
        if s not in s_2_os_added:
            s_2_os_added[s] = []
        s_2_os_added[s].append(o)

    for s, p, o in deleted:
        if s not in s_2_os_deleted:
            s_2_os_deleted[s] = []
        s_2_os_deleted[s].append(o)

    # encode renamings wrt KGCL model
    kgcl = []
    nonDeterministic = []  # list of non-deterministic choices
    for s in s_2_os_added:
        if s in s_2_os_deleted:

            # get the objects as sets
            added_objects = set(s_2_os_added[s])
            deleted_objects = set(s_2_os_deleted[s])

            # get intersection of relevant objects
            shared_objects = added_objects & deleted_objects

            for i in shared_objects:
                # get corresponding predicates
                changed_to = set()
                changed_from = set()
                for s, p, o in added.triples((s, None, i)):
                    changed_to.add((s, p, o))
                for s, p, o in deleted.triples((s, None, i)):
                    changed_from.add((s, p, o))

                # create KGCL edge object
                edge = Edge(subject=str(s), object=str(i))

                language = None
                datatype = None
                if isinstance(i, Literal):
                    language = i.language
                    datatype = i.datatype
                    if datatype is not None:
                        datatype = (
                            "<" + datatype + ">"
                        )  # expect data types without curies

                # if i.language is not None:
                #    language = str(i.language)
                # else:
                #    language = None
                # if i.datatype is not None:
                #    datatype = str(i.datatype)
                # else:
                #    datatype = None

                object_type = get_type(i)

                if len(changed_to) > 1 or len(changed_from) > 1:
                    nonDeterministic.append((set(changed_from), set(changed_to)))

                # match potential predicate changes
                m = min(len(changed_to), len(changed_from))
                for x in range(m):
                    id = "test_id_" + str(next(id_gen))
                    old = (changed_from.pop())[1]
                    new = (changed_to.pop())[1]

                    # KGCL change object
                    change = PredicateChange(
                        id=id,
                        about_edge=edge,
                        old_value=str(old),
                        new_value=str(new),
                        object_type=object_type,
                        language=language,
                        datatype=datatype,
                    )

                    kgcl.append(change)
                    covered.add((s, old, i))
                    covered.add((s, new, i))

    return kgcl, covered, nonDeterministic
