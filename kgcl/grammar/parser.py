from lark import Lark, Token
import re
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
    """
    Returns a new ID for KGCL change operations.
    """
    id = 0
    while True:
        yield id
        id += 1


# initialise ID generator
id_gen = id_generator()


# initialise parser
path = Path(__file__).parent
kgcl_parser = Lark.open(str(path) + "/kgcl.lark", start="expression")


def parse(input):
    """
    Parse a set of KGCL command separated by \n and
    return instantiated dataclass objects from model.kgcl.
    """
    statements = input.splitlines()
    parsed = []

    for s in statements:
        parsed.append(parse_statement(s))
    return parsed


def parse_statement(input):
    """
    Parse a KGCL command and
    return an instantiated dataclass object from model.kgcl.
    """

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

    subclass, s_representation = get_entity_representation(subclass_token)
    property, p_representation = get_entity_representation(property_token)
    filler, f_representation = get_entity_representation(filler_token)

    return ExistentialRestrictionDeletion(
        id=id,
        subclass=subclass,
        property=property,
        filler=filler,
        subclass_type=s_representation,
        property_type=p_representation,
        filler_type=f_representation,
    )


def parse_add_existential_restriction_axiom(tree, id):
    subclass_token = extract(tree, "subclass")
    property_token = extract(tree, "property")
    filler_token = extract(tree, "filler")

    subclass, s_representation = get_entity_representation(subclass_token)
    property, p_representation = get_entity_representation(property_token)
    filler, f_representation = get_entity_representation(filler_token)

    return ExistentialRestrictionCreation(
        id=id,
        subclass=subclass,
        property=property,
        filler=filler,
        subclass_type=s_representation,
        property_type=p_representation,
        filler_type=f_representation,
    )


def parse_delete_subsumption_axiom(tree, id):
    subclass_token = extract(tree, "subclass")
    superclass_token = extract(tree, "superclass")

    subclass, sub_representation = get_entity_representation(subclass_token)
    superclass, sup_representation = get_entity_representation(superclass_token)

    # TODO the hardcoded owl:subClassOf should be part of the data model
    return RemoveUnder(
        id=id,
        subject=subclass,
        predicate="<http://www.w3.org/2000/01/rdf-schema#subClassOf>",
        object=superclass,
        subject_type=sub_representation,
        object_type=sup_representation,
    )


def parse_add_subsumption_axiom(tree, id):
    subclass_token = extract(tree, "subclass")
    superclass_token = extract(tree, "superclass")

    subclass, sub_representation = get_entity_representation(subclass_token)
    superclass, sup_representation = get_entity_representation(superclass_token)

    # TODO the hardcoded owl:subClassOf should be part of the data model
    return PlaceUnder(
        id=id,
        subject=subclass,
        predicate="<http://www.w3.org/2000/01/rdf-schema#subClassOf>",
        object=superclass,
        subject_type=sub_representation,
        object_type=sup_representation,
    )


def parse_create_synonym(tree, id):
    entity_token = extract(tree, "entity")
    entity, representation = get_entity_representation(entity_token)

    synonym_string_token = extract(tree, "synonym")
    synonym, representation2 = get_entity_representation(synonym_string_token)

    language_token = extract(tree, "language")
    qualifier_token = extract(tree, "synonym_qualifier")

    return NewSynonym(
        id=id,
        about_node=entity,
        about_node_representation=representation,
        new_value=synonym,
        qualifier=qualifier_token,
        language=language_token,
    )


def parse_create_class(tree, id):
    term_id_token = extract(tree, "id")
    entity, representation = get_entity_representation(term_id_token)

    return ClassCreation(
        id=id, node_id=entity, about_node_representation=representation
    )


# the KGCL model suggests the command
# 'create node {id} {label} with {annotation set}'
# TODO: handling of {annotation set}
def parse_create(tree, id):
    term_id_token = extract(tree, "id")
    label_token = extract(tree, "label")
    language_token = extract(tree, "language")

    entity, representation = get_entity_representation(term_id_token)

    return NodeCreation(
        id=id,
        about_node=entity,
        about_node_representation=representation,
        node_id=term_id_token,
        name=label_token,
        language=language_token,
    )


