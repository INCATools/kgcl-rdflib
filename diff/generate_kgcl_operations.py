import rdflib
from rdflib.namespace import (
    RDFS,
    RDF,
    OWL,
)
from rdflib import BNode
from kgcl import (
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
from ontology_model import Edge
import time

# 1. load both 'added' and 'deleted' from temp folder
# 2. check for possible transformations wrt each KGCL operation

# done:
# rename, change relationship, obsolete, unobsolete, create synonym
# move, create, create edge, delete edge
# (these all operate on iri's and not blank nodes)

# TODO:
# deepen,shallow (requires reasoning - later)
# delete (more work since we'd need check whether ALL triples with a class have been deleted)


def id_generator():
    id = 0
    while True:
        yield id
        id += 1


id_gen = id_generator()


def identify_edge_deletion(added, deleted):

    # added + deleted are cases of renamings
    diff = deleted - added

    kgcl = []
    for s, p, o in diff:
        id = "test_id_" + str(next(id_gen))

        node = EdgeDeletion(id=id, subject=str(s), predicate=str(p), object=str(o))
        kgcl.append(node)

    return kgcl


def identify_edge_creation(added, deleted):

    # added + deleted are cases of renamings
    diff = added - deleted

    kgcl = []
    for s, p, o in diff:
        id = "test_id_" + str(next(id_gen))

        node = EdgeCreation(id=id, subject=str(s), predicate=str(p), object=str(o))
        kgcl.append(node)

    return kgcl


# TODO: check that ALL triples with a class are deleted from a graph
# def identify_class_deletion(added, deleted):
#     covered = rdflib.Graph()
#
#     added_classes = set()
#     for s, p, o in added.triples((None, RDFS.label, None)):
#         added_classes.add(s)
#
#     deleted_classes = set()
#     for s, p, o in deleted.triples((None, RDFS.label, None)):
#         deleted_classes.add(s)
#
#     # added + deleted are cases of renamings
#     deleted_classes = deleted_classes - added_classes


def identify_label_creation(added, deleted):
    covered = rdflib.Graph()

    added_classes = set()
    for s, p, o in added.triples((None, RDFS.label, None)):
        added_classes.add(s)

    deleted_classes = set()
    for s, p, o in deleted.triples((None, RDFS.label, None)):
        deleted_classes.add(s)

    # added + deleted are cases of renamings
    created_classes = added_classes - deleted_classes

    kgcl = []
    for s, p, o in added.triples((None, RDFS.label, None)):
        if s in created_classes:
            id = "test_id_" + str(next(id_gen))
            covered.add((s, p, o))
            node = NodeCreation(id=id, about_node=str(s), node_id=str(s), name=str(o))
            kgcl.append(node)

    return kgcl, covered


def identify_class_creation(added, deleted):
    covered = rdflib.Graph()

    added_classes = set()
    for s, p, o in added.triples((None, RDF.type, None)):
        added_classes.add(s)

    deleted_classes = set()
    for s, p, o in deleted.triples((None, RDF.type, None)):
        deleted_classes.add(s)

    created_classes = added_classes - deleted_classes

    kgcl = []
    for s, p, o in added.triples((None, RDF.type, None)):
        if s in created_classes:
            id = "test_id_" + str(next(id_gen))
            covered.add((s, p, o))
            node = NodeCreation(id=id, about_node=str(s), node_id=str(s))
            kgcl.append(node)

    return kgcl, covered


def identify_node_moves(added, deleted):
    covered = rdflib.Graph()

    s2p_added = {}
    for s, p, o in added.triples():
        if s not in s2p_added:
            s2p_added[s] = set()
        s2p_added[s].add(o)

    s2p_deleted = {}
    for s, p, o in deleted.triples():
        if s not in s2p_deleted:
            s2p_deleted[s] = set()
        s2p_deleted[s].add(o)

    # identify triples that only differ wrt their object
    s2p_shared = {}
    for s in s2p_added:
        s2p_shared[s] = s2p_added[s] & s2p_deleted[s]

    # get triples
    add_moves = set()
    delete_moves = set()
    for subject in s2p_shared:
        for predicate in s2p_shared[s]:
            for s, p, o in added.triples((subject, predicate, None)):
                add_moves.add((s, p, o))
            for s, p, o in deleted.triples((subject, predicate, None)):
                delete_moves.add((s, p, o))

    kgcl = []
    for s in s2p_shared:
        shared = len(s2p_shared[s])
        for x in range(shared):
            id = "test_id_" + str(next(id_gen))
            new = add_moves.pop()
            old = delete_moves.pop()
            covered.add(new)
            covered.add(old)
            edge = Edge(subject=str(old[0]), object=str(old[2]))
            node = NodeMove(
                id=id, about_edge=edge, old_value=str(old[2]), new_value=str(new[2])
            )
            kgcl.append(node)

    return kgcl, covered


def identify_synonym_creation(added, deleted):
    covered = rdflib.Graph()
    OBOINOWL = rdflib.Namespace("http://www.geneontology.org/formats/oboInOwl#")

    synonyms = {}
    for s, p, o in added.triples((None, OBOINOWL.Synonym, None)):
        synonyms[s] = o
        covered.add((s, p, o))

    kgcl = []
    for subject, synonym in synonyms.items():
        id = "test_id_" + str(next(id_gen))
        node = NewSynonym(id=id, about_node=str(subject), new_value=str(synonym))
        kgcl.append(node)

    return kgcl, covered


def identify_unobsoletions(added, deleted):
    covered = rdflib.Graph()
    # look for subjects that were originally owl:deprecated
    deprecated = []
    OBO = rdflib.Namespace("http://purl.obolibrary.org/obo/")
    OBOINOWL = rdflib.Namespace("http://www.geneontology.org/formats/oboInOwl#")
    for s, p, o in deleted.triples((None, OWL.deprecated, None)):
        deprecated.append(s)

    for d in deprecated:
        for s, p, o in deleted.triples((d, RDFS.label, None)):
            covered.add((s, p, o))
        for s, p, o in deleted.triples((d, OWL.deprecated, None)):
            covered.add((s, p, o))
        for s, p, o in deleted.triples((d, OBO.IAO_0000115, None)):
            covered.add((s, p, o))
        for s, p, o in deleted.triples((d, OBO.IAO_0100001, None)):
            covered.add((s, p, o))
        for s, p, o in deleted.triples((d, OBOINOWL.consider, None)):
            covered.add((s, p, o))

        for s, p, o in added.triples((d, RDFS.label, None)):
            covered.add((s, p, o))
        for s, p, o in added.triples((d, OBO.IAO_0000115, None)):
            covered.add((s, p, o))

    kgcl = []
    for s in deprecated:
        id = "test_id_" + str(next(id_gen))
        node = NodeUnobsoletion(id=id, about_node=str(s))
        kgcl.append(node)

    return kgcl, covered


def identify_obsoletions(added, deleted):
    covered = rdflib.Graph()

    # look for subjects that are owl:deprecated
    deprecated = []
    OBO = rdflib.Namespace("http://purl.obolibrary.org/obo/")
    for s, p, o in added.triples((None, OWL.deprecated, None)):
        deprecated.append(s)

    # need to get label, replaced by, consider
    replacement = {}
    for d in deprecated:
        # collect all removed subclass, equivalnce class axioms
        for s, p, o in deleted.triples((d, RDFS.label, None)):
            covered.add((s, p, o))
        for s, p, o in deleted.triples((d, RDFS.subClassOf, None)):
            covered.add((s, p, o))
        for s, p, o in deleted.triples((d, OWL.equivalentClass, None)):
            covered.add((s, p, o))
        for s, p, o in deleted.triples((None, OWL.equivalentClass, d)):
            covered.add((s, p, o))

        for s, p, o in added.triples((d, OWL.deprecated, None)):
            covered.add((s, p, o))
        for s, p, o in added.triples((d, OBO.IAO_0100001, None)):
            covered.add((s, p, o))
            replacement[s] = o  # assume that each subject has exactly one replacement
        for s, p, o in added.triples((d, RDFS.label, None)):
            covered.add((s, p, o))

    kgcl = []
    for s in deprecated:
        id = "test_id_" + str(next(id_gen))
        if s in replacement:
            replace = replacement[s]
            obsoletion = NodeObsoletion(
                id=id, about_node=str(s), has_direct_replacement=str(replace)
            )
            kgcl.append(obsoletion)
        else:
            obsoletion = NodeObsoletion(id=id, about_node=str(s))
            kgcl.append(obsoletion)

    return kgcl, covered


def identify_predicate_changes(added, deleted):
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
    for s in s_2_os_added:
        if s in s_2_os_deleted:
            added_objects = set(s_2_os_added[s])
            deleted_objects = set(s_2_os_deleted[s])
            # get intersection of relevant objects
            shared_objects = added_objects & deleted_objects

            for i in shared_objects:
                # get corresponding predicates
                added_predicates = set()
                deleted_predicates = set()
                for s, p, o in added.triples((s, None, i)):
                    added_predicates.add(p)
                for s, p, o in deleted.triples((s, None, i)):
                    deleted_predicates.add(p)

                # create KGCL edge object
                edge = Edge(subject=s, object=i)

                # match potential predicate changes
                m = min(len(added_predicates), len(deleted_predicates))
                for x in range(m):
                    id = "test_id_" + str(next(id_gen))
                    old = deleted_predicates.pop()
                    new = added_predicates.pop()

                    # KGCL change object
                    change = PredicateChange(
                        id=id, about_edge=edge, old_value=old, new_value=new
                    )

                    kgcl.append(change)
                    covered.add((s, old, i))
                    covered.add((s, new, i))

    return kgcl, covered


def identify_renamings(added, deleted):
    """Given a diff represented by 'added' and 'deleted' triples,
    return all possible KGCL renaming operations and
    the corresponding triples (as a graph)"""

    covered = rdflib.Graph()

    # get label tripples from diff
    added_labels = {}
    deleted_labels = {}

    for s, p, o in added.triples((None, RDFS.label, None)):
        added_labels[s] = o

    for s, p, o in deleted.triples((None, RDFS.label, None)):
        deleted_labels[s] = o

    # collect renamings
    renamed_subjects = []
    for subject in deleted_labels:
        if subject in added_labels:
            renamed_subjects.append(subject)
            covered.add((subject, RDFS.label, deleted_labels[subject]))
            covered.add((subject, RDFS.label, added_labels[subject]))

    # encode renamings wrt KGCL model
    kgcl = []
    for s in renamed_subjects:
        id = "test_id_" + str(next(id_gen))
        subject = str(s)
        old_label = str(deleted_labels[s])
        new_label = str(added_labels[s])
        node = NodeRename(
            id=id,
            about_node=subject,
            old_value=old_label,
            new_value=new_label,
        )
        kgcl.append(node)

        # print(f"{subject} {old_label} {new_label}")
    return kgcl, covered


if __name__ == "__main__":

    a = rdflib.Graph()
    a.load("tmp/added", format="nt")

    # filter out triples with blank nodes
    added = rdflib.Graph()
    for s, p, o in a.triples((None, None, None)):
        if not isinstance(s, BNode) and not isinstance(o, BNode):
            added.add((s, p, o))

    d = rdflib.Graph()
    d.load("tmp/deleted", format="nt")

    deleted = rdflib.Graph()
    for s, p, o in d.triples((None, None, None)):
        if not isinstance(s, BNode) and not isinstance(o, BNode):
            deleted.add((s, p, o))

    print(len(added))
    print(len(deleted))

    renamings, changeGraph = identify_renamings(added, deleted)
    # print(renamings)
    # predicateChanges, changeGraph = identify_predicate_changes(added, deleted)
    # print(predicateChanges)
    # obsoletions, changeGraph = identify_obsoletions(added, deleted)
    # print(len(obsoletions))
    # synonyms, changeGraph = identify_synonym_creation(added, deleted)
    # print(synonyms)
