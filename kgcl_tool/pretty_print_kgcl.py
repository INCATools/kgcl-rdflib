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
    labelling = get_labels(graph)

    pretty_print_kgcl = []
    for k in kgcl:
        kgcl_instance = grammar.parser.parse_statement(k)
        # print(render_instance(kgcl_instance, labelling))  # pretty print
        # render_instance(kgcl_instance, labelling)
        pretty_print_kgcl.append(render_instance(kgcl_instance, labelling))

    return pretty_print_kgcl


def label_entity(entity, labelling):
    # check whether there is a label
    if entity in labelling:
        return "'" + labelling[entity][0] + "'"
    else:
        return entity


def curie_entity(entity):
    # check whether an URI can be rewritten into a CURIE
    for prefix, curie in prefix_2_uri.items():
        if curie in entity:
            return entity.replace(curie, prefix + ":")[1:-1]
    return entity


def render_entity(entity, type, labelling):
    entity = str(entity)
    entity = repr(entity)[1:-1]
    if type == "IRI":
        labelling = label_entity(entity[1:-1], labelling)
        if entity[1:-1] != labelling:
            return labelling

        curing = curie_entity(entity)
        if entity != curing:
            return curing
        # return "<" + entity + ">"
        return entity

    elif type == "Label":
        if "'" not in entity:
            return "'" + entity + "'"

    elif type == "Literal":
        if '"' not in entity:
            return '"' + entity + '"'
        elif "'''" not in entity and entity[-1] != "'":
            return "'''" + entity + "'''"
        elif '"""' not in entity and entity[-1] != '"':
            return '"""' + entity + '"""'
        else:
            return "Error  " + entity
            # print("Rendering error: " + entity)
            # raise
    else:
        return "Error  " + entity
    # print("Rendering error: " + entity)
    # raise


# add labels to render_entity


def render_instance(kgclInstance, labelling):
    if type(kgclInstance) is NodeRename:
        # TODO: subject could be 'None'? (not in KGCL Diff)
        subject = render_entity(kgclInstance.about_node, "IRI", labelling)
        # old = render_entity(kgclInstance.old_value, "Label", labelling)
        # new = render_entity(kgclInstance.new_value, "Label", labelling)
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
        subject = render_entity(kgclInstance.about_node, "IRI", labelling)
        # TODO: type this correctly
        replacement = render_entity(
            kgclInstance.has_direct_replacement, "IRI", labelling
        )
        if kgclInstance.has_direct_replacement is not None:
            return "obsolete " + subject + " with replacement " + replacement
        else:
            return "obsolete " + subject

    if type(kgclInstance) is NodeUnobsoletion:
        subject = render_entity(kgclInstance.about_node, "IRI", labelling)
        return "unobsolete " + subject

    if type(kgclInstance) is NodeDeletion:
        subject = render_entity(kgclInstance.about_node, "IRI", labelling)
        return "delete " + subject

    if type(kgclInstance) is NodeMove:
        subject = render_entity(kgclInstance.about_edge.subject, "IRI", labelling)
        predicate = render_entity(kgclInstance.about_edge.predicate, "IRI", labelling)

        if kgclInstance.new_object_type == "literal":
            new = render_entity(kgclInstance.new_value, "Literal", labelling)
        if kgclInstance.new_object_type == "uri":
            new = render_entity(kgclInstance.new_value, "IRI", labelling)
        if kgclInstance.new_object_type == "label":
            new = render_entity(kgclInstance.new_value, "Label", labelling)

        if kgclInstance.old_object_type == "literal":
            old = render_entity(kgclInstance.old_value, "Literal", labelling)
        if kgclInstance.old_object_type == "uri":
            old = render_entity(kgclInstance.old_value, "IRI", labelling)
        if kgclInstance.old_object_type == "label":
            old = render_entity(kgclInstance.old_value, "Label", labelling)

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
        subject = render_entity(kgclInstance.about_edge.subject, "IRI", labelling)

        if kgclInstance.about_edge.object_representation == "literal":
            object = render_entity(kgclInstance.about_edge.object, "Literal", labelling)
        if kgclInstance.about_edge.object_representation == "uri":
            object = render_entity(kgclInstance.about_edge.object, "IRI", labelling)
        if kgclInstance.about_edge.object_representation == "label":
            object = render_entity(kgclInstance.about_edge.object, "Label", labelling)

        new = render_entity(
            kgclInstance.new_value,
            "IRI",
            labelling,
        )
        old = render_entity(kgclInstance.old_value, "IRI", labelling)

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
        subject = render_entity(kgclInstance.about_node, "IRI", labelling)
        label = render_entity(kgclInstance.name, "Label", labelling)
        if kgclInstance.name is not None:
            return "create node " + subject + " " + label
        else:
            return "create " + subject

    if type(kgclInstance) is ClassCreation:
        subject = render_entity(kgclInstance.node_id, "IRI", labelling)
        return "create " + subject

    if type(kgclInstance) is NewSynonym:
        subject = render_entity(kgclInstance.about_node, "IRI", labelling)
        synonym = render_entity(kgclInstance.new_value, "Literal", labelling)
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
        subclass = render_entity(kgclInstance.subclass, "IRI", labelling)
        property = render_entity(kgclInstance.property, "IRI", labelling)
        filler = render_entity(kgclInstance.filler, "IRI", labelling)
        return "add " + subclass + " SubClassOf " + property + " some " + filler

    if type(kgclInstance) is ExistentialRestrictionDeletion:
        subclass = render_entity(kgclInstance.subclass, "IRI", labelling)
        property = render_entity(kgclInstance.property, "IRI", labelling)
        filler = render_entity(kgclInstance.filler, "IRI", labelling)
        return "delete " + subclass + " SubClassOf " + property + " some " + filler

    if type(kgclInstance) is PlaceUnder:
        subclass = render_entity(kgclInstance.subject, "IRI", labelling)
        superclass = render_entity(kgclInstance.object, "IRI", labelling)
        return "add " + subclass + " SubClassOf " + superclass

    if type(kgclInstance) is RemoveUnder:
        subclass = render_entity(kgclInstance.subject, "IRI", labelling)
        superclass = render_entity(kgclInstance.object, "IRI", labelling)
        return "delete " + subclass + " SubClassOf " + superclass


