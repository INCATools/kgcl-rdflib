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
        old_token = extract(tree, "old_label")
        new_token = extract(tree, "new_label")
        term_id_token = extract(tree, "id")

        return NodeRename(
            id=id,
            about_node=term_id_token,
            old_value=old_token,
            new_value=new_token,
        )

    if command == "obsolete":
        label_token = extract(tree, "entity")
        replacement_token = extract(tree, "replacement")
        return NodeObsoletion(
            id=id, about_node=label_token, has_direct_replacement=replacement_token
        )

    if command == "unobsolete":
        term_id_token = extract(tree, "id")
        return NodeUnobsoletion(id=id, about_node=term_id_token)

    if command == "delete":
        label_token = extract(tree, "entity")
        return NodeDeletion(id=id, about_node=label_token)

    if command == "move":
        term_id_token = extract(tree, "id")
        old_token = extract(tree, "old_id")
        new_token = extract(tree, "new_id")

        edge = Edge(subject=term_id_token, object=old_token)

        return NodeMove(
            id=id, about_edge=edge, old_value=old_token, new_value=new_token
        )

    if command == "deepen":
        term_id_token = extract(tree, "id")
        old_token = extract(tree, "old_id")
        new_token = extract(tree, "new_id")

        edge = Edge(subject=term_id_token, object=old_token)

        return NodeDeepening(
            id=id, about_edge=edge, old_value=old_token, new_value=new_token
        )

    if command == "shallow":
        term_id_token = extract(tree, "id")
        old_token = extract(tree, "old_id")
        new_token = extract(tree, "new_id")

        edge = Edge(subject=term_id_token, object=old_token)

        return NodeShallowing(
            id=id, about_edge=edge, old_value=old_token, new_value=new_token
        )

    if command == "create_edge":
        subject_token = extract(tree, "subject")
        predicate_token = extract(tree, "predicate")
        object_token = extract(tree, "object")

        return EdgeCreation(
            id=id, subject=subject_token, predicate=predicate_token, object=object_token
        )

    if command == "delete_edge":
        subject_token = extract(tree, "subject")
        predicate_token = extract(tree, "predicate")
        object_token = extract(tree, "object")

        return EdgeDeletion(
            id=id, subject=subject_token, predicate=predicate_token, object=object_token
        )

    if command == "change_relationship":
        subject_token = extract(tree, "subject")
        object_token = extract(tree, "object")

        edge = Edge(subject=subject_token, object=object_token)

        old_token = extract(tree, "old")
        new_token = extract(tree, "new")
        return PredicateChange(
            id=id, about_edge=edge, old_value=old_token, new_value=new_token
        )

    # the KGCL model suggests the command
    # 'create node {id} {label} with {annotation set}'
    # TODO: handling of {annotation set}
    if command == "create":
        term_id_token = extract(tree, "id")
        label_token = extract(tree, "label")
        # TODO: where is the difference between
        # a 'node_id' provided by 'NodeCreation'
        # and 'about_node' inherited by 'NodeChange'?
        return NodeCreation(
            id=id, about_node=term_id_token, node_id=term_id_token, name=label_token
        )

    if command == "create_class":
        term_id_token = extract(tree, "id")
        return ClassCreation(id=id, node_id=term_id_token)

    if command == "create_synonym":
        term_id_token = extract(tree, "id")
        synonym_string_token = extract(tree, "synonym")

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

        term_id_token = extract(tree, "id")
        subset_id_token = extract(tree, "subset")

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


def extract(tree, data):
    node = get_next(tree.find_data(data))
    if node is not None:
        node_token = next(get_tokens(node))
        return node_token
    else:
        return None


def get_tokens(tree):
    return tree.scan_values(lambda v: isinstance(v, Token))


def get_next(generator):
    try:
        res = next(generator)
        return res
    except StopIteration:
        return None


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
