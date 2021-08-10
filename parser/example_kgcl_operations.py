from generate_kgcl_operations import (
    identify_renamings,
    identify_label_creation,
    identify_obsoletions,
    identify_unobsoletions,
    identify_synonym_creation,
    identify_node_moves,
    identify_class_creation,
    identify_predicate_changes,
    identify_edge_creation,
    identify_edge_deletion,
)
import rdflib
from render_operations import render
from get_class_entity import get_class_entity
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


def update_statements(kgclInstances, class_2_statements):
    for k in kgclInstances:
        e = get_class_entity(k)
        if e not in class_2_statements:
            class_2_statements[e] = []
        class_2_statements[e].append(render(k))


def run(identify, class_2_statements, added, deleted):
    kgcl, changeGraph = identify(added, deleted)
    update_statements(kgcl, class_2_statements)
    added = added - changeGraph
    deleted = deleted - changeGraph
    return kgcl


# if __name__ == "__main__":
def generate_diff():
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

    # map from classes to corresponding KGCL statements
    class_2_statements = {}

    renamings, changeGraph = identify_renamings(added, deleted)
    update_statements(renamings, class_2_statements)
    added = added - changeGraph
    deleted = deleted - changeGraph

    obsoletions = run(identify_obsoletions, class_2_statements, added, deleted)
    # obsoletions, changeGraph = identify_obsoletions(added, deleted)
    # update_statements(obsoletions, class_2_statements)
    # added = added - changeGraph
    # deleted = deleted - changeGraph

    unobsoletions, changeGraph = identify_unobsoletions(added, deleted)
    update_statements(unobsoletions, class_2_statements)
    added = added - changeGraph
    deleted = deleted - changeGraph

    labels, changeGraph = identify_label_creation(added, deleted)
    update_statements(labels, class_2_statements)
    added = added - changeGraph
    deleted = deleted - changeGraph

    synonyms, changeGraph = identify_synonym_creation(added, deleted)
    update_statements(synonyms, class_2_statements)
    added = added - changeGraph
    deleted = deleted - changeGraph

    nodeMoves, changeGraph = identify_node_moves(added, deleted)
    update_statements(nodeMoves, class_2_statements)
    added = added - changeGraph
    deleted = deleted - changeGraph

    classCreations, changeGraph = identify_class_creation(added, deleted)
    update_statements(classCreations, class_2_statements)
    added = added - changeGraph
    deleted = deleted - changeGraph

    predicateChanges, changeGraph = identify_predicate_changes(added, deleted)
    update_statements(predicateChanges, class_2_statements)
    added = added - changeGraph
    deleted = deleted - changeGraph

    edgeCreations, changeGraph = identify_edge_creation(added, deleted)
    update_statements(edgeCreations, class_2_statements)
    added = added - changeGraph
    deleted = deleted - changeGraph

    edgeDeletions, changeGraph = identify_edge_deletion(added, deleted)
    update_statements(edgeDeletions, class_2_statements)
    added = added - changeGraph
    deleted = deleted - changeGraph

    # write summary stats
    f = open("stats/summary", "a")
    f.write("Obsoletions: " + str(len(obsoletions)) + "\n")
    f.write("Unobsoletions: " + str(len(unobsoletions)) + "\n")
    f.write("Label Creations: " + str(len(labels)) + "\n")
    f.write("Synonym Creations: " + str(len(synonyms)) + "\n")
    f.write("Node Moves: " + str(len(nodeMoves)) + "\n")
    f.write("Class Creations: " + str(len(classCreations)) + "\n")
    f.write("Predicate Changes: " + str(len(predicateChanges)) + "\n")
    f.write("Edge Creations: " + str(len(edgeCreations)) + "\n")
    f.write("Edge Deletions: " + str(len(edgeDeletions)) + "\n")
    f.close()

    # write KGCL statements
    f = open("stats/all", "a")
    all = []
    id = 0
    for k in class_2_statements:
        id += 1
        ff = open("stats/" + str(id), "a")
        for s in class_2_statements[k]:
            ff.write(s)
            ff.write("\n")
            f.write(s)
            f.write("\n")
        ff.close()
    f.close()
