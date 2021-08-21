from lark import Lark, Token
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
from pathlib import Path


def id_generator():
    id = 0
    while True:
        yield id
        id += 1


path = Path(__file__).parent
kgcl_parser = Lark.open(str(path) + "/kgcl.lark", start="expression")
id_gen = id_generator()


# input may be a set of KGCL statements separated by \n
def parse(input):
    statements = input.splitlines()
    parsed = []

    for s in statements:
        parsed.append(parse_statement(s))
        # parsed.append((s,parse_statement(s)))
    return parsed


def parse_statement(input):

    tree = kgcl_parser.parse(input)

    id = "test_id_" + str(next(id_gen))

    command = tree.data
    # print("Command: " + command)

    if command == "rename":
        # node with data 'old_label' is unique
        old = next(tree.find_data("old_label"))
        # and this node only has one token
        old_token = next(get_tokens(old))

        new = next(tree.find_data("new_label"))
        new_token = next(get_tokens(new))

        term_id = tree.find_data("id")

        term_id_list = list(tree.find_data("id"))
        # test whether there is an element in the generator
        if term_id_list:
            t = next(term_id)
            term_id_token = next(get_tokens(t))
            return NodeRename(
                id=id,
                about_node=term_id_token,
                old_value=old_token,
                new_value=new_token,
            )
        else:
            return NodeRename(id=id, old_value=old_token, new_value=new_token)

    if command == "obsolete":
        label = next(tree.find_data("entity"))
        label_token = next(get_tokens(label))

        replacement_id = tree.find_data("replacement")

        replacement_id_list = list(tree.find_data("replacement"))
        if replacement_id_list:
            t = next(replacement_id)
            replace = next(get_tokens(t))
            return NodeObsoletion(
                id=id, about_node=label_token, has_direct_replacement=replace
            )
        else:
            return NodeObsoletion(id=id, about_node=label_token)

    if command == "unobsolete":
        term_id = next(tree.find_data("id"))
        term_id_token = next(get_tokens(term_id))

        return NodeUnobsoletion(id=id, about_node=term_id_token)

    if command == "delete":
        label = next(
            tree.find_data("entity")
        )  # TODO check whether we want to delete nodes by label
        label_token = next(get_tokens(label))

        return NodeDeletion(id=id, about_node=label_token)

    if command == "move":
        term_id = next(tree.find_data("id"))
        term_id_token = next(get_tokens(term_id))

        old = next(tree.find_data("old_id"))
        old_token = next(get_tokens(old))

        new = next(tree.find_data("new_id"))
        new_token = next(get_tokens(new))

        edge = Edge(subject=term_id_token, object=old_token)

        return NodeMove(
            id=id, about_edge=edge, old_value=old_token, new_value=new_token
        )
    if command == "deepen":
        term_id = next(tree.find_data("id"))
        term_id_token = next(get_tokens(term_id))

        old = next(tree.find_data("old_id"))
        old_token = next(get_tokens(old))

        new = next(tree.find_data("new_id"))
        new_token = next(get_tokens(new))

        edge = Edge(subject=term_id_token, object=old_token)

        return NodeDeepening(
            id=id, about_edge=edge, old_value=old_token, new_value=new_token
        )

    if command == "shallow":
        term_id = next(tree.find_data("id"))
        term_id_token = next(get_tokens(term_id))

        old = next(tree.find_data("old_id"))
        old_token = next(get_tokens(old))

        new = next(tree.find_data("new_id"))
        new_token = next(get_tokens(new))

        edge = Edge(subject=term_id_token, object=old_token)

        return NodeShallowing(
            id=id, about_edge=edge, old_value=old_token, new_value=new_token
        )

    if command == "create_edge":
        subject = next(tree.find_data("subject"))
        subject_token = next(get_tokens(subject))

        predicate = next(tree.find_data("predicate"))
        predicate_token = next(get_tokens(predicate))

        object = next(tree.find_data("object"))
        object_token = next(get_tokens(object))

        return EdgeCreation(
            id=id, subject=subject_token, predicate=predicate_token, object=object_token
        )

    if command == "delete_edge":
        subject = next(tree.find_data("subject"))
        subject_token = next(get_tokens(subject))

        predicate = next(tree.find_data("predicate"))
        predicate_token = next(get_tokens(predicate))

        object = next(tree.find_data("object"))
        object_token = next(get_tokens(object))

        return EdgeDeletion(
            id=id, subject=subject_token, predicate=predicate_token, object=object_token
        )

    if command == "change_relationship":
        subject = next(tree.find_data("subject"))
        subject_token = next(get_tokens(subject))

        object = next(tree.find_data("object"))
        object_token = next(get_tokens(object))

        edge = Edge(subject=subject_token, object=object_token)

        old = next(tree.find_data("old"))
        old_token = next(get_tokens(old))

        new = next(tree.find_data("new"))
        new_token = next(get_tokens(new))
        return PredicateChange(
            id=id, about_edge=edge, old_value=old_token, new_value=new_token
        )

    # the KGCL model suggests the command
    # 'create node {id} {label} with {annotation set}'
    # TODO: handling of {annotation set}
    if command == "create":
        term_id = next(tree.find_data("id"))
        term_id_token = next(get_tokens(term_id))

        label = next(tree.find_data("label"))
        label_token = next(get_tokens(label))
        # TODO: where is the difference between
        # a 'node_id' provided by 'NodeCreation'
        # and 'about_node' inherited by 'NodeChange'?
        return NodeCreation(
            id=id, about_node=term_id_token, node_id=term_id_token, name=label_token
        )

    if command == "create_class":
        term_id = next(tree.find_data("id"))
        term_id_token = next(get_tokens(term_id))
        return ClassCreation(id=id, node_id=term_id_token)

    if command == "create_synonym":
        term_id = next(tree.find_data("id"))
        term_id_token = next(get_tokens(term_id))

        # synonym_type = next(tree.find_data('synonym_type'))
        # synonym_type_token = next(get_tokens(synonym_type))

        synonym_string = next(tree.find_data("synonym"))
        synonym_string_token = next(get_tokens(synonym_string))

        return NewSynonym(
            id=id, about_node=term_id_token, new_value=synonym_string_token
        )
    # TODO: does not have a field for subsets
    # if(command == "add_to_subset"):

    #    term_id = next(tree.find_data('id'))
    #    term_id_token = next(get_tokens(term_id))

    #    subset_id = next(tree.find_data('subset'))
    #    subset_id_token = next(get_tokens(subset_id))

    #    return AddNodeToSubset(
    #        id=id, in_subset=subset_id_token, about_node=term_id_token
    #     )

    if command == "remove_from_subset":

        term_id = next(tree.find_data("id"))
        term_id_token = next(get_tokens(term_id))

        subset_id = next(tree.find_data("subset"))
        subset_id_token = next(get_tokens(subset_id))

        return RemovedNodeFromSubset(
            id=id, subset=subset_id_token, about_node=term_id_token
        )

    # TODO: more cases
    # if(command == "merge"):
    # if(command == "add"):
    # if(command == "add_parent"):
    # if(command == "add_annotation"):
    # if(command == "add_synonym"):
    # if(command == "add_axiom"): (in Manchester Syntax?)
    # if(command == "add_class"):
    # if(command == "add_text_definition"):
    # if(command == "merge"):


def get_tokens(tree):
    return tree.scan_values(lambda v: isinstance(v, Token))


if __name__ == "__main__":
    #
    # MANUAL TESTING
    #
    example1 = "renamea 'abnormal ear' to 'abnormal ear morphology'"
    tree = kgcl_parser.parse(example1)
    print(tree)
    old = next(tree.find_data("old_label"))
    print(old)
    old_token = next(get_tokens(old))
    print(old_token)
