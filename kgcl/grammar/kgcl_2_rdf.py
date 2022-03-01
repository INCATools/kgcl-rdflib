from kgcl.grammar.parser import parse
from kgcl.utils import from_yaml, to_rdf, to_json
from kgcl.model.kgcl import (
    NodeRename,
    NodeObsoletion,
    NodeUnobsoletion,
    NodeDeletion,
    NodeAnnotationChange,
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
)

# parse kgcl to python data class
# serialse puython data class to yaml
# convert python data class to RDF


def kgcl_2_yaml(kgcl_patch, output):
    parsed_patch = parse(kgcl_patch)
    serialise_yaml(parsed_patch, output)


def serialise_yaml(kgcl_instances, output):

    preamble = """activity_set:
- {id: uuid:876aac6a6ef6, description: "my sane edits", was_associated_with: "https://orcid.org/0000-0002-6601-2165"}
- {id: uuid:e887d3aac33f, description: "deliberate mistakes", was_associated_with: "OntologicalAnarchist"}
change_set:\n"""

    with open(output, "w") as f:
        f.write(preamble)
        for k in kgcl_instances:
            f.write(data_model_to_yaml(k))
            f.write("\n")


def data_model_to_yaml(kgcl_instance):
    if type(kgcl_instance) is NodeRename:
        return rename(kgcl_instance)
    if type(kgcl_instance) is NodeObsoletion:
        return obsoletion(kgcl_instance)
    if type(kgcl_instance) is NodeUnobsoletion:
        return unobsoletion(kgcl_instance)
    if type(kgcl_instance) is NodeDeletion:
        return node_deletion(kgcl_instance)
    if type(kgcl_instance) is NodeMove:
        return node_move(kgcl_instance)
    if type(kgcl_instance) is NodeDeepening:
        return node_deepening(kgcl_instance)
    if type(kgcl_instance) is NodeShallowing:
        return node_shallowing(kgcl_instance)
    if type(kgcl_instance) is EdgeCreation:
        return edge_creation(kgcl_instance)
    if type(kgcl_instance) is EdgeDeletion:
        return edge_deletion(kgcl_instance)
    if type(kgcl_instance) is PredicateChange:
        return predicate_change(kgcl_instance)
    if type(kgcl_instance) is NodeAnnotationChange:
        return node_annotation_change(kgcl_instance)
    if type(kgcl_instance) is NodeCreation:
        return node_creation(kgcl_instance)
    if type(kgcl_instance) is ClassCreation:
        return class_creation(kgcl_instance)
    if type(kgcl_instance) is NewSynonym:
        return new_synonym(kgcl_instance)
    if type(kgcl_instance) is PlaceUnder:
        return place_under(kgcl_instance)
    if type(kgcl_instance) is RemoveUnder:
        return place_under(kgcl_instance)


def rename(kgcl_instance):
    type = "NodeRename"
    id = kgcl_instance.id
    about_node = render_id(
        kgcl_instance.about_node, kgcl_instance.about_node_representation
    )
    old_value = kgcl_instance.old_value
    new_value = kgcl_instance.new_value
    old_language = kgcl_instance.old_language
    new_language = kgcl_instance.new_language

    serialisation = (
        f"type: {type}, "
        f"id: {id}, "
        f"about_node: {about_node}, "
        f"old_value: {old_value}, "
        f"new_value: {new_value}, "
        f"old_language: {old_language}, "
        f"new_language: {new_language}"
    )

    return "- {" + serialisation + "}"


def obsoletion(kgcl_instance):
    type = "NodeObsoletion"
    id = kgcl_instance.id
    about_node = render_id(
        kgcl_instance.about_node, kgcl_instance.about_node_representation
    )
    replacement = kgcl_instance.has_direct_replacement

    serialisation = (
        f"type: {type}, "
        f"id: {id}, "
        f"about_node: {about_node}, "
        f"has_direct_replacement: {replacement} "
    )

    return "- {" + serialisation + "}"


def unobsoletion(kgcl_instance):
    type = "NodeUnobsoletion"
    id = kgcl_instance.id
    about_node = render_id(
        kgcl_instance.about_node, kgcl_instance.about_node_representation
    )

    serialisation = f"type: {type}, " f"id: {id}, " f"about_node: {about_node}"

    return "- {" + serialisation + "}"


def node_deletion(kgcl_instance):
    type = "NodeDeletion"
    id = kgcl_instance.id
    about_node = render_id(
        kgcl_instance.about_node, kgcl_instance.about_node_representation
    )

    serialisation = f"type: {type}, " f"id: {id}, " f"about_node: {about_node}"

    return "- {" + serialisation + "}"


