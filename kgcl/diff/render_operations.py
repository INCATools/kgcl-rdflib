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
import re


def render_entity(entity, rdf_type):
    entity = repr(entity)[1:-1]
    if rdf_type == "uri":
        return "<" + entity + ">"
    elif rdf_type == "label":
        if "'" in entity:
            # TODO: replacing quotes with backticks
            # is only a temporary workaround
            entity = entity.replace("'", "`")
        return "'" + entity + "'"
    elif rdf_type == "literal":
        # TODO: test this
        if '"' not in entity:
            return '"' + entity + '"'
        elif "'''" not in entity and entity[-1] != "'":
            return "'''" + entity + "'''"
        elif '"""' not in entity and entity[-1] != '"':
            return '"""' + entity + '"""'
        else:
            print("Rendering error: " + entity)
            raise
    else:
        print("Rendering error: " + entity)
        raise
    # return "'" + entity.replace("\\'", "`") + "'"


def render(kgclInstance):

    if type(kgclInstance) is NodeRename:
        # TODO: subject could be 'None'?
        subject = render_entity(kgclInstance.about_node, "uri")
        old = render_entity(kgclInstance.old_value, "label")
        new = render_entity(kgclInstance.new_value, "label")

        new_language = kgclInstance.new_language
        old_language = kgclInstance.old_language

        if old_language is not None:
            old = old + "@" + old_language

        if new_language is not None:
            new = new + "@" + new_language

        return "rename " + subject + " from " + old + " to " + new

    if type(kgclInstance) is NodeObsoletion:
        subject = render_entity(kgclInstance.about_node, "uri")
        # TODO: type this correctly
        replacement = render_entity(kgclInstance.has_direct_replacement, "uri")
        if kgclInstance.has_direct_replacement is not None:
            return "obsolete " + subject + " with replacement " + replacement
        else:
            return "obsolete " + subject

    if type(kgclInstance) is NodeUnobsoletion:
        subject = render_entity(kgclInstance.about_node, "uri")
        return "unobsolete " + subject

    if type(kgclInstance) is NodeDeletion:
        subject = render_entity(kgclInstance.about_node, "uri")
        return "delete " + subject

    if type(kgclInstance) is NodeMove:
        subject = render_entity(kgclInstance.about_edge.subject, "uri")
        predicate = render_entity(kgclInstance.about_edge.predicate, "uri")
        new = render_entity(kgclInstance.new_value, kgclInstance.new_object_type)
        old = render_entity(kgclInstance.old_value, kgclInstance.old_object_type)
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
            return render_edge_creation(kgclInstance)
        else:
            return render_annotation_creation(kgclInstance)

    if type(kgclInstance) is EdgeDeletion:
        if kgclInstance.annotation_set is None:
            return render_edge_deletion(kgclInstance)
        else:
            return render_annotation_deletion(kgclInstance)

    if type(kgclInstance) is PredicateChange:
        subject = render_entity(kgclInstance.about_edge.subject, "uri")
        object = render_entity(kgclInstance.about_edge.object, kgclInstance.object_type)
        new = render_entity(kgclInstance.new_value, "uri")
        old = render_entity(kgclInstance.old_value, "uri")

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
        subject = render_entity(kgclInstance.about_node, "uri")
        label = render_entity(kgclInstance.name, "label")
        if kgclInstance.name is not None:
            return "create node " + subject + " " + label
        else:
            return "create " + subject

    if type(kgclInstance) is ClassCreation:
        subject = render_entity(kgclInstance.about_node, "uri")
        return "create " + subject

    if type(kgclInstance) is NewSynonym:
        subject = render_entity(kgclInstance.about_node, "uri")
        synonym = render_entity(kgclInstance.new_value, "label")
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
        subclass = render_entity(kgclInstance.subclass, "uri")
        property = render_entity(kgclInstance.property, "uri")
        filler = render_entity(kgclInstance.filler, "uri")
        return "add " + subclass + " SubClassOf " + property + " some " + filler

    if type(kgclInstance) is ExistentialRestrictionDeletion:
        subclass = render_entity(kgclInstance.subclass, "uri")
        property = render_entity(kgclInstance.property, "uri")
        filler = render_entity(kgclInstance.filler, "uri")
        return "delete " + subclass + " SubClassOf " + property + " some " + filler

    if type(kgclInstance) is PlaceUnder:
        subclass = render_entity(kgclInstance.subject, "uri")
        superclass = render_entity(kgclInstance.object, "uri")
        return "add " + subclass + " SubClassOf " + superclass

    if type(kgclInstance) is RemoveUnder:
        subclass = render_entity(kgclInstance.subject, "uri")
        superclass = render_entity(kgclInstance.object, "uri")
        return "delete " + subclass + " SubClassOf " + superclass


def render_annotation_creation(kgclInstance):
    subject = render_entity(kgclInstance.subject, "uri")
    predicate = render_entity(kgclInstance.predicate, "uri")
    object = render_entity(kgclInstance.object, kgclInstance.object_type)

    annotation = kgclInstance.annotation_set
    annotation_property = render_entity(annotation.property, "uri")
    annotation_filler = render_entity(annotation.filler, annotation.filler_type)

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


def render_annotation_deletion(kgclInstance):
    subject = render_entity(kgclInstance.subject, "uri")
    predicate = render_entity(kgclInstance.predicate, "uri")
    object = render_entity(kgclInstance.object, kgclInstance.object_type)

    annotation = kgclInstance.annotation_set
    annotation_property = render_entity(annotation.property, "uri")
    annotation_filler = render_entity(annotation.filler, annotation.filler_type)

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


def render_edge_deletion(kgclInstance):
    subject = render_entity(kgclInstance.subject, "uri")
    predicate = render_entity(kgclInstance.predicate, "uri")
    object = render_entity(kgclInstance.object, kgclInstance.object_type)
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


def render_edge_creation(kgclInstance):
    subject = render_entity(kgclInstance.subject, "uri")
    predicate = render_entity(kgclInstance.predicate, "uri")
    object = render_entity(kgclInstance.object, kgclInstance.object_type)

    language = kgclInstance.language
    datatype = kgclInstance.datatype

    base = "create edge " + subject + " " + predicate + " " + object

    if language is not None:
        return base + "@" + language
    elif datatype is not None:
        return base + "^^" + datatype
    else:
        return base
