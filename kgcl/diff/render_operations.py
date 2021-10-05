from kgcl.model.kgcl import (
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
    PlaceUnder,
    RemoveUnder,
    RemovedNodeFromSubset,
    ExistentialRestrictionCreation,
    ExistentialRestrictionDeletion,
)


def render_entity(entity, rdf_type):
    entity = repr(entity)[1:-1]
    if rdf_type == "uri":
        return "<" + entity + ">"
    elif rdf_type == "label":
        if "'" in entity:
            # TODO: replacing quotes with backticks
            # is only a temporary workaround
            entity = entity.replace("'", "`")
        return "'" + entity + "'"
    elif rdf_type == "literal":
        # TODO: test this
        if '"' not in entity:
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


def render(kgcl_instance):

    if type(kgcl_instance) is NodeRename:
        # TODO: subject could be 'None'?
        subject = render_entity(kgcl_instance.about_node, "uri")
        old = render_entity(kgcl_instance.old_value, "label")
        new = render_entity(kgcl_instance.new_value, "label")

        new_language = kgcl_instance.new_language
        old_language = kgcl_instance.old_language

        if old_language is not None:
            old = old + "@" + old_language

        if new_language is not None:
            new = new + "@" + new_language

        return "rename " + subject + " from " + old + " to " + new

    if type(kgcl_instance) is NodeObsoletion:
        subject = render_entity(kgcl_instance.about_node, "uri")
        # TODO: type this correctly
        replacement = render_entity(kgcl_instance.has_direct_replacement, "uri")
        if kgcl_instance.has_direct_replacement is not None:
            return "obsolete " + subject + " with replacement " + replacement
        else:
            return "obsolete " + subject

    if type(kgcl_instance) is NodeUnobsoletion:
        subject = render_entity(kgcl_instance.about_node, "uri")
        return "unobsolete " + subject

    if type(kgcl_instance) is NodeDeletion:
        subject = render_entity(kgcl_instance.about_node, "uri")
        return "delete " + subject

    if type(kgcl_instance) is NodeMove:
        subject = render_entity(kgcl_instance.about_edge.subject, "uri")
        predicate = render_entity(kgcl_instance.about_edge.predicate, "uri")
        new = render_entity(kgcl_instance.new_value, kgcl_instance.new_object_type)
        old = render_entity(kgcl_instance.old_value, kgcl_instance.old_object_type)
        return (
            "move "
            + subject
            + " "
            + predicate
            + " "
            + old
            + " "
            + "from"
            + " "
            + old
            + " "
            + "to"
            + " "
            + new
        )

    if type(kgcl_instance) is EdgeCreation:
        if kgcl_instance.annotation_set is None:
            return render_edge_creation(kgcl_instance)
        else:
            return render_annotation_creation(kgcl_instance)

    if type(kgcl_instance) is EdgeDeletion:
        if kgcl_instance.annotation_set is None:
            return render_edge_deletion(kgcl_instance)
        else:
            return render_annotation_deletion(kgcl_instance)

    if type(kgcl_instance) is PredicateChange:
        subject = render_entity(kgcl_instance.about_edge.subject, "uri")
        object = render_entity(
            kgcl_instance.about_edge.object, kgcl_instance.object_type
        )
        new = render_entity(kgcl_instance.new_value, "uri")
        old = render_entity(kgcl_instance.old_value, "uri")

        if kgcl_instance.language is not None:
            object += "@" + kgcl_instance.language

        if kgcl_instance.datatype is not None:
            object += "^^" + kgcl_instance.datatype

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

    if type(kgcl_instance) is NodeCreation:
        subject = render_entity(kgcl_instance.about_node, "uri")
        label = render_entity(kgcl_instance.name, "label")
        if kgcl_instance.name is not None:
            return "create node " + subject + " " + label
        else:
            return "create " + subject

    if type(kgcl_instance) is ClassCreation:
        subject = render_entity(kgcl_instance.about_node, "uri")
        return "create " + subject

    if type(kgcl_instance) is NewSynonym:
        subject = render_entity(kgcl_instance.about_node, "uri")
        synonym = render_entity(kgcl_instance.new_value, "label")
        qualifier = kgcl_instance.qualifier
        language = kgcl_instance.language

        if language is not None:
            synonym = synonym + "@" + language

        if qualifier is not None:
            return (
                "create " + qualifier + " synonym" + " " + synonym + " for " + subject
            )
        else:
            return "create synonym " + synonym + " for " + subject

    if type(kgcl_instance) is ExistentialRestrictionCreation:
        subclass = render_entity(kgcl_instance.subclass, "uri")
        property = render_entity(kgcl_instance.property, "uri")
        filler = render_entity(kgcl_instance.filler, "uri")
        return "add " + subclass + " SubClassOf " + property + " some " + filler

    if type(kgcl_instance) is ExistentialRestrictionDeletion:
        subclass = render_entity(kgcl_instance.subclass, "uri")
        property = render_entity(kgcl_instance.property, "uri")
        filler = render_entity(kgcl_instance.filler, "uri")
        return "delete " + subclass + " SubClassOf " + property + " some " + filler

    if type(kgcl_instance) is PlaceUnder:
        subclass = render_entity(kgcl_instance.subject, "uri")
        superclass = render_entity(kgcl_instance.object, "uri")
        return "add " + subclass + " SubClassOf " + superclass

    if type(kgcl_instance) is RemoveUnder:
        subclass = render_entity(kgcl_instance.subject, "uri")
        superclass = render_entity(kgcl_instance.object, "uri")
        return "delete " + subclass + " SubClassOf " + superclass


