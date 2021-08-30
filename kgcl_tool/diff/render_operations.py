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
import re


def render_entity(entity, rdf_type):
    entity = repr(entity)[1:-1]
    if rdf_type == "IRI":
        return "<" + entity + ">"
    elif rdf_type == "Literal":
        # TODO: test this
        if "'" not in entity:
            return "'" + entity + "'"
        elif '"' not in entity:
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
        subject = render_entity(kgclInstance.about_node)
        old = render_entity(kgclInstance.old_value, "Literal")
        new = render_entity(kgclInstance.new_value, "Literal")
        return "rename " + old + " from " + subject + " to " + new

    if type(kgclInstance) is NodeObsoletion:
        subject = render_entity(kgclInstance.about_node, "IRI")
        # TODO: type this correctly
        replacement = render_entity(kgclInstance.has_direct_replacement, "IRI")
        if kgclInstance.has_direct_replacement is not None:
            return "obsolete " + subject + " with replacement " + replacement
        else:
            return "obsolete " + subject

    if type(kgclInstance) is NodeUnobsoletion:
        subject = render_entity(kgclInstance.about_node, "IRI")
        return "unobsolete " + subject

    if type(kgclInstance) is NodeDeletion:
        subject = render_entity(kgclInstance.about_node, "IRI")
        return "delete " + subject

    if type(kgclInstance) is NodeMove:
        subject = render_entity(kgclInstance.about_edge.subject, "IRI")
        new = render_entity(kgclInstance.new_value, kgclInstance.new_object_type)
        old = render_entity(kgclInstance.old_value, kgclInstance.old_object_type)
        return "move " + subject + " from " + old + " to " + new

    if type(kgclInstance) is EdgeCreation:
        subject = render_entity(kgclInstance.subject, "IRI")
        predicate = render_entity(kgclInstance.predicate, "IRI")
        object = render_entity(kgclInstance.object, kgclInstance.object_type)
        # object = render_entity(repr(kgclInstance.object)[1:-1])
        return "create edge " + subject + " " + predicate + " " + object

    if type(kgclInstance) is EdgeDeletion:
        subject = render_entity(kgclInstance.subject, "IRI")
        predicate = render_entity(kgclInstance.predicate, "IRI")
        object = render_entity(kgclInstance.object, kgclInstance.object_type)
        # object = render_entity(repr(kgclInstance.object)[1:-1])
        return "delete edge " + subject + " " + predicate + " " + object

    if type(kgclInstance) is PredicateChange:
        subject = render_entity(kgclInstance.about_edge.subject, "IRI")
        object = render_entity(kgclInstance.about_edge.object, kgclInstance.object_type)
        new = render_entity(kgclInstance.new_value, "IRI")
        old = render_entity(kgclInstance.old_value, "IRI")
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
        subject = render_entity(kgclInstance.about_node, "IRI")
        label = render_entity(kgclInstance.name, "Literal")
        if kgclInstance.name is not None:
            return "create node " + subject + " " + label
        else:
            return "create " + subject

    if type(kgclInstance) is ClassCreation:
        subject = render_entity(kgclInstance.about_node, "IRI")
        return "create " + subject

    if type(kgclInstance) is NewSynonym:
        subject = render_entity(kgclInstance.about_node, "IRI")
        synonym = render_entity(kgclInstance.new_value, "Literal")
        return "create synonym " + synonym + " for " + subject
