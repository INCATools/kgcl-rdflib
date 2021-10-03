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
    PlaceUnder,
    RemoveUnder,
    RemovedNodeFromSubset,
    ExistentialRestrictionCreation,
    ExistentialRestrictionDeletion,
)
from model.ontology_model import Edge
import grammar.parser


# TODO: maintain this dictionary in a file
prefix_2_uri = {
    "obo": "http://purl.obolibrary.org/obo/",
    "ex": "http://example.org/",
    "oboInOwl": "http://www.geneontology.org/formats/oboInOwl#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "swrl": "http://www.w3.org/2003/11/swrl#",
    "oio": "http://www.geneontology.org/formats/oboInOwl#",
    "dce": "http://purl.org/dc/elements/1.1/",
    "dct": "http://purl.org/dc/terms/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "protege": "http://protege.stanford.edu/plugins/owl/protege#",
    "BFO": "http://purl.obolibrary.org/obo/BFO_",
    "CHEBI": "http://purl.obolibrary.org/obo/CHEBI_",
    "CL": "http://purl.obolibrary.org/obo/CL_",
    "IAO": "http://purl.obolibrary.org/obo/IAO_",
    "NCBITaxon": "http://purl.obolibrary.org/obo/NCBITaxon_",
    "OBI": "http://purl.obolibrary.org/obo/OBI_",
    "PR": "http://purl.obolibrary.org/obo/PR_",
    "obo": "http://purl.obolibrary.org/obo/",
    "UP": "http://purl.uniprot.org/uniprot/",
    "UC": "http://purl.uniprot.org/core/",
    "PRO": "http://www.uniprot.org/annotation/PRO_",
    "faldo": "http://biohackathon.org/resource/faldo#",
}


def get_labels(graph):
    """
    Returns a map from IRIs in a graph to (a set of) labels.
    """
    entity_2_label = {}
    for s, p, o in graph.triples((None, RDFS.label, None)):
        ss = str(s)
        os = str(o)
        if "'" not in os:
            if ss not in entity_2_label:
                entity_2_label[ss] = []
            entity_2_label[ss].append(os)

    return entity_2_label


def render_instances(kgcl, graph):
    """
    Takes a KGCL patch for a graph and
    returns a more readable patch
    in which IRI's are replaced by CURIEs and labels where possible.
    """
    labelling = get_labels(graph)

    pretty_print_kgcl = []
    for k in kgcl:
        # print(k)
        kgcl_instance = grammar.parser.parse_statement(k)
        # print(render_instance(kgcl_instance, labelling))  # pretty print
        # render_instance(kgcl_instance, labelling)
        pretty_print_kgcl.append(render_instance(kgcl_instance, labelling))

    return pretty_print_kgcl


def has_label(entity, labelling):
    """
    Returns the label for an entity if it exists
    and the entity itself otherwise.
    """
    if entity in labelling:
        return "'" + labelling[entity][0] + "'"
    else:
        return entity


def curie_entity(entity):
    """
    Returns the CURIE for an entity if it exists
    and the entity itself otherwise.
    """
    for prefix, curie in prefix_2_uri.items():
        if curie in entity:
            return entity.replace(curie, prefix + ":")[1:-1]
    return entity


def render_entity(entity, type, labelling):
    """
    Returns an encoding of the given entity using either
    a CURIE, a label, a literal, or a URI.
    """
    entity = str(entity)
    entity = repr(entity)[1:-1]
    if type == "uri":
        labelling = has_label(entity[1:-1], labelling)
        if entity[1:-1] != labelling:
            return labelling

        curing = curie_entity(entity)
        if entity != curing:
            return curing
        # return "<" + entity + ">"
        return entity

    elif type == "label":
        if "'" not in entity:
            return "'" + entity + "'"

    elif type == "literal":
        if '"' not in entity:
            return '"' + entity + '"'
        elif "'''" not in entity and entity[-1] != "'":
            return "'''" + entity + "'''"
        elif '"""' not in entity and entity[-1] != '"':
            return '"""' + entity + '"""'
        else:
            # return "Error  " + entity
            print("Rendering error: " + entity)
            raise
    else:
        # return "Error  " + entity
        print("Rendering error: " + entity)
        raise


