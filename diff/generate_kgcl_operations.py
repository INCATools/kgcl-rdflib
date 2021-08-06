import rdflib
from rdflib.namespace import (
    RDFS,
    RDF,
    OWL,
)
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
# obsolete,  unobsolete, create synonym

# done: rename, change relationship,
# move deepen,shallow

# -delete, create, create edge, delete edge


def id_generator():
    id = 0
    while True:
        yield id
        id += 1


id_gen = id_generator()


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
    added = rdflib.Graph()
    added.load("tmp/added", format="nt")

    deleted = rdflib.Graph()
    deleted.load("tmp/deleted", format="nt")

    renamings, changeGraph = identify_renamings(added, deleted)
    predicateChanges, changeGraph = identify_predicate_changes(added, deleted)
    obsoletions, changeGraph = identify_obsoletions(added, deleted)
    print(obsoletions)

    # print(renamingGraph.serialize(format="n3"))

    # for s, p, o in added:
    # print(s + " " + p + " " + o)
