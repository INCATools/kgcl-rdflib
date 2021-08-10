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
import re


# TODO: this is a rather crude test
def is_id(input):
    return re.match(r"http.*", str(input))


def render_entity(entity):
    if entity is None:
        return ""
    if is_id(entity):
        return "<" + entity + ">"
    else:
        return "'" + entity.replace("'", "") + "'"


def render(kgclInstance):

    if type(kgclInstance) is NodeRename:
        subject = render_entity(kgclInstance.about_node)
        old = render_entity(kgclInstance.old_value)
        new = render_entity(kgclInstance.new_value)
        return "rename " + old + " from " + subject + " to " + new

    if type(kgclInstance) is NodeObsoletion:
        subject = render_entity(kgclInstance.about_node)
        replacement = render_entity(kgclInstance.has_direct_replacement)
        if kgclInstance.has_direct_replacement is not None:
            return "obsolete " + subject + " with replacement " + replacement
        else:
            return "obsolete " + subject

    if type(kgclInstance) is NodeUnobsoletion:
        subject = render_entity(kgclInstance.about_node)
        return "unobsolete " + subject

    if type(kgclInstance) is NodeDeletion:
        subject = render_entity(kgclInstance.about_node)
        return "delete " + subject

    if type(kgclInstance) is NodeMove:
        subject = render_entity(kgclInstance.about_edge.subject)
        new = render_entity(kgclInstance.new_value)
        old = render_entity(kgclInstance.old_value)
        return "move " + subject + " from " + old + " to " + new

    if type(kgclInstance) is EdgeCreation:
        subject = render_entity(kgclInstance.subject)
        predicate = render_entity(kgclInstance.predicate)
        # object = render_entity(kgclInstance.object)
        object = render_entity(repr(kgclInstance.object)[1:-1])
        return "create edge " + predicate + " from " + subject + " to " + object

    if type(kgclInstance) is EdgeDeletion:
        subject = render_entity(kgclInstance.subject)
        predicate = render_entity(kgclInstance.predicate)
        object = render_entity(repr(kgclInstance.object)[1:-1])
        return "delete edge " + predicate + " from " + subject + " to " + object

    if type(kgclInstance) is PredicateChange:
        subject = render_entity(kgclInstance.about_edge.subject)
        object = render_entity(kgclInstance.about_edge.object)
        new = render_entity(kgclInstance.new_value)
        old = render_entity(kgclInstance.old_value)
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
        subject = render_entity(kgclInstance.about_node)
        label = render_entity(kgclInstance.name)
        if label is not None:
            return "create node " + subject + " " + label
        else:
            return "create " + subject

    if type(kgclInstance) is ClassCreation:
        subject = render_entity(kgclInstance.about_node)
        return "create " + subject

    if type(kgclInstance) is NewSynonym:
        subject = render_entity(kgclInstance.about_node)
        synonym = render_entity(kgclInstance.new_value)
        return "create synonym " + synonym + " for " + subject