def parse_change_relationship(tree, id):
    subject_token = extract(tree, "entity_subject")
    object_token = extract(tree, "entity_object")

    subject, s_representation = get_entity_representation(subject_token)
    object, o_representation = get_entity_representation(object_token)

    old_token = extract(tree, "old_entity")
    new_token = extract(tree, "new_entity")

    old, old_representation = get_entity_representation(old_token)
    new, new_representation = get_entity_representation(new_token)

    edge = Edge(
        subject=subject,
        predicate=old,
        object=object,
        subject_representation=s_representation,
        predicate_representation=old_representation,
        object_representation=o_representation,
    )

    language_token = extract(tree, "language")
    datatype_token = extract(tree, "datatype")

    return PredicateChange(
        id=id,
        about_edge=edge,
        old_value=old,
        new_value=new,
        old_value_type=old_representation,
        new_value_type=new_representation,
        language=language_token,
        datatype=datatype_token,
    )


def parse_delete_annotated_edge(tree, id):
    subject_token = extract(tree, "entity_subject")
    predicate_token = extract(tree, "entity_predicate")
    object_token = extract(tree, "entity_object")

    subject, s_representation = get_entity_representation(subject_token)
    predicate, p_representation = get_entity_representation(predicate_token)
    object, o_representation = get_entity_representation(object_token)

    annotation_property_token = extract(tree, "annotation_property")
    annotation_token = extract(tree, "annotation")

    annotation_property, prop_representation = get_entity_representation(
        annotation_property_token
    )
    annotation, a_representation = get_entity_representation(annotation_token)

    annotation_set = Annotation(
        property=annotation_property,
        filler=annotation,
        property_type=prop_representation,
        filler_type=a_representation,
    )

    return EdgeDeletion(
        id=id,
        subject=subject,
        predicate=predicate,
        object=object,
        subject_type=s_representation,
        predicate_type=p_representation,
        object_type=o_representation,
        annotation_set=annotation_set,
    )


def parse_create_annotated_edge(tree, id):
    subject_token = extract(tree, "entity_subject")
    predicate_token = extract(tree, "entity_predicate")
    object_token = extract(tree, "entity_object")

    subject, s_representation = get_entity_representation(subject_token)
    predicate, p_representation = get_entity_representation(predicate_token)
    object, o_representation = get_entity_representation(object_token)

    annotation_property_token = extract(tree, "annotation_property")
    annotation_token = extract(tree, "annotation")

    annotation_property, prop_representation = get_entity_representation(
        annotation_property_token
    )
    annotation, a_representation = get_entity_representation(annotation_token)

    annotation_set = Annotation(
        property=annotation_property,
        filler=annotation,
        property_type=prop_representation,
        filler_type=a_representation,
    )

    return EdgeCreation(
        id=id,
        subject=subject,
        predicate=predicate,
        object=object,
        subject_type=s_representation,
        predicate_type=p_representation,
        object_type=o_representation,
        annotation_set=annotation_set,
    )


def parse_delete_edge(tree, id):
    subject_token = extract(tree, "entity_subject")
    predicate_token = extract(tree, "entity_predicate")
    object_token = extract(tree, "entity_object")

    subject, s_representation = get_entity_representation(subject_token)
    predicate, p_representation = get_entity_representation(predicate_token)
    object, o_representation = get_entity_representation(object_token)

    language_token = extract(tree, "language")
    datatype_token = extract(tree, "datatype")

    return EdgeDeletion(
        id=id,
        subject=subject,
        predicate=predicate,
        object=object,
        subject_type=s_representation,
        predicate_type=p_representation,
        object_type=o_representation,
        language=language_token,
        datatype=datatype_token,
    )


def parse_create_edge(tree, id):
    subject_token = extract(tree, "entity_subject")
    predicate_token = extract(tree, "entity_predicate")
    object_token = extract(tree, "entity_object")

    subject, s_representation = get_entity_representation(subject_token)
    predicate, p_representation = get_entity_representation(predicate_token)
    object, o_representation = get_entity_representation(object_token)

    language_token = extract(tree, "language")
    datatype_token = extract(tree, "datatype")

    return EdgeCreation(
        id=id,
        subject=subject,
        predicate=predicate,
        object=object,
        subject_type=s_representation,
        predicate_type=p_representation,
        object_type=o_representation,
        language=language_token,
        datatype=datatype_token,
    )


