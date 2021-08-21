from diff.generate_kgcl_operations import (
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
from diff.render_operations import render
from diff.get_class_entity import get_class_entity
from rdflib import BNode
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


def update_statements(kgclInstances, class_2_statements):
    for k in kgclInstances:
        e = get_class_entity(k)
        if e not in class_2_statements:
            class_2_statements[e] = []
        class_2_statements[e].append(render(k))


def run(identify, class_2_statements, added, deleted):
    kgcl, changeGraph = identify(added, deleted)
    update_statements(kgcl, class_2_statements)
    added -= changeGraph
    deleted -= changeGraph
    return kgcl


# if __name__ == "__main__":
def generate_diff():
    a = rdflib.Graph()
    a.load("diff/tmp/added", format="nt")

    # filter out triples with blank nodes
    added = rdflib.Graph()
    for s, p, o in a.triples((None, None, None)):
        if not isinstance(s, BNode) and not isinstance(o, BNode):
            added.add((s, p, o))

    d = rdflib.Graph()
    d.load("diff/tmp/deleted", format="nt")

    deleted = rdflib.Graph()
    for s, p, o in d.triples((None, None, None)):
        if not isinstance(s, BNode) and not isinstance(o, BNode):
            deleted.add((s, p, o))

    # map from classes to corresponding KGCL statements
    class_2_statements = {}

    obsoletions = run(identify_obsoletions, class_2_statements, added, deleted)
    unobsoletions = run(identify_unobsoletions, class_2_statements, added, deleted)
    renamings = run(identify_renamings, class_2_statements, added, deleted)
    labels = run(identify_label_creation, class_2_statements, added, deleted)
    synonyms = run(identify_synonym_creation, class_2_statements, added, deleted)
    nodeMoves = run(identify_node_moves, class_2_statements, added, deleted)
    classCreations = run(identify_class_creation, class_2_statements, added, deleted)
    predicateChanges = run(
        identify_predicate_changes, class_2_statements, added, deleted
    )
    edgeCreations = run(identify_edge_creation, class_2_statements, added, deleted)
    edgeDeletions = run(identify_edge_deletion, class_2_statements, added, deleted)

    # write summary stats
    f = open("diff/stats/summary", "a")
    f.write("Renamings: " + str(len(renamings)) + "\n")
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
    f = open("diff/stats/all", "a")
    all = []
    id = 0
    for k in class_2_statements:
        id += 1
        ff = open("diff/stats/" + str(id), "a")
        for s in class_2_statements[k]:
            ff.write(s)
            ff.write("\n")
            f.write(s)
            f.write("\n")
        ff.close()
    f.close()