def render_instance(kgclInstance, labelling):
    if type(kgclInstance) is NodeRename:
        # TODO: subject could be 'None'? (not in KGCL Diff)
        # passing an empty labelling because we do not want to repeat labels
        subject = render_entity(kgclInstance.about_node, "uri", {})
        old = kgclInstance.old_value
        new = kgclInstance.new_value

        new_language = kgclInstance.new_language
        old_language = kgclInstance.old_language

        if old_language is not None:
            old = old + "@" + old_language

        if new_language is not None:
            new = new + "@" + new_language

        return "rename " + subject + " from " + old + " to " + new

    if type(kgclInstance) is NodeObsoletion:
        subject = render_entity(kgclInstance.about_node, "uri", labelling)
        replacement = render_entity(
            kgclInstance.has_direct_replacement, "uri", labelling
        )
        if kgclInstance.has_direct_replacement is not None:
            return "obsolete " + subject + " with replacement " + replacement
        else:
            return "obsolete " + subject

    if type(kgclInstance) is NodeUnobsoletion:
        subject = render_entity(kgclInstance.about_node, "uri", labelling)
        return "unobsolete " + subject

    if type(kgclInstance) is NodeDeletion:
        subject = render_entity(kgclInstance.about_node, "uri", labelling)
        return "delete " + subject

    if type(kgclInstance) is NodeMove:
        subject = render_entity(kgclInstance.about_edge.subject, "uri", labelling)
        predicate = render_entity(kgclInstance.about_edge.predicate, "uri", labelling)
        new = render_entity(
            kgclInstance.new_value, kgclInstance.new_object_type, labelling
        )
        old = render_entity(
            kgclInstance.old_value, kgclInstance.old_object_type, labelling
        )

        return (
            "move "
            + subject
            + " "
            + predicate
            + " "
            + old
            + " "
            + "from"
            + " "
            + old
            + " "
            + "to"
            + " "
            + new
        )

    if type(kgclInstance) is EdgeCreation:
        if kgclInstance.annotation_set is None:
            return render_edge_creation(kgclInstance, labelling)
        else:
            return render_annotation_creation(kgclInstance, labelling)

    if type(kgclInstance) is EdgeDeletion:
        if kgclInstance.annotation_set is None:
            return render_edge_deletion(kgclInstance, labelling)
        else:
            return render_annotation_deletion(kgclInstance, labelling)

    if type(kgclInstance) is PredicateChange:
        subject = render_entity(kgclInstance.about_edge.subject, "uri", labelling)
        object = render_entity(
            kgclInstance.about_edge.object,
            kgclInstance.about_edge.object_representation,
            labelling,
        )

        new = render_entity(
            kgclInstance.new_value,
            "uri",
            labelling,
        )
        old = render_entity(kgclInstance.old_value, "uri", labelling)

        if kgclInstance.language is not None:
            object += "@" + kgclInstance.language

        if kgclInstance.datatype is not None:
            object += "^^" + kgclInstance.datatype

        return (
            "change relationship between "
            + subject
            + " and "
            + object
            + " from "
            + old
            + " to "
            + new
        )

    if type(kgclInstance) is NodeCreation:
        subject = render_entity(kgclInstance.about_node, "uri", labelling)
        label = render_entity(kgclInstance.name, "label", labelling)
        if kgclInstance.name is not None:
            return "create node " + subject + " " + label
        else:
            return "create " + subject

    if type(kgclInstance) is ClassCreation:
        subject = render_entity(kgclInstance.node_id, "uri", labelling)
        return "create " + subject

    if type(kgclInstance) is NewSynonym:
        subject = render_entity(kgclInstance.about_node, "uri", labelling)
        synonym = render_entity(kgclInstance.new_value, "label", labelling)
        qualifier = kgclInstance.qualifier
        language = kgclInstance.language

        if language is not None:
            synonym = synonym + "@" + language

        if qualifier is not None:
            return (
                "create " + qualifier + " synonym" + " " + synonym + " for " + subject
            )
        else:
            return "create synonym " + synonym + " for " + subject

    if type(kgclInstance) is ExistentialRestrictionCreation:
        subclass = render_entity(kgclInstance.subclass, "uri", labelling)
        property = render_entity(kgclInstance.property, "uri", labelling)
        filler = render_entity(kgclInstance.filler, "uri", labelling)
        return "add " + subclass + " SubClassOf " + property + " some " + filler

    if type(kgclInstance) is ExistentialRestrictionDeletion:
        subclass = render_entity(kgclInstance.subclass, "uri", labelling)
        property = render_entity(kgclInstance.property, "uri", labelling)
        filler = render_entity(kgclInstance.filler, "uri", labelling)
        return "delete " + subclass + " SubClassOf " + property + " some " + filler

    if type(kgclInstance) is PlaceUnder:
        subclass = render_entity(kgclInstance.subject, "uri", labelling)
        superclass = render_entity(kgclInstance.object, "uri", labelling)
        return "add " + subclass + " SubClassOf " + superclass

    if type(kgclInstance) is RemoveUnder:
        subclass = render_entity(kgclInstance.subject, "uri", labelling)
        superclass = render_entity(kgclInstance.object, "uri", labelling)
        return "delete " + subclass + " SubClassOf " + superclass