def parse_shallow(tree, id):
    entity_token = extract(tree, "entity")
    old_token = extract(tree, "old_entity")
    new_token = extract(tree, "new_entity")

    entity, e_representation = get_entity_representation(entity_token)
    old_entity, o_representation = get_entity_representation(old_token)
    new_entity, n_representation = get_entity_representation(new_token)

    edge = Edge(
        subject=entity,
        object=old_entity,
        subject_representation=e_representation,
        object_representation=o_representation,
    )

    return NodeShallowing(
        id=id,
        about_edge=edge,
        old_value=old_entity,
        new_value=new_entity,
        old_object_type=o_representation,
        new_object_type=n_representation,
    )


def parse_deepen(tree, id):
    entity_token = extract(tree, "entity")
    old_token = extract(tree, "old_entity")
    new_token = extract(tree, "new_entity")

    entity, e_representation = get_entity_representation(entity_token)
    old_entity, o_representation = get_entity_representation(old_token)
    new_entity, n_representation = get_entity_representation(new_token)

    edge = Edge(
        subject=entity,
        object=old_entity,
        subject_representation=e_representation,
        object_representation=o_representation,
    )

    return NodeDeepening(
        id=id,
        about_edge=edge,
        old_value=old_entity,
        new_value=new_entity,
        old_object_type=o_representation,
        new_object_type=n_representation,
    )


def parse_move(tree, id):
    subject_token = extract(tree, "entity_subject")
    predicate_token = extract(tree, "entity_predicate")
    object_token = extract(tree, "entity_object")

    subject, s_representation = get_entity_representation(subject_token)
    predicate, p_representation = get_entity_representation(predicate_token)
    object, o_representation = get_entity_representation(object_token)

    old_token = extract(tree, "old_entity")
    new_token = extract(tree, "new_entity")

    old, old_representation = get_entity_representation(old_token)
    new, new_representation = get_entity_representation(new_token)

    edge = Edge(
        subject=subject,
        predicate=predicate,
        object=object,
        subject_representation=s_representation,
        predicate_representation=p_representation,
        object_representation=o_representation,
    )

    return NodeMove(
        id=id,
        about_edge=edge,
        old_value=old,
        new_value=new,
        old_object_type=old_representation,
        new_object_type=new_representation,
    )


def parse_delete(tree, id):
    entity_token = extract(tree, "entity")
    entity, representation = get_entity_representation(entity_token)

    return NodeDeletion(
        id=id, about_node=entity, about_node_representation=representation
    )


def parse_unobsolete(tree, id):
    entity_token = extract(tree, "entity")
    entity, representation = get_entity_representation(entity_token)

    return NodeUnobsoletion(
        id=id, about_node=entity, about_node_representation=representation
    )


def parse_obsolete(tree, id):
    entity_token = extract(tree, "entity")
    entity, representation = get_entity_representation(entity_token)

    replacement_token = extract(tree, "replacement")

    return NodeObsoletion(
        id=id,
        about_node=entity,
        about_node_representation=representation,
        has_direct_replacement=replacement_token,
    )


def parse_rename(tree, id):
    old_token = extract(tree, "old_label")
    new_token = extract(tree, "new_label")
    old_language = extract(tree, "old_language")
    new_language = extract(tree, "new_language")

    # TODO old_token and new_token are enclosed in ''

    term_id_token = extract(tree, "id")
    if term_id_token is not None:
        entity, representation = get_entity_representation(term_id_token)
    else:
        entity = None
        representation = None

    return NodeRename(
        id=id,
        about_node=entity,
        about_node_representation=representation,
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


def get_entity_representation(entity):
    first_character = entity[0]
    last_character = entity[-1:]
    if first_character == "<" and last_character == ">":
        return entity, "uri"  # not removing brackets (TODO why?)
    if first_character == "'" and last_character == "'" and entity[1] != "'":
        return entity[1:-1], "label"
    if first_character == '"' and last_character == '"':
        return entity[1:-1], "literal"
    if entity[0:3] == '"""' and entity[-3:] == '"""':
        return entity[3:-3], "literal"
    if entity[0:3] == "'''" and entity[-3:] == "'''":
        return entity[3:-3], "literal"

    # TODO: use predefined set of prefixes to identify CURIEs
    return entity, "curie"
    # return entity, "error"


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
