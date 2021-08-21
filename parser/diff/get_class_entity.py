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


def get_class_entity(kgclInstance):

    if type(kgclInstance) is NodeRename:
        subject = kgclInstance.about_node
        return subject

    if type(kgclInstance) is NodeObsoletion:
        subject = kgclInstance.about_node
        return subject

    if type(kgclInstance) is NodeUnobsoletion:
        subject = kgclInstance.about_node
        return subject

    if type(kgclInstance) is NodeDeletion:
        subject = kgclInstance.about_node
        return subject

    if type(kgclInstance) is NodeMove:
        subject = kgclInstance.about_edge.subject
        return subject

    if type(kgclInstance) is EdgeCreation:
        subject = kgclInstance.subject
        return subject

    if type(kgclInstance) is EdgeDeletion:
        subject = kgclInstance.subject
        return subject

    if type(kgclInstance) is PredicateChange:
        subject = kgclInstance.about_edge.subject
        return subject

    if type(kgclInstance) is NodeCreation:
        subject = kgclInstance.about_node
        return subject

    if type(kgclInstance) is ClassCreation:
        subject = kgclInstance.about_node
        return subject

    if type(kgclInstance) is NewSynonym:
        subject = kgclInstance.about_node
        return subject
