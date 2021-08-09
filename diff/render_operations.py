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


def render(kgclInstance):

    if type(kgclInstance) is NodeRename:
        subject = kgclInstance.about_node
        old = kgclInstance.old_value
        new = kgclInstance.new_value
        return "rename " + subject + " from " + old + " to " + new

    if type(kgclInstance) is NodeObsoletion:
        subject = kgclInstance.about_node
        replacement = kgclInstance.has_direct_replacement
        if replacement is not None:
            return "obsolete " + subject + " with replacement " + replacement
        else:
            return "obsolete " + subject

    if type(kgclInstance) is NodeUnobsoletion:
        subject = kgclInstance.about_node
        return "unobsolete " + subject

    if type(kgclInstance) is NodeDeletion:
        subject = kgclInstance.about_node
        return "delete " + subject

    if type(kgclInstance) is NodeMove:
        subject = kgclInstance.about_edge.subject
        new = kgclInstance.new_value
        old = kgclInstance.old_value
        return "move " + subject + " from " + old + " to " + new

    if type(kgclInstance) is EdgeCreation:
        subject = kgclInstance.subject
        predicate = kgclInstance.predicate
        object = kgclInstance.object
        return "create edge " + predicate + " from " + subject + " to " + object

    if type(kgclInstance) is EdgeDeletion:
        subject = kgclInstance.subject
        predicate = kgclInstance.predicate
        object = kgclInstance.object
        return "delete edge " + predicate + " from " + subject + " to " + object

    if type(kgclInstance) is PredicateChange:
        subject = kgclInstance.about_edge.subject
        new = kgclInstance.new_value
        old = kgclInstance.old_value
        return "change relationship between " + subject + " and " + old + " to " + new

    if type(kgclInstance) is NodeCreation:
        subject = kgclInstance.about_node
        label = kgclInstance.name
        return "create " + subject + " " + label

    if type(kgclInstance) is ClassCreation:
        subject = kgclInstance.about_node
        return "create " + subject

    if type(kgclInstance) is NewSynonym:
        subject = kgclInstance.about_node
        synonym = kgclInstance.new_value
        return "create synonym " + synonym + " for " + subject