def render_annotation_creation(kgclInstance, labelling):
    subject = render_entity(kgclInstance.subject, "uri", labelling)
    predicate = render_entity(kgclInstance.predicate, "uri", labelling)
    object = render_entity(kgclInstance.object, kgclInstance.object_type, labelling)

    annotation = kgclInstance.annotation_set
    annotation_property = render_entity(annotation.property, "uri", labelling)
    annotation_filler = render_entity(
        annotation.filler, annotation.filler_type, labelling
    )

    language = kgclInstance.language
    datatype = kgclInstance.datatype

    if language is not None:
        object = object + "@" + language
    if datatype is not None:
        object = object + "^^" + datatype

    return (
        "create edge <<"
        + subject
        + " "
        + predicate
        + " "
        + object
        + ">>"
        + " "
        + annotation_property
        + " "
        + annotation_filler
    )


def render_annotation_deletion(kgclInstance, labelling):
    subject = render_entity(kgclInstance.subject, "uri", labelling)
    predicate = render_entity(kgclInstance.predicate, "uri", labelling)
    object = render_entity(kgclInstance.object, kgclInstance.object_type, labelling)

    annotation = kgclInstance.annotation_set
    annotation_property = render_entity(annotation.property, "uri", labelling)
    annotation_filler = render_entity(
        annotation.filler, annotation.filler_type, labelling
    )

    language = kgclInstance.language
    datatype = kgclInstance.datatype

    if language is not None:
        object = object + "@" + language
    if datatype is not None:
        object = object + "^^" + datatype

    return (
        "delete edge <<"
        + subject
        + " "
        + predicate
        + " "
        + object
        + ">>"
        + " "
        + annotation_property
        + " "
        + annotation_filler
    )


def render_edge_deletion(kgclInstance, labelling):
    subject = render_entity(kgclInstance.subject, "uri", labelling)
    predicate = render_entity(kgclInstance.predicate, "uri", labelling)
    object = render_entity(kgclInstance.object, kgclInstance.object_type, labelling)

    language = kgclInstance.language
    datatype = kgclInstance.datatype

    base = "delete edge " + subject + " " + predicate + " " + object

    if language is not None:
        return base + "@" + language
    elif datatype is not None:
        return base + "^^" + datatype
    else:
        return base


def render_edge_creation(kgclInstance, labelling):
    subject = render_entity(kgclInstance.subject, "uri", labelling)
    predicate = render_entity(kgclInstance.predicate, "uri", labelling)
    object = render_entity(kgclInstance.object, kgclInstance.object_type, labelling)

    language = kgclInstance.language
    datatype = kgclInstance.datatype

    base = "create edge " + subject + " " + predicate + " " + object

    if language is not None:
        return base + "@" + language
    elif datatype is not None:
        return base + "^^" + datatype
    else:
        return base
