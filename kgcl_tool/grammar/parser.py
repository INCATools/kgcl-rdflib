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
    PlaceUnder,
    RemoveUnder,
    ExistentialRestrictionCreation,
    ExistentialRestrictionDeletion,
)
from model.ontology_model import Edge, Annotation
from pathlib import Path


def id_generator():
    id = 0
    while True:
        yield id
        id += 1


path = Path(__file__).parent
kgcl_parser = Lark.open(str(path) + "/kgcl.lark", start="expression")
id_gen = id_generator()


# multiple KGCL input statements are expected to be separated by \n
def parse(input):
    statements = input.splitlines()
    parsed = []

    for s in statements:
        parsed.append(parse_statement(s))
    return parsed


def parse_statement(input):

    tree = kgcl_parser.parse(input)
    id = "kgcl_change_id_" + str(next(id_gen))

    command = tree.data

    if command == "rename":
        return parse_rename(tree, id)
    elif command == "obsolete":
        return parse_obsolete(tree, id)
    elif command == "unobsolete":
        return parse_unobsolete(tree, id)
    elif command == "delete":
        return parse_delete(tree, id)
    elif command == "move":
        return parse_move(tree, id)
    elif command == "deepen":
        return parse_deepen(tree, id)
    elif command == "shallow":
        return parse_shallow(tree, id)
    elif command == "create_edge":
        return parse_create_edge(tree, id)
    elif command == "delete_edge":
        return parse_delete_edge(tree, id)
    elif command == "create_annotated_edge":
        return parse_create_annotated_edge(tree, id)
    elif command == "delete_annotated_edge":
        return parse_delete_annotated_edge(tree, id)
    elif command == "change_relationship":
        return parse_change_relationship(tree, id)
    elif command == "create":
        return parse_create(tree, id)
    elif command == "create_class":
        return parse_create_class(tree, id)
    elif command == "create_synonym":
        return parse_create_synonym(tree, id)
    elif command == "add_subsumption_axiom":
        return parse_add_subsumption_axiom(tree, id)
    elif command == "delete_subsumption_axiom":
        return parse_delete_subsumption_axiom(tree, id)
    elif command == "add_existential_restriction_axiom":
        return parse_add_existential_restriction_axiom(tree, id)
    elif command == "delete_existential_restriction_axiom":
        return parse_delete_existential_restriction_axiom(tree, id)
    elif command == "remove_from_subset":
        return parse_remove_from_subset(tree, id)
    else:
        raise NotImplementedError("No implementation for KGCL command: " + command)

    # TODO: does not have a field for subsets
    # if(command == "add_to_subset"):

    #    term_id = next(tree.find_data('id'))
    #    term_id_token = next(get_tokens(term_id))

    #    subset_id = next(tree.find_data('subset'))
    #    subset_id_token = next(get_tokens(subset_id))

    #    return AddNodeToSubset(
    #        id=id, in_subset=subset_id_token, about_node=term_id_token
    #     )

    # TODO: more commands
    # if(command == "merge"):
    # if(command == "add"):
    # if(command == "add_parent"):
    # if(command == "add_annotation"):
    # if(command == "add_axiom"): (in Manchester Syntax?)
    # if(command == "add_class"):
    # if(command == "add_text_definition"):
    # if(command == "merge"):


def parse_remove_from_subset(tree, id):
    term_id_token = extract(tree, "id")
    subset_id_token = extract(tree, "subset")

    return RemovedNodeFromSubset(
        id=id, subset=subset_id_token, about_node=term_id_token
    )


def parse_delete_existential_restriction_axiom(tree, id):
    subclass_token = extract(tree, "subclass")
    property_token = extract(tree, "property")
    filler_token = extract(tree, "filler")

    return ExistentialRestrictionDeletion(
        id=id,
        subclass=subclass_token,
        property=property_token,
        filler=filler_token,
    )


def parse_add_existential_restriction_axiom(tree, id):
    subclass_token = extract(tree, "subclass")
    property_token = extract(tree, "property")
    filler_token = extract(tree, "filler")

    return ExistentialRestrictionCreation(
        id=id,
        subclass=subclass_token,
        property=property_token,
        filler=filler_token,
    )


def parse_delete_subsumption_axiom(tree, id):
    subclass_token = extract(tree, "subclass")
    superclass_token = extract(tree, "superclass")

    return RemoveUnder(
        id=id,
        subject=subclass_token,
        predicate="<http://www.w3.org/2000/01/rdf-schema#subClassOf>",
        object=superclass_token,
    )


def parse_add_subsumption_axiom(tree, id):
    subclass_token = extract(tree, "subclass")
    superclass_token = extract(tree, "superclass")

    return PlaceUnder(
        id=id,
        subject=subclass_token,
        predicate="<http://www.w3.org/2000/01/rdf-schema#subClassOf>",
        object=superclass_token,
    )


