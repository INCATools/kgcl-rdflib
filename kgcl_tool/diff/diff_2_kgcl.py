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
from diff.change_detection import (
    detect_renamings,
    detect_node_moves,
    detect_predicate_changes,
)
from diff.render_operations import render


def id_generator():
    id = 0
    while True:
        yield id
        id += 1


id_gen = id_generator()


def generate_kgcl_commands(added, deleted):

    renamings, covered, nonDeterministic = detect_renamings(added, deleted)
    added = added - covered
    deleted = deleted - covered

    edge_creations, covered = generate_edge_creations(added)
    edge_deletions, covered = generate_edge_deletions(deleted)

    kgcl_commands = []
    for r in renamings:
        kgcl_commands.append(render(r))
    for e in edge_creations:
        kgcl_commands.append(render(e))
    for e in edge_deletions:
        kgcl_commands.append(render(e))

    return kgcl_commands


def get_type(rdf_entity):
    if isinstance(rdf_entity, URIRef):
        return "IRI"
    elif isinstance(rdf_entity, Literal):
        return "Literal"
    else:
        return "Error"


def get_language_tag(rdf_entity):
    if isinstance(rdf_entity, Literal):
        return rdf_entity.language
    else:
        return None


def get_datatype(rdf_entity):
    if isinstance(rdf_entity, Literal) and rdf_entity.datatype is not None:
        return str(rdf_entity.datatype)
    else:
        return None


def generate_edge_deletions(deleted):
    covered = rdflib.Graph()
    kgcl = []
    for s, p, o in deleted:

        id = "test_id_" + str(next(id_gen))
        object_type = get_type(o)
        language_tag = get_language_tag(o)
        datatype = get_datatype(o)
        if datatype is not None:
            datatype = "<" + datatype + ">"

        node = EdgeDeletion(
            id=id,
            subject=str(s),
            predicate=str(p),
            object=str(o),
            object_type=object_type,
            language=language_tag,
            datatype=datatype,
        )

        kgcl.append(node)
        covered.add((s, p, o))

    return kgcl, covered


def generate_edge_creations(added):
    covered = rdflib.Graph()

    kgcl = []
    for s, p, o in added:

        id = "test_id_" + str(next(id_gen))
        object_type = get_type(o)
        language_tag = get_language_tag(o)
        datatype = get_datatype(o)
        if datatype is not None:
            datatype = "<" + datatype + ">"  # expect data types without curies

        node = EdgeCreation(
            id=id,
            subject=str(s),
            predicate=str(p),
            object=str(o),
            object_type=str(object_type),
            language=language_tag,
            datatype=datatype,
        )

        kgcl.append(node)
        covered.add((s, p, o))

    return kgcl, covered