def node_move(kgcl_instance):
    type = "NodeMove"
    id = kgcl_instance.id
    subject = render_id(
        kgcl_instance.about_edge.subject,
        kgcl_instance.about_edge.subject_representation,
    )
    predicate = render_id(
        kgcl_instance.about_edge.predicate,
        kgcl_instance.about_edge.predicate_representation,
    )
    object = render_id(
        kgcl_instance.about_edge.object,
        kgcl_instance.about_edge.object_representation,
    )
    about_edge = (
        f"{{"
        f"subject: {subject}, "
        f"predicate: {predicate}, "
        f"object: {object} "
        f"}}"
    )

    new_value = render_id(kgcl_instance.new_value, kgcl_instance.new_object_type)
    old_value = render_id(kgcl_instance.old_value, kgcl_instance.old_object_type)

    serialisation = (
        f"type: {type}, "
        f"id: {id}, "
        f"about_edge: {about_edge},"
        f"new_value: {new_value}, "
        f"old_value: {old_value} "
    )

    return "- {" + serialisation + "}"


def node_deepening(kgcl_instance):
    type = "NodeDeepening"
    id = kgcl_instance.id
    subject = render_id(
        kgcl_instance.about_edge.subject,
        kgcl_instance.about_edge.subject_representation,
    )
    predicate = render_id(
        kgcl_instance.about_edge.predicate,
        kgcl_instance.about_edge.predicate_representation,
    )
    object = render_id(
        kgcl_instance.about_edge.object,
        kgcl_instance.about_edge.object_representation,
    )
    about_edge = (
        f"{{"
        f"subject: {subject}, "
        f"predicate: {predicate}, "
        f"object: {object} "
        f"}}"
    )

    new_value = render_id(kgcl_instance.new_value, kgcl_instance.new_object_type)
    old_value = render_id(kgcl_instance.old_value, kgcl_instance.old_object_type)

    serialisation = (
        f"type: {type}, "
        f"id: {id}, "
        f"about_edge: {about_edge},"
        f"new_value: {new_value}, "
        f"old_value: {old_value} "
    )

    return "- {" + serialisation + "}"


def node_shallowing(kgcl_instance):
    type = "NodeShallowing"
    id = kgcl_instance.id
    subject = render_id(
        kgcl_instance.about_edge.subject,
        kgcl_instance.about_edge.subject_representation,
    )
    predicate = render_id(
        kgcl_instance.about_edge.predicate,
        kgcl_instance.about_edge.predicate_representation,
    )
    object = render_id(
        kgcl_instance.about_edge.object,
        kgcl_instance.about_edge.object_representation,
    )
    about_edge = (
        f"{{"
        f"subject: {subject}, "
        f"predicate: {predicate}, "
        f"object: {object} "
        f"}}"
    )

    new_value = render_id(kgcl_instance.new_value, kgcl_instance.new_object_type)
    old_value = render_id(kgcl_instance.old_value, kgcl_instance.old_object_type)

    serialisation = (
        f"type: {type}, "
        f"id: {id}, "
        f"about_edge: {about_edge},"
        f"new_value: {new_value}, "
        f"old_value: {old_value} "
    )

    return "- {" + serialisation + "}"


def edge_creation(kgcl_instance):
    type = "EdgeCreation"
    id = kgcl_instance.id
    subject = render_id(
        kgcl_instance.subject,
        kgcl_instance.subject_type,
    )
    predicate = render_id(
        kgcl_instance.predicate,
        kgcl_instance.predicate_type,
    )
    object = render_id(
        kgcl_instance.object,
        kgcl_instance.object_type,
    )

    serialisation = (
        f"type: {type}, "
        f"id: {id}, "
        f"subject: {subject}, "
        f"predicate: {predicate}, "
        f"object: {object} "
    )

    return "- {" + serialisation + "}"


def edge_deletion(kgcl_instance):
    type = "EdgeDeletion"
    id = kgcl_instance.id
    subject = render_id(
        kgcl_instance.subject,
        kgcl_instance.subject_type,
    )
    predicate = render_id(
        kgcl_instance.predicate,
        kgcl_instance.predicate_type,
    )
    object = render_id(
        kgcl_instance.object,
        kgcl_instance.object_type,
    )

    serialisation = (
        f"type: {type}, "
        f"id: {id}, "
        f"subject: {subject}, "
        f"predicate: {predicate}, "
        f"object: {object} "
    )

    return "- {" + serialisation + "}"