def render_annotation_creation(kgclInstance, labelling):
    subject = render_entity(kgclInstance.subject, "IRI", labelling)
    predicate = render_entity(kgclInstance.predicate, "IRI", labelling)

    if kgclInstance.object_type == "literal":
        object = render_entity(kgclInstance.object, "Literal", labelling)
    if kgclInstance.object_type == "uri":
        object = render_entity(kgclInstance.object, "IRI", labelling)
    if kgclInstance.object_type == "label":
        object = render_entity(kgclInstance.object, "Label", labelling)

    annotation = kgclInstance.annotation_set
    annotation_property = render_entity(annotation.property, "IRI", labelling)
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
    subject = render_entity(kgclInstance.subject, "IRI", labelling)
    predicate = render_entity(kgclInstance.predicate, "IRI", labelling)

    if kgclInstance.object_type == "literal":
        object = render_entity(kgclInstance.object, "Literal", labelling)
    if kgclInstance.object_type == "uri":
        object = render_entity(kgclInstance.object, "IRI", labelling)
    if kgclInstance.object_type == "label":
        object = render_entity(kgclInstance.object, "Label", labelling)

    annotation = kgclInstance.annotation_set
    annotation_property = render_entity(annotation.property, "IRI", labelling)
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
    subject = render_entity(kgclInstance.subject, "IRI", labelling)
    predicate = render_entity(kgclInstance.predicate, "IRI", labelling)

    if kgclInstance.object_type == "literal":
        object = render_entity(kgclInstance.object, "Literal", labelling)
    if kgclInstance.object_type == "uri":
        object = render_entity(kgclInstance.object, "IRI", labelling)
    if kgclInstance.object_type == "label":
        object = render_entity(kgclInstance.object, "Label", labelling)
    # object = render_entity(repr(kgclInstance.object)[1:-1])

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
    subject = render_entity(kgclInstance.subject, "IRI", labelling)
    predicate = render_entity(kgclInstance.predicate, "IRI", labelling)

    if kgclInstance.object_type == "literal":
        object = render_entity(kgclInstance.object, "Literal", labelling)
    if kgclInstance.object_type == "uri":
        object = render_entity(kgclInstance.object, "IRI", labelling)
    if kgclInstance.object_type == "label":
        object = render_entity(kgclInstance.object, "Label", labelling)

    language = kgclInstance.language
    datatype = kgclInstance.datatype

    base = "create edge " + subject + " " + predicate + " " + object

    if language is not None:
        return base + "@" + language
    elif datatype is not None:
        return base + "^^" + datatype
    else:
        return base
