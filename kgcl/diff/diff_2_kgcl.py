import rdflib
from rdflib import URIRef, Literal
from kgcl.model.kgcl import (
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
    PlaceUnder,
    RemoveUnder,
    NewSynonym,
    RemovedNodeFromSubset,
    ExistentialRestrictionCreation,
    ExistentialRestrictionDeletion,
)
from kgcl.diff.graph_diff import (
    get_added_triple_annotations,
    get_deleted_triple_annotations,
    get_added_existentials,
    get_deleted_existentials,
)
from kgcl.diff.render_operations import render
from kgcl.model.ontology_model import Annotation


def id_generator():
    id = 0
    while True:
        yield id
        id += 1


# TODO: refactor this


id_gen = id_generator()

# def generate_obsoletion_commands(g1, g2):
# def generate_unobsoletion_commands(g1, g2):


def generate_atomic_existential_commands(g1, g2):
    added = get_added_existentials(g1, g2)
    deleted = get_deleted_existentials(g1, g2)

    existential_additions, covered = generate_existential_additions(added)
    existential_deletions, covered = generate_existential_deletions(deleted)

    kgcl_commands = []
    for a in existential_additions:
        kgcl_commands.append(render(a))
    for d in existential_deletions:
        kgcl_commands.append(render(d))

    return kgcl_commands


def generate_triple_annotation_commands(g1, g2):
    added = get_added_triple_annotations(g1, g2)
    deleted = get_deleted_triple_annotations(g1, g2)

    annotation_additions, covered = generate_triple_annotation_additions(added)
    annotation_deletions, covered = generate_triple_annotation_deletions(deleted)

    kgcl_commands = []
    for a in annotation_additions:
        kgcl_commands.append(render(a))
    for d in annotation_deletions:
        kgcl_commands.append(render(d))

    return kgcl_commands


def get_type(rdf_entity):
    if isinstance(rdf_entity, URIRef):
        return "uri"
    elif isinstance(rdf_entity, Literal):
        return "literal"
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


def generate_existential_deletions(deleted):
    covered = rdflib.Graph()
    kgcl = []

    for a in deleted:
        subclass = str(a.subclass)
        property = str(a.property)
        filler = str(a.filler)

        id = "test_id_" + str(next(id_gen))

        node = ExistentialRestrictionDeletion(
            id=id, subclass=subclass, property=property, filler=filler
        )

        kgcl.append(node)
        for t in a.triples:
            covered.add(t)

    return kgcl, covered


def generate_existential_additions(added):
    covered = rdflib.Graph()
    kgcl = []

    for a in added:
        subclass = str(a.subclass)
        property = str(a.property)
        filler = str(a.filler)

        id = "test_id_" + str(next(id_gen))

        node = ExistentialRestrictionCreation(
            id=id, subclass=subclass, property=property, filler=filler
        )

        kgcl.append(node)
        for t in a.triples:
            covered.add(t)

    return kgcl, covered


def generate_triple_annotation_additions(added):
    covered = rdflib.Graph()
    kgcl = []

    for a in added:
        source = str(a.source)
        property = str(a.property)
        target = str(a.target)
        target_type = get_type(a.target)
        annotation_property = str(a.annotation_property)
        annotation = str(a.annotation)
        annotation_type = get_type(a.annotation)

        id = "test_id_" + str(next(id_gen))

        language = get_language_tag(a.target)
        datatype = get_datatype(a.target)

        annotation = Annotation(
            property=annotation_property, filler=annotation, filler_type=annotation_type
        )

        node = EdgeCreation(
            id=id,
            subject=source,
            predicate=property,
            object=target,
            object_type=target_type,
            annotation_set=annotation,
            language=language,
            datatype=datatype,
        )

        kgcl.append(node)
        for t in a.triples:
            covered.add(t)

    return kgcl, covered


def generate_triple_annotation_deletions(deleted):
    covered = rdflib.Graph()
    kgcl = []

    for a in deleted:
        source = str(a.source)
        property = str(a.property)
        target = str(a.target)
        target_type = get_type(a.target)
        annotation_property = str(a.annotation_property)
        annotation = str(a.annotation)
        annotation_type = get_type(a.annotation)

        id = "test_id_" + str(next(id_gen))

        language = get_language_tag(a.target)
        datatype = get_datatype(a.target)

        annotation = Annotation(
            property=annotation_property, filler=annotation, filler_type=annotation_type
        )

        node = EdgeDeletion(
            id=id,
            subject=source,
            predicate=property,
            object=target,
            object_type=target_type,
            annotation_set=annotation,
            language=language,
            datatype=datatype,
        )

        kgcl.append(node)
        for t in a.triples:
            covered.add(t)

    return kgcl, covered
