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
    PlaceUnder,
    RemoveUnder,
    NewSynonym,
    RemovedNodeFromSubset,
    ExistentialRestrictionCreation,
    ExistentialRestrictionDeletion,
)
from diff.change_detection import (
    detect_renamings,
    detect_node_moves,
    detect_predicate_changes,
)
from diff.owlstar_sublanguage import (
    get_triple_annotations,
    get_bnodes_2_triple_annotations,
)
from diff.graph_diff import (
    get_added_triple_annotations,
    get_deleted_triple_annotations,
    get_added_existentials,
    get_deleted_existentials,
)
from diff.render_operations import render
from model.ontology_model import Edge, Annotation


def id_generator():
    id = 0
    while True:
        yield id
        id += 1


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


def generate_thin_triple_commands(added, deleted):

    # synonyms
    synonym_additions, covered = generate_synonym_creations(added)
    # TODO: extend data model for deleted synonyms
    # synonym_deletions, covered = generate_synonym_deletions(added)

    # deepen [TODO: need some kind of reasoning/querying for this]
    # shallow [TODO: need some kind of reasoning/querying for this]

    # move
    node_moves, covered, nonDeterministic = detect_node_moves(added, deleted)
    added = added - covered
    deleted = deleted - covered

    # change relationship
    relationship_change, covered, nonDeterministic = detect_predicate_changes(
        added, deleted
    )
    added = added - covered
    deleted = deleted - covered

    # renamings
    renamings, covered, nonDeterministic = detect_renamings(added, deleted)
    added = added - covered
    deleted = deleted - covered

    # subsumptions
    subsumption_creations, covered = generate_subsumption_creations(added)
    added = added - covered
    subsumption_deletions, covered = generate_subsumption_deletions(deleted)
    deleted = deleted - covered

    # create node
    node_creations, covered = generate_class_creations(added)
    added = added - covered

    # any remaning edges
    edge_creations, covered = generate_edge_creations(added)
    edge_deletions, covered = generate_edge_deletions(deleted)

    kgcl_commands = []
    for c in node_creations:
        kgcl_commands.append(render(c))
    for m in node_moves:
        kgcl_commands.append(render(m))
    for s in subsumption_creations:
        kgcl_commands.append(render(s))
    for s in subsumption_deletions:
        kgcl_commands.append(render(s))
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


def generate_subsumption_creations(added):
    covered = rdflib.Graph()
    kgcl = []

    for s, p, o in added.triples((None, RDFS.subClassOf, None)):
        id = "test_id_" + str(next(id_gen))
        subclass = str(s)
        superclass = str(o)

        # TODO the hardcoded owl:subClassOf should be part of the data model
        node = PlaceUnder(
            id=id,
            subject=subclass,
            predicate="<http://www.w3.org/2000/01/rdf-schema#subClassOf>",
            object=superclass,
        )

        kgcl.append(node)
        covered.add((s, p, o))

    return kgcl, covered


def generate_subsumption_deletions(deleted):
    covered = rdflib.Graph()
    kgcl = []

    for s, p, o in deleted.triples((None, RDFS.subClassOf, None)):
        id = "test_id_" + str(next(id_gen))
        subclass = str(s)
        superclass = str(o)

        # TODO the hardcoded owl:subClassOf should be part of the data model
        node = RemoveUnder(
            id=id,
            subject=subclass,
            predicate="<http://www.w3.org/2000/01/rdf-schema#subClassOf>",
            object=superclass,
        )

        kgcl.append(node)
        covered.add((s, p, o))

    return kgcl, covered


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


# TODO: identify node creations + labels
def generate_class_creations(added):
    covered = rdflib.Graph()
    kgcl = []

    for s, p, o in added.triples((None, RDF.type, OWL.Class)):
        id = "test_id_" + str(next(id_gen))
        covered.add((s, p, o))
        node = ClassCreation(id=id, about_node=str(s), node_id=str(s))
        kgcl.append(node)

    return kgcl, covered


def generate_synonym_creations(added):
    covered = rdflib.Graph()
    kgcl = []

    # synonym = URIRef("http://www.geneontology.org/formats/oboInOwl#hasSynonym")
    exact_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasExactSynonym"
    )
    narrow_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym"
    )
    broad_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym"
    )
    related_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym"
    )

    # synonyms
    for s, p, o in added:
        id = "test_id_" + str(next(id_gen))
        covered.add((s, p, o))

        language = get_language_tag(o)
        # datatype = get_datatype(o)

        qualifier = ""  # case for hasSynonym
        if p == exact_synonym:
            qualifier = "exact"
        elif p == narrow_synonym:
            qualifier = "narrow"
        elif p == broad_synonym:
            qualifier = "broad"
        elif p == related_synonym:
            qualifier = "related"

        node = NewSynonym(
            id=id,
            about_node=str(s),
            new_value=str(o),
            qualifier=qualifier,
            language=language,
        )

        kgcl.append(node)

    return kgcl, covered


# TODO: extend data model for deleted synonyms
def generate_synonym_deletions(deleted):
    covered = rdflib.Graph()
    kgcl = []

    # synonym = URIRef("http://www.geneontology.org/formats/oboInOwl#hasSynonym")
    exact_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasExactSynonym"
    )
    narrow_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym"
    )
    broad_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym"
    )
    related_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym"
    )

    # synonyms
    for s, p, o in deleted:
        id = "test_id_" + str(next(id_gen))
        covered.add((s, p, o))

        language = get_language_tag(o)
        # datatype = get_datatype(o)

        qualifier = ""  # case for hasSynonym
        if p == exact_synonym:
            qualifier = "exact"
        elif p == narrow_synonym:
            qualifier = "narrow"
        elif p == broad_synonym:
            qualifier = "broad"
        elif p == related_synonym:
            qualifier = "related"

        # TODO: extend data model for deleted synonyms
        node = NewSynonym(
            id=id,
            about_node=str(s),
            new_value=str(o),
            qualifier=qualifier,
            language=language,
        )

        kgcl.append(node)

    return kgcl, covered
