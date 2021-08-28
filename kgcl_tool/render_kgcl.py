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


def render(kgclInstance):
    render = ""
    if type(kgclInstance) is NodeRename:
        render = (
            render
            + "NodeRename("
            + "ID="
            + kgclInstance.id
            + ", "
            + "About="
            + str(kgclInstance.about_node)
            + ","
            + "Old Value="
            + kgclInstance.old_value
            + ", "
            + "New Value="
            + kgclInstance.new_value
            + ", "
            + "Old Language="
            + str(kgclInstance.old_language)
            + ", "
            + "New Language="
            + str(kgclInstance.new_language)
            + ")"
        )

    if type(kgclInstance) is NodeObsoletion:
        render = (
            render
            + "NodeObsoletion("
            + "ID="
            + kgclInstance.id
            + ", "
            + "Replacement="
            + str(kgclInstance.has_direct_replacement)
            + ", "
            + "About="
            + kgclInstance.about_node
            + ")"
        )

    if type(kgclInstance) is NodeDeletion:
        render = (
            render
            + "NodeDeletion("
            + "ID="
            + kgclInstance.id
            + ", "
            + "About="
            + kgclInstance.about_node
            + ")"
        )

    if type(kgclInstance) is ClassCreation:
        render = (
            render
            + "ClassCreation("
            + "ID="
            + kgclInstance.id
            + ", "
            + "Term_ID"
            + kgclInstance.node_id
            + ")"
        )

    if type(kgclInstance) is NodeCreation:
        render = (
            render
            + "NodeCreation("
            + "ID="
            + kgclInstance.id
            + ", "
            + "Term ID="
            + kgclInstance.node_id
            + ", "
            + "Label="
            + kgclInstance.name
            + ")"
        )

    if type(kgclInstance) is NodeMove:
        render = (
            render
            + "NodeMove("
            + "ID="
            + kgclInstance.id
            + ", "
            + "Old Value="
            + kgclInstance.old_value
            + ", "
            + "New Value="
            + kgclInstance.new_value
            + ")"
        )

    if type(kgclInstance) is NodeUnobsoletion:
        render = (
            render
            + "NodeUnobsoletion("
            + "ID="
            + kgclInstance.id
            + ", "
            + "Term id="
            + kgclInstance.about_node
            + ")"
        )

    if type(kgclInstance) is NodeDeepening:
        render = (
            render
            + "NodeDeepening("
            + "ID="
            + kgclInstance.id
            + ", "
            + "Term ID="
            + kgclInstance.about_edge.subject
            + ", "
            + "Old Value="
            + kgclInstance.old_value
            + ", "
            + "New Value="
            + kgclInstance.new_value
            + ")"
        )

    if type(kgclInstance) is NodeShallowing:
        render = (
            render
            + "NodeShallowing("
            + "ID="
            + kgclInstance.id
            + ", "
            + "Term ID="
            + kgclInstance.about_edge.subject
            + ", "
            + "Old Value="
            + kgclInstance.old_value
            + ", "
            + "New Value="
            + kgclInstance.new_value
            + ")"
        )

    if type(kgclInstance) is EdgeCreation:
        render = (
            render
            + "EdgeCreation("
            + "ID="
            + kgclInstance.id
            + ", "
            + "Subject="
            + kgclInstance.subject
            + ", "
            + "Predicate="
            + kgclInstance.predicate
            + ", "
            + "Object="
            + kgclInstance.object
            + ")"
        )

    if type(kgclInstance) is EdgeDeletion:
        render = (
            render
            + "EdgeDeletion("
            + "ID="
            + kgclInstance.id
            + ", "
            + "Subject="
            + kgclInstance.subject
            + ", "
            + "Predicate="
            + kgclInstance.predicate
            + ", "
            + "Object="
            + kgclInstance.object
            + ")"
        )

    if type(kgclInstance) is NewSynonym:
        render = (
            render
            + "NewSynonym("
            + "ID="
            + kgclInstance.id
            + ", "
            + "About Node="
            + kgclInstance.about_node
            + ", "
            + "Synonym="
            + kgclInstance.new_value
            + ")"
        )

    if type(kgclInstance) is PredicateChange:
        render = (
            render
            + "PredicateChange("
            + "ID="
            + kgclInstance.id
            + ", "
            + "Subject="
            + kgclInstance.about_edge.subject
            + ", "
            + "Subject="
            + kgclInstance.about_edge.object
            + ", "
            + "Old Value="
            + kgclInstance.old_value
            + ", "
            + "New Value"
            + kgclInstance.new_value
            + ")"
        )

    # if(type(kgclInstance) is AddNodeToSubset):
    #    render = render + "AddNodeToSubset(" \
    #            + "ID=" + kgclInstance.id + ", " \
    #            + "Subset=" + kgclInstance.in_subset + ", " \
    #            + "About Node" + kgclInstance.about_node + ")"

    if type(kgclInstance) is RemovedNodeFromSubset:
        render = (
            render
            + "RemovedNodeFromSubset("
            + "ID="
            + kgclInstance.id
            + ", "
            + "Subset="
            + kgclInstance.subset
            + ", "
            + "About Node"
            + kgclInstance.about_node
            + ")"
        )

    return render