def predicate_change(kgcl_instance):
    type = "PredicateChange"
    id = kgcl_instance.id
    subject = render_id(
        kgcl_instance.about_edge.subject,
        kgcl_instance.about_edge.subject_representation,
    )
    predicate = render_id(
        kgcl_instance.about_edge.predicate,
        kgcl_instance.about_edge.predicate_representation,
    )
    object = render_id(
        kgcl_instance.about_edge.object,
        kgcl_instance.about_edge.object_representation,
    )
    about_edge = (
        f"{{"
        f"subject: {subject}, "
        f"predicate: {predicate}, "
        f"object: {object} "
        f"}}"
    )
    old_value = kgcl_instance.old_value
    new_value = kgcl_instance.new_value
    old_language = kgcl_instance.old_language
    new_language = kgcl_instance.new_language

    serialisation = (
        f"type: {type}, "
        f"id: {id}, "
        f"about_edge: {about_edge},"
        f"old_value: {old_value}, "
        f"new_value: {new_value}, "
        f"old_language: {old_language}, "
        f"new_language: {new_language}"
    )

    return "- {" + serialisation + "}"


def node_annotation_change(kgcl_instance):
    type = "NodeAnnotationChange"
    id = kgcl_instance.id
    about_node = render_id(
        kgcl_instance.about_node, kgcl_instance.about_node_representation
    )
    old_value = kgcl_instance.old_value
    new_value = kgcl_instance.new_value
    old_language = kgcl_instance.old_language
    new_language = kgcl_instance.new_language
    old_datatype = kgcl_instance.old_datatype
    new_datatype = kgcl_instance.new_datatype

    serialisation = (
        f"type: {type}, "
        f"id: {id}, "
        f"about_node: {about_node},"
        f"old_value: {old_value}, "
        f"new_value: {new_value}, "
        f"old_language: {old_language}, "
        f"new_language: {new_language},"
        f"old_datatype: {old_datatype}, "
        f"new_datatype: {new_datatype}"
    )

    return "- {" + serialisation + "}"


def node_creation(kgcl_instance):
    type = "NodeCreation"
    id = kgcl_instance.id
    about_node = render_id(
        kgcl_instance.about_node, kgcl_instance.about_node_representation
    )
    name = kgcl_instance.name
    language = kgcl_instance.language

    serialisation = (
        f"type: {type}, "
        f"id: {id}, "
        f"about_node: {about_node}, "
        f"language: {language},"
        f"name: {name}"
    )

    return "- {" + serialisation + "}"


def class_creation(kgcl_instance):
    type = "ClassCreation"
    id = kgcl_instance.id
    about_node = render_id(
        kgcl_instance.about_node, kgcl_instance.about_node_representation
    )

    serialisation = f"type: {type}, " f"id: {id}, " f"about_node: {about_node}, "

    return "- {" + serialisation + "}"


def new_synonym(kgcl_instance):
    type = "NewSynonym"
    id = kgcl_instance.id
    about_node = render_id(
        kgcl_instance.about_node, kgcl_instance.about_node_representation
    )
    new_value = kgcl_instance.new_value
    qualifier = kgcl_instance.qualifier
    language = kgcl_instance.language

    serialisation = (
        f"type: {type}, "
        f"id: {id}, "
        f"about_node: {about_node}, "
        f"language: {language},"
        f"new_value: {new_value},"
        f"qualifier: {qualifier}"
    )

    return "- {" + serialisation + "}"


def place_under(kgcl_instance):
    type = "PlaceUnder"
    id = kgcl_instance.id
    subject = render_id(
        kgcl_instance.subject,
        kgcl_instance.subject_type,
    )
    predicate = render_id(
        kgcl_instance.predicate,
        kgcl_instance.predicate_type,
    )
    object = render_id(
        kgcl_instance.object,
        kgcl_instance.object_type,
    )

    serialisation = (
        f"type: {type}, "
        f"id: {id}, "
        f"subject: {subject}, "
        f"predicate: {predicate}, "
        f"object: {object} "
    )

    return "- {" + serialisation + "}"


def remove_under(kgcl_instance):
    type = "RemoveUnder"
    id = kgcl_instance.id
    subject = render_id(
        kgcl_instance.subject,
        kgcl_instance.subject_type,
    )
    predicate = render_id(
        kgcl_instance.predicate,
        kgcl_instance.predicate_type,
    )
    object = render_id(
        kgcl_instance.object,
        kgcl_instance.object_type,
    )

    serialisation = (
        f"type: {type}, "
        f"id: {id}, "
        f"subject: {subject}, "
        f"predicate: {predicate}, "
        f"object: {object} "
    )

    return "- {" + serialisation + "}"


def render_id(id, type):
    if type == "label":
        return '"' + str(id) + '"'
    else:
        return str(id)