def render_annotation_creation(kgcl_instance):
    subject = render_entity(kgcl_instance.subject, "uri")
    predicate = render_entity(kgcl_instance.predicate, "uri")
    object = render_entity(kgcl_instance.object, kgcl_instance.object_type)

    annotation = kgcl_instance.annotation_set
    annotation_property = render_entity(annotation.property, "uri")
    annotation_filler = render_entity(annotation.filler, annotation.filler_type)

    language = kgcl_instance.language
    datatype = kgcl_instance.datatype

    if language is not None:
        object = object + "@" + language
    if datatype is not None:
        object = object + "^^" + datatype

    return (
        "create edge <<"
        + subject
        + " "
        + predicate
        + " "
        + object
        + ">>"
        + " "
        + annotation_property
        + " "
        + annotation_filler
    )


def render_annotation_deletion(kgcl_instance):
    subject = render_entity(kgcl_instance.subject, "uri")
    predicate = render_entity(kgcl_instance.predicate, "uri")
    object = render_entity(kgcl_instance.object, kgcl_instance.object_type)

    annotation = kgcl_instance.annotation_set
    annotation_property = render_entity(annotation.property, "uri")
    annotation_filler = render_entity(annotation.filler, annotation.filler_type)

    language = kgcl_instance.language
    datatype = kgcl_instance.datatype

    if language is not None:
        object = object + "@" + language
    if datatype is not None:
        object = object + "^^" + datatype

    return (
        "delete edge <<"
        + subject
        + " "
        + predicate
        + " "
        + object
        + ">>"
        + " "
        + annotation_property
        + " "
        + annotation_filler
    )


def render_edge_deletion(kgcl_instance):
    subject = render_entity(kgcl_instance.subject, "uri")
    predicate = render_entity(kgcl_instance.predicate, "uri")
    object = render_entity(kgcl_instance.object, kgcl_instance.object_type)
    # object = render_entity(repr(kgcl_instance.object)[1:-1])

    language = kgcl_instance.language
    datatype = kgcl_instance.datatype

    base = "delete edge " + subject + " " + predicate + " " + object

    if language is not None:
        return base + "@" + language
    elif datatype is not None:
        return base + "^^" + datatype
    else:
        return base


def render_edge_creation(kgcl_instance):
    subject = render_entity(kgcl_instance.subject, "uri")
    predicate = render_entity(kgcl_instance.predicate, "uri")
    object = render_entity(kgcl_instance.object, kgcl_instance.object_type)

    language = kgcl_instance.language
    datatype = kgcl_instance.datatype

    base = "create edge " + subject + " " + predicate + " " + object

    if language is not None:
        return base + "@" + language
    elif datatype is not None:
        return base + "^^" + datatype
    else:
        return base