def parse_create_synonym(tree, id):
    term_id_token = extract(tree, "id")
    synonym_string_token = extract(tree, "synonym")
    language_token = extract(tree, "language")
    qualifier_token = extract(tree, "synonym_qualifier")

    return NewSynonym(
        id=id,
        about_node=term_id_token,
        new_value=synonym_string_token,
        qualifier=qualifier_token,
        language=language_token,
    )


def parse_create_class(tree, id):
    term_id_token = extract(tree, "id")
    return ClassCreation(id=id, node_id=term_id_token)


# the KGCL model suggests the command
# 'create node {id} {label} with {annotation set}'
# TODO: handling of {annotation set}
def parse_create(tree, id):
    term_id_token = extract(tree, "id")
    label_token = extract(tree, "label")
    language_token = extract(tree, "language")

    return NodeCreation(
        id=id,
        about_node=term_id_token,
        node_id=term_id_token,
        name=label_token,
        language=language_token,
    )


def parse_change_relationship(tree, id):
    subject_token = extract(tree, "subject")
    object_token = extract(tree, "object")

    edge = Edge(subject=subject_token, object=object_token)

    old_token = extract(tree, "old_predicate")
    new_token = extract(tree, "new_predicate")
    return PredicateChange(
        id=id, about_edge=edge, old_value=old_token, new_value=new_token
    )


def parse_delete_annotated_edge(tree, id):
    subject_token = extract(tree, "subject")
    predicate_token = extract(tree, "predicate")
    object_token = extract(tree, "object")
    annotation_property_token = extract(tree, "annotation_property")
    annotation_token = extract(tree, "annotation")

    annotation = Annotation(
        property=annotation_property_token,
        filler=annotation_token,
    )

    return EdgeDeletion(
        id=id,
        subject=subject_token,
        predicate=predicate_token,
        object=object_token,
        annotation_set=annotation,
    )


def parse_create_annotated_edge(tree, id):
    subject_token = extract(tree, "subject")
    predicate_token = extract(tree, "predicate")
    object_token = extract(tree, "object")
    annotation_property_token = extract(tree, "annotation_property")
    annotation_token = extract(tree, "annotation")

    annotation = Annotation(property=annotation_property_token, filler=annotation_token)

    return EdgeCreation(
        id=id,
        subject=subject_token,
        predicate=predicate_token,
        object=object_token,
        annotation_set=annotation,
    )


def parse_delete_edge(tree, id):
    subject_token = extract(tree, "subject")
    predicate_token = extract(tree, "predicate")
    object_token = extract(tree, "object")

    return EdgeDeletion(
        id=id, subject=subject_token, predicate=predicate_token, object=object_token
    )


def parse_create_edge(tree, id):
    subject_token = extract(tree, "subject")
    predicate_token = extract(tree, "predicate")
    object_token = extract(tree, "object")

    return EdgeCreation(
        id=id, subject=subject_token, predicate=predicate_token, object=object_token
    )


def parse_shallow(tree, id):
    term_id_token = extract(tree, "id")
    old_token = extract(tree, "old_id")
    new_token = extract(tree, "new_id")

    edge = Edge(subject=term_id_token, object=old_token)

    return NodeShallowing(
        id=id, about_edge=edge, old_value=old_token, new_value=new_token
    )


def parse_deepen(tree, id):
    term_id_token = extract(tree, "id")
    old_token = extract(tree, "old_id")
    new_token = extract(tree, "new_id")

    edge = Edge(subject=term_id_token, object=old_token)

    return NodeDeepening(
        id=id, about_edge=edge, old_value=old_token, new_value=new_token
    )


def parse_move(tree, id):
    subject_token = extract(tree, "subject")
    predicate_token = extract(tree, "predicate")
    object_token = extract(tree, "object")

    old_token = extract(tree, "old_id")
    new_token = extract(tree, "new_id")

    edge = Edge(subject=subject_token, predicate=predicate_token, object=object_token)

    return NodeMove(id=id, about_edge=edge, old_value=old_token, new_value=new_token)


def parse_delete(tree, id):
    label_token = extract(tree, "entity")
    return NodeDeletion(id=id, about_node=label_token)


def parse_unobsolete(tree, id):
    term_id_token = extract(tree, "id")
    return NodeUnobsoletion(id=id, about_node=term_id_token)


def parse_obsolete(tree, id):
    label_token = extract(tree, "entity")
    replacement_token = extract(tree, "replacement")
    return NodeObsoletion(
        id=id, about_node=label_token, has_direct_replacement=replacement_token
    )


def parse_rename(tree, id):
    old_token = extract(tree, "old_label")
    new_token = extract(tree, "new_label")
    old_language = extract(tree, "old_language")
    new_language = extract(tree, "new_language")
    term_id_token = extract(tree, "id")

    return NodeRename(
        id=id,
        about_node=term_id_token,
        old_value=old_token,
        new_value=new_token,
        old_language=old_language,
        new_language=new_language,
    )


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
