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


# TODO: extract prefix of curies
# TODO: hardcode map of prefixeds for curies


def get_prefix(curie):
    return curie.split(":")[0]


prefix_2_uri = {
    "obo": "<http://purl.obolibrary.org/obo/>",
    "ex": "<http://example.org/>",
    # TODO add more prefixes
}


def is_label(input):
    return re.match(r"\'[^ \s\'].*\'", input)


def is_id(input):
    return re.match(r"<\S+>", input)


def convert(kgclInstance):

    # label renaming
    if type(kgclInstance) is NodeRename:
        if is_label(kgclInstance.old_value) and is_label(kgclInstance.new_value):
            return rename(kgclInstance)

    # node obsoletion
    if type(kgclInstance) is NodeObsoletion:
        representation = kgclInstance.about_node_representation
        if representation == "uri":
            return obsolete_by_id(kgclInstance)
        if representation == "label":
            return obsolete_by_label(kgclInstance)
        if representation == "curie":
            return obsolete_curie(kgclInstance)

    # node obsoletion
    if type(kgclInstance) is NodeUnobsoletion:
        representation = kgclInstance.about_node_representation
        if representation == "uri":
            return unobsolete_by_id(kgclInstance)
        if representation == "label":
            return unobsolete_by_label(kgclInstance)
        if representation == "curie":
            return unobsolete_curie(kgclInstance)

    # node deletion
    if type(kgclInstance) is NodeDeletion:
        representation = kgclInstance.about_node_representation
        if representation == "uri":
            return delete_by_id(kgclInstance)
        if representation == "label":
            return delete_by_label(kgclInstance)
        if representation == "curie":
            return delete_curie(kgclInstance)

    # node creation
    if type(kgclInstance) is NodeCreation:
        if is_id(kgclInstance.node_id) and is_label(kgclInstance.name):
            return create_node(kgclInstance)

    # class creation
    if type(kgclInstance) is ClassCreation:
        if is_id(kgclInstance.node_id):
            return create_class(kgclInstance)

    # node deepending
    if type(kgclInstance) is NodeDeepening:
        return node_deepening(kgclInstance)

    # node shallowing
    if type(kgclInstance) is NodeShallowing:
        return node_shallowing(kgclInstance)

    # edge creation
    if type(kgclInstance) is EdgeCreation:
        if kgclInstance.annotation_set is None:
            return edge_creation(kgclInstance)
        else:
            return edge_annotation_creation(kgclInstance)

    if type(kgclInstance) is PlaceUnder:
        return edge_creation(kgclInstance)

    if type(kgclInstance) is RemoveUnder:
        return edge_deletion(kgclInstance)

    # edge deletion
    if type(kgclInstance) is EdgeDeletion:
        if (
            is_id(kgclInstance.subject)
            and is_id(kgclInstance.predicate)
            # and (is_id(kgclInstance.object) or is_label(kgclInstance.object))
        ):

            if kgclInstance.annotation_set is None:
                return edge_deletion(kgclInstance)
            else:
                return edge_annotation_deletion(kgclInstance)

    # node move
    if type(kgclInstance) is NodeMove:
        return node_move(kgclInstance)

    if type(kgclInstance) is NewSynonym:
        representation = kgclInstance.about_node_representation

        # if is_id(kgclInstance.about_node) and is_label(kgclInstance.new_value):
        if representation == "uri":
            return new_synonym_for_uri(kgclInstance)
        if representation == "label":
            return new_synonym_for_label(kgclInstance)
        if representation == "curie":
            return new_synonym_for_curie(kgclInstance)

    if type(kgclInstance) is PredicateChange:
        return change_predicate(kgclInstance)

    if type(kgclInstance) is RemovedNodeFromSubset:
        if is_id(kgclInstance.about_node) and is_id(kgclInstance.subset):
            return remove_node_from_subset(kgclInstance)

    if type(kgclInstance) is ExistentialRestrictionCreation:
        return create_existential_restriction(kgclInstance)

    if type(kgclInstance) is ExistentialRestrictionDeletion:
        return delete_existential_restriction(kgclInstance)


def node_move(kgclInstance):

    # NB: object and old_value are the (necessarily) the same
    subject = kgclInstance.about_edge.subject
    predicate = kgclInstance.about_edge.predicate
    object = kgclInstance.about_edge.object

    subject_type = kgclInstance.about_edge.subject_representation
    predicate_type = kgclInstance.about_edge.predicate_representation
    object_type = kgclInstance.about_edge.object_representation

    old_value = kgclInstance.old_value
    new_value = kgclInstance.new_value

    old_type = kgclInstance.old_object_type
    new_type = kgclInstance.new_object_type

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "

    # set up prefixes  for curies as needed
    if subject_type == "curie":
        curie_prefix = get_prefix(subject)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    if predicate_type == "curie":
        curie_prefix = get_prefix(predicate)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    if object_type == "curie":
        curie_prefix = get_prefix(object)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    if old_type == "curie":
        curie_prefix = get_prefix(old_value)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    if new_type == "curie":
        curie_prefix = get_prefix(new_value)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    deleteQuery = "?subject " + predicate + " ?old . "

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = "?subject " + predicate + " ?new . "

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = ""

    if old_type == "label":
        whereQuery += "?old rdfs:label ?old_label . "
        whereQuery += ' FILTER(STR(?old_label)="' + old_value + '") '
    else:
        whereQuery += " BIND(" + old_value + " AS ?old) "

    if new_type == "label":
        whereQuery += "?new rdfs:label ?new_label . "
        whereQuery += ' FILTER(STR(?new_label)="' + new_value + '") '
    else:
        whereQuery += " BIND(" + new_value + " AS ?new) "

    if subject_type == "label":
        whereQuery += "?subject rdfs:label ?entity_label . "
        whereQuery += ' FILTER(STR(?entity_label)="' + subject + '") '
    else:
        whereQuery += " BIND(" + subject + " AS ?subject) "

    whereQuery += "?subject " + predicate + " ?old . "

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def remove_node_from_subset(kgclInstance):

    about = kgclInstance.about_node
    subset = kgclInstance.subset

    updateQuery = (
        f"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"
        f"PREFIX obo: <http://purl.obolibrary.org/obo/>"
        f"DELETE {{ {about} obo:inSubset {subset} }}"
        f"WHERE {{ {about} obo:inSubset {subset} }}"
    )

    # prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    # prefix += "PREFIX obo: <http://purl.obolibrary.org/obo/> "

    # deleteQuery = about + " obo:inSubset " + subset + " . "

    # delete = "DELETE {" + deleteQuery + "}"

    # whereQuery = about + " obo:inSubset " + subset + " . "

    # where = "WHERE { " + whereQuery + " }"

    # updateQuery = prefix + " " + delete + " " + where

    return updateQuery


def change_predicate(kgclInstance):

    subject = kgclInstance.about_edge.subject
    object = kgclInstance.about_edge.object

    old_value = kgclInstance.old_value
    new_value = kgclInstance.new_value

    language = kgclInstance.language
    datatype = kgclInstance.datatype

    subject_type = kgclInstance.about_edge.subject_representation
    object_type = kgclInstance.about_edge.object_representation

    old_value_type = kgclInstance.old_value_type
    new_value_type = kgclInstance.new_value_type

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "

    if subject_type == "curie":
        curie_prefix = get_prefix(subject)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    if object_type == "curie":
        curie_prefix = get_prefix(subject)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    if old_value_type == "curie":
        curie_prefix = get_prefix(old_value)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    if new_value_type == "curie":
        curie_prefix = get_prefix(new_value)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    deleteQuery = "?subject ?old ?object . "

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = "?subject ?new ?object . "

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = deleteQuery

    if subject_type == "label":
        whereQuery += "?subject rdfs:label ?subject_label . "
        whereQuery += ' FILTER(STR(?subject_label)="' + subject + '") '
    else:
        whereQuery += " BIND(" + subject + " AS ?subject) "

    if object_type == "label":
        whereQuery += "?object rdfs:label ?object_label . "
        whereQuery += ' FILTER(STR(?object_label)="' + object + '") '
    else:
        whereQuery += " BIND(" + object + " AS ?object) "

    whereQuery += " BIND(" + old_value + " AS ?old) "
    whereQuery += " BIND(" + new_value + " AS ?new) "

    # TODO: this needs to be reworked
    # if datatype is not None:
    #    whereQuery += " BIND( STRDT(" + object + "," + datatype + ") AS ?object) "
    # elif language is not None:
    #    whereQuery += "BIND( STRLANG(" + object + ',"' + language + '") AS ?object) '
    # else:
    #    whereQuery += "BIND(" + object + " AS ?object)"

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def node_deepening(kgclInstance):

    entity = kgclInstance.about_edge.subject
    old_value = kgclInstance.old_value
    new_value = kgclInstance.new_value

    entity_type = kgclInstance.about_edge.subject_representation
    old_type = kgclInstance.old_object_type
    new_type = kgclInstance.new_object_type

    # curie
    # label
    # uri

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "

    # set up prefixes  for curies as needed
    if entity_type == "curie":
        curie_prefix = get_prefix(entity)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    if old_type == "curie":
        curie_prefix = get_prefix(old_value)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    if new_type == "curie":
        curie_prefix = get_prefix(new_value)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    # query for labels
    # query for curies and uris

    deleteQuery = "?entity ?relation ?old . "

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = "?entity ?relation ?new . "

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = ""

    if old_type == "label":
        whereQuery += "?old rdfs:label ?old_label . "
        whereQuery += ' FILTER(STR(?old_label)="' + old_value + '") '
    else:
        whereQuery += " BIND(" + old_value + " AS ?old) "

    if new_type == "label":
        whereQuery += "?new rdfs:label ?new_label . "
        whereQuery += ' FILTER(STR(?new_label)="' + new_value + '") '
    else:
        whereQuery += " BIND(" + new_value + " AS ?new) "

    if entity_type == "label":
        whereQuery += "?entity rdfs:label ?entity_label . "
        whereQuery += ' FILTER(STR(?entity_label)="' + entity + '") '
    else:
        whereQuery += " BIND(" + entity + " AS ?entity) "

    whereQuery += "?entity ?relation ?old . "
    whereQuery += "?new ?relation ?old . "

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def node_shallowing(kgclInstance):

    entity = kgclInstance.about_edge.subject
    old_value = kgclInstance.old_value
    new_value = kgclInstance.new_value

    entity_type = kgclInstance.about_edge.subject_representation
    old_type = kgclInstance.old_object_type
    new_type = kgclInstance.new_object_type

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "

    # set up prefixes  for curies as needed
    if entity_type == "curie":
        curie_prefix = get_prefix(entity)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    if old_type == "curie":
        curie_prefix = get_prefix(old_value)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    if new_type == "curie":
        curie_prefix = get_prefix(new_value)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    # query for labels
    # query for curies and uris

    deleteQuery = "?entity ?relation ?old . "

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = "?entity ?relation ?new . "

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = ""

    if old_type == "label":
        whereQuery += "?old rdfs:label ?old_label . "
        whereQuery += ' FILTER(STR(?old_label)="' + old_value + '") '
    else:
        whereQuery += " BIND(" + old_value + " AS ?old) "

    if new_type == "label":
        whereQuery += "?new rdfs:label ?new_label . "
        whereQuery += ' FILTER(STR(?new_label)="' + new_value + '") '
    else:
        whereQuery += " BIND(" + new_value + " AS ?new) "

    if entity_type == "label":
        whereQuery += "?entity rdfs:label ?entity_label . "
        whereQuery += ' FILTER(STR(?entity_label)="' + entity + '") '
    else:
        whereQuery += " BIND(" + entity + " AS ?entity) "

    whereQuery += "?entity ?relation ?old . "
    whereQuery += "?old ?relation ?new . "

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


# TODO: handling of language tags
# look things up at https://www.ebi.ac.uk/ols/ontologies/iao
def unobsolete_by_id(kgclInstance):
    about = kgclInstance.about_node
    # http://wiki.geneontology.org/index.php/Restoring_an_Obsolete_Ontology_Term
    # 1. remove 'obsolete' from label
    # 2. remove 'OBSOLETE' from definition
    # 3. update comment to "Note that this term was reinstated from obsolete"
    #   TODO: no we remove the previous comment?  (all comments?)
    # 4. Remove any replaced_by and consider tags
    # 5. Remove the owl:deprecated: true tag

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> "
    prefix += "PREFIX obo: <http://purl.obolibrary.org/obo/> "
    prefix += "PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> "

    deleteQuery = about + " rdfs:label ?label . "
    deleteQuery += about + ' owl:deprecated "true"^^xsd:boolean . '
    deleteQuery += about + " obo:IAO_0000115 ?unobsolete_definition . "
    deleteQuery += about + " obo:IAO_0100001 ?replacedBy .  "
    deleteQuery += about + " oboInOwl:consider ?consider . "
    deleteQuery += about + " rdfs:subClassOf oboInOwl:ObsoleteClass . "

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = about + " rdfs:label ?unobsolete_label . "
    insertQuery += about + " obo:IAO_0000115 ?unobsolete_definition . "
    insertQuery += (
        '?entity rdfs:comment "Note that this term was reinstated from obsolete." . '
    )

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = "{ " + about + " rdfs:label ?label . "
    whereQuery += 'BIND(IF(STRSTARTS(?label, "obsolete "),'
    whereQuery += "SUBSTR(?label,10),?label) AS ?unobsolete_label ) } "
    whereQuery += " UNION "
    whereQuery += "{ " + about + " rdfs:label ?label . "
    whereQuery += about + " obo:IAO_0000115 ?definition . "
    whereQuery += 'BIND(IF(STRSTARTS(?definition, "OBSOLETE "),'
    whereQuery += "SUBSTR(?definition,10),?definition) AS ?unobsolete_definition ) } "
    whereQuery += " UNION "
    whereQuery += "{ " + about + " rdfs:label ?label . "
    whereQuery += about + " obo:IAO_0100001 ?replacedBy . } "
    whereQuery += " UNION "
    whereQuery += "{ " + about + " rdfs:label ?label . "
    whereQuery += about + " oboInOwl:consider ?consider . } "

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def unobsolete_by_label(kgclInstance):
    about = kgclInstance.about_node
    # http://wiki.geneontology.org/index.php/Restoring_an_Obsolete_Ontology_Term
    # 1. remove 'obsolete' from label
    # 2. remove 'OBSOLETE' from definition
    # 3. update comment to "Note that this term was reinstated from obsolete"
    #   TODO: no we remove the previous comment?  (all comments?)
    # 4. Remove any replaced_by and consider tags
    # 5. Remove the owl:deprecated: true tag

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> "
    prefix += "PREFIX obo: <http://purl.obolibrary.org/obo/> "
    prefix += "PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> "

    deleteQuery = " ?about rdfs:label ?label . "
    deleteQuery += ' ?about owl:deprecated "true"^^xsd:boolean . '
    deleteQuery += " ?about obo:IAO_0000115 ?unobsolete_definition . "
    deleteQuery += " ?about obo:IAO_0100001 ?replacedBy .  "
    deleteQuery += " ?about oboInOwl:consider ?consider . "
    deleteQuery += " ?about rdfs:subClassOf oboInOwl:ObsoleteClass . "

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = "?about rdfs:label ?unobsolete_label . "
    insertQuery += "?about obo:IAO_0000115 ?unobsolete_definition . "
    insertQuery += (
        '?entity rdfs:comment "Note that this term was reinstated from obsolete." . '
    )

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = "{ ?about rdfs:label ?label . "
    whereQuery += ' FILTER(STR(?label)="' + about + '") '
    whereQuery += 'BIND(IF(STRSTARTS(?label, "obsolete "),'
    whereQuery += "SUBSTR(?label,10),?label) AS ?unobsolete_label ) } "
    whereQuery += " UNION "
    whereQuery += "{ ?about rdfs:label ?label . "
    whereQuery += ' FILTER(STR(?label)="' + about + '") '
    whereQuery += "?about obo:IAO_0000115 ?definition . "
    whereQuery += 'BIND(IF(STRSTARTS(?definition, "OBSOLETE "),'
    whereQuery += "SUBSTR(?definition,10),?definition) AS ?unobsolete_definition ) } "
    whereQuery += " UNION "
    whereQuery += "{ ?about rdfs:label ?label . "
    whereQuery += ' FILTER(STR(?label)="' + about + '") '
    whereQuery += "?about obo:IAO_0100001 ?replacedBy . } "
    whereQuery += " UNION "
    whereQuery += "{ ?about rdfs:label ?label . "
    whereQuery += ' FILTER(STR(?label)="' + about + '") '
    whereQuery += "?about oboInOwl:consider ?consider . } "

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def unobsolete_curie(kgclInstance):
    about = kgclInstance.about_node
    # http://wiki.geneontology.org/index.php/Restoring_an_Obsolete_Ontology_Term
    # 1. remove 'obsolete' from label
    # 2. remove 'OBSOLETE' from definition
    # 3. update comment to "Note that this term was reinstated from obsolete"
    #   TODO: no we remove the previous comment?  (all comments?)
    # 4. Remove any replaced_by and consider tags
    # 5. Remove the owl:deprecated: true tag

    curie_prefix = get_prefix(about)
    curie_uri = prefix_2_uri[curie_prefix]

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> "
    prefix += "PREFIX obo: <http://purl.obolibrary.org/obo/> "
    prefix += "PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> "
    prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    deleteQuery = about + " rdfs:label ?label . "
    deleteQuery += about + ' owl:deprecated "true"^^xsd:boolean . '
    deleteQuery += about + " obo:IAO_0000115 ?unobsolete_definition . "
    deleteQuery += about + " obo:IAO_0100001 ?replacedBy .  "
    deleteQuery += about + " oboInOwl:consider ?consider . "
    deleteQuery += about + " rdfs:subClassOf oboInOwl:ObsoleteClass . "

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = about + " rdfs:label ?unobsolete_label . "
    insertQuery += about + " obo:IAO_0000115 ?unobsolete_definition . "
    insertQuery += (
        '?entity rdfs:comment "Note that this term was reinstated from obsolete." . '
    )

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = "{ " + about + " rdfs:label ?label . "
    whereQuery += 'BIND(IF(STRSTARTS(?label, "obsolete "),'
    whereQuery += "SUBSTR(?label,10),?label) AS ?unobsolete_label ) } "
    whereQuery += " UNION "
    whereQuery += "{ " + about + " rdfs:label ?label . "
    whereQuery += about + " obo:IAO_0000115 ?definition . "
    whereQuery += 'BIND(IF(STRSTARTS(?definition, "OBSOLETE "),'
    whereQuery += "SUBSTR(?definition,10),?definition) AS ?unobsolete_definition ) } "
    whereQuery += " UNION "
    whereQuery += "{ " + about + " rdfs:label ?label . "
    whereQuery += about + " obo:IAO_0100001 ?replacedBy . } "
    whereQuery += " UNION "
    whereQuery += "{ " + about + " rdfs:label ?label . "
    whereQuery += about + " oboInOwl:consider ?consider . } "

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


# NB this does not preserve language tags
def rename(kgclInstance):
    oldValue = kgclInstance.old_value
    newValue = kgclInstance.new_value

    # strip label's single quotes
    oldValue = oldValue.replace("'", "")
    newValue = newValue.replace("'", "")

    old_language = kgclInstance.old_language
    new_language = kgclInstance.new_language

    if kgclInstance.about_node is None:
        subject = "?entity"
    else:
        subject = kgclInstance.about_node

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"
    deleteQuery = subject + " rdfs:label ?oldlabel ."
    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = subject + " rdfs:label ?newlabel ."
    insert = "INSERT {" + insertQuery + "}"

    whereQuery = subject + " rdfs:label ?label .  "
    whereQuery += ' FILTER(STR(?label)="' + oldValue + '") '

    if old_language is None:
        whereQuery += ' BIND("' + oldValue + '" AS ?oldlabel) '
    else:
        whereQuery += ' FILTER(LANG(?label) ="' + old_language + '")'
        whereQuery += (
            ' BIND( STRLANG("' + oldValue + '","' + old_language + '") AS ?oldlabel) '
        )

    if new_language is None:
        whereQuery += ' BIND("' + newValue + '" AS ?newlabel) '
    else:
        whereQuery += (
            ' BIND( STRLANG("' + newValue + '","' + new_language + '") AS ?newlabel) '
        )

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


# TODO: this implementation is buggy
# this implementation should preserve language tags
# note that this cannot be used for diffing
def rename_preserve(kgclInstance):
    oldValue = kgclInstance.old_value
    newValue = kgclInstance.new_value
    oldValue = oldValue.replace("'", "")
    old_language = kgclInstance.old_language
    new_language = kgclInstance.new_language

    # initialise subject
    if kgclInstance.about_node is None:
        subject = "?entity"
    else:
        subject = kgclInstance.about_node

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"
    deleteQuery = subject + " rdfs:label ?tag ."
    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = subject + " rdfs:label ?tag ."
    insert = "INSERT {" + insertQuery + "}"

    whereQuery = subject + " rdfs:label ?label .  "
    whereQuery += " BIND( LANG(?label) AS ?language)  "
    whereQuery += ' FILTER(STR(?label)="' + oldValue + '") '

    # if old_Language tag is specified
    # then, we need to filter results according to the specified language tag
    if old_language is not None:
        whereQuery += ' FILTER(LANG(?label) ="' + old_language + '")'

    # if new_language tag is specifed, then
    # we need to add this tag to insert query
    if new_language is None:
        whereQuery += " BIND( STRLANG(" + newValue + ",?language) AS ?tag) "
    else:
        whereQuery += (
            " BIND( STRLANG(" + newValue + ',"' + new_language + '") AS ?tag) '
        )

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def delete_by_id(kgclInstance):
    about = kgclInstance.about_node  # this needs to be an ID - not a label

    deleteQuery = (
        "?s1 ?p1 " + about + " . "
    )  # this does not delete triples with blank nodes
    deleteQuery += "?s2 " + about + " ?o1 . "
    deleteQuery += "?s2 " + about + " ?o1 . "
    deleteQuery += about + " ?p2 ?o2 . "

    delete = "DELETE {" + deleteQuery + "}"

    whereQuery = "{ ?s1 ?p1 " + about + " . } "
    whereQuery += " UNION "
    whereQuery = "{ ?s2 " + about + " ?o1 . } "
    whereQuery += " UNION "
    whereQuery += "{ " + about + " ?p2 ?o2 . } "

    where = "WHERE {" + whereQuery + "}"

    updateQuery = delete + " " + where

    return updateQuery


def delete_curie(kgclInstance):
    about = kgclInstance.about_node

    curie_prefix = get_prefix(about)
    curie_uri = prefix_2_uri[curie_prefix]
    prefix = "PREFIX " + curie_prefix + ": " + curie_uri + " "

    # this does not delete triples with blank nodes
    deleteQuery = "?s1 ?p1 " + about + " . "
    deleteQuery += "?s2 " + about + " ?o1 . "
    deleteQuery += about + " ?p2 ?o2 . "

    delete = "DELETE {" + deleteQuery + "}"

    whereQuery = "{ ?s1 ?p1 " + about + " . } "
    whereQuery += " UNION "
    whereQuery = "{ ?s2 " + about + " ?o1 . } "
    whereQuery += " UNION "
    whereQuery += "{ " + about + " ?p2 ?o2 . } "

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + where

    return updateQuery


def delete_by_label(kgclInstance):
    about = kgclInstance.about_node
    # about = about.replace("'", "")  # remove single quotes from label input

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"

    deleteQuery = "?s1 rdfs:label ?label . "
    deleteQuery += "?s1 ?p2 ?o1 . "

    delete = "DELETE {" + deleteQuery + "}"

    whereQuery = "?s1 rdfs:label ?label . "
    whereQuery += "?s1 ?p2 ?o1 . "
    whereQuery += ' FILTER(STR(?label)="' + about + '") '  # ignore language tags

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + where

    return updateQuery


def create_class(kgclInstance):
    termId = kgclInstance.node_id

    prefix = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    insertQuery = termId + " rdf:type owl:Class  . "
    insert = "INSERT {" + insertQuery + "}"
    where = "WHERE {}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def create_node(kgclInstance):
    termId = kgclInstance.node_id
    label = kgclInstance.name
    language = kgclInstance.language

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "

    if language is None:
        insertQuery = termId + " rdfs:label " + label + "  . "
    else:
        insertQuery = termId + " rdfs:label ?tag  . "

    insert = "INSERT {" + insertQuery + "}"

    if language is None:
        where = "WHERE {}"
    else:
        whereQuery = " BIND( STRLANG(" + label + ',"' + language + '") AS ?tag) '
        where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def edge_annotation_creation(kgclInstance):
    subject = kgclInstance.subject
    predicate = kgclInstance.predicate
    object = kgclInstance.object
    annotation = kgclInstance.annotation_set

    prefix = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "

    insertQuery = "?bnode owl:annotatedSource " + subject + " . "
    insertQuery += "?bnode owl:annotatedProperty " + predicate + " . "
    insertQuery += "?bnode owl:annotatedTarget " + object + " . "
    insertQuery += "?bnode " + annotation.property + " " + annotation.filler + " . "
    insertQuery += "?bnode rdf:type owl:Axiom ."
    insert = "INSERT {" + insertQuery + "}"

    whereQuery = ' BIND(BNODE("reification") AS ?bnode) '
    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def edge_creation(kgclInstance):
    subject = kgclInstance.subject
    predicate = kgclInstance.predicate
    object = kgclInstance.object

    subject_type = kgclInstance.subject_type
    predicate_type = kgclInstance.predicate_type
    object_type = kgclInstance.object_type

    language = kgclInstance.language
    datatype = kgclInstance.datatype  # TODO: currently only accepting full IRIs

    prefix = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "

    if subject_type == "curie":
        curie_prefix = get_prefix(subject)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    if predicate_type == "curie":
        curie_prefix = get_prefix(predicate)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    if object_type == "curie":
        curie_prefix = get_prefix(object)
        curie_uri = prefix_2_uri[curie_prefix]
        prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    insertQuery = "?subject " + predicate + " ?object . "

    insert = "INSERT {" + insertQuery + "}"

    # TODO this needs to be reworked
    # currently language tags are ignored if an entity is specified via a label
    whereQuery = ""
    if subject_type == "label":
        whereQuery += "?subject rdfs:label ?object_label . "
        whereQuery += ' FILTER(STR(?object_label)="' + subject + '") '
    else:
        whereQuery += "BIND(" + subject + " AS ?subject)"

    if object_type == "label":
        whereQuery += "?object rdfs:label ?object_label . "
        whereQuery += ' FILTER(STR(?object_label)="' + object + '") '
    else:  # curie or uri
        if datatype is not None:
            whereQuery += " BIND( STRDT(" + object + "," + datatype + ") AS ?object) "
        elif language is not None:
            whereQuery += (
                "BIND( STRLANG(" + object + ',"' + language + '") AS ?object) '
            )
        else:
            whereQuery += "BIND(" + object + " AS ?object)"

    where = "WHERE { " + whereQuery + " }"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def edge_annotation_deletion(kgclInstance):
    subject = kgclInstance.subject
    predicate = kgclInstance.predicate
    object = kgclInstance.object
    annotation = kgclInstance.annotation_set

    # NB: we need to distinguish between two cases
    # (a) the entire reification needs to be deleted
    # (b) only one annotation triple is deleted
    #     while the reification is not because it's
    #     needed for other annotations

    # TODO: example

    # Query for (a)
    # A reification for a single annotations will consist of 5 triples.
    # So, we use this size bound to determine whether we need to
    # delete the entire reification or not
    prefix = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "

    insert = "INSERT { }"

    deleteQuery = "?bnode owl:annotatedSource " + subject + " . "
    deleteQuery += "?bnode owl:annotatedProperty " + predicate + " . "
    deleteQuery += "?bnode owl:annotatedTarget " + object + " . "
    deleteQuery += "?bnode " + annotation.property + " " + annotation.filler + " . "
    deleteQuery += "?bnode rdf:type owl:Axiom ."

    delete = "DELETE {" + deleteQuery + "}"

    whereQuery = "SELECT ?bnode WHERE { "
    whereQuery += "?bnode ?ap ?p ."
    whereQuery += "?bnode owl:annotatedSource " + subject + " . } "
    whereQuery += "HAVING((COUNT(?ap) <= 5) && (COUNT(?p) <= 5))"

    where = "WHERE {" + whereQuery + "}"

    subquery1 = prefix + " " + delete + " " + insert + " " + where

    # Query for (b)
    deleteQuery = "?bnode " + annotation.property + " " + annotation.filler + " . "
    delete = "DELETE {" + deleteQuery + "}"

    whereQuery = "SELECT ?bnode WHERE {"
    whereQuery += "?bnode ?ap ?p ."
    whereQuery += "?bnode owl:annotatedSource " + subject + " . } "
    whereQuery += "HAVING((COUNT(?ap) > 5) || (COUNT(?ap) > 5))"

    where = "WHERE {" + whereQuery + "}"

    subquery2 = prefix + " " + delete + " " + insert + " " + where

    # putting (a) and (b) together
    updateQuery = subquery1 + " ; " + subquery2

    return updateQuery


def edge_deletion(kgclInstance):
    subject = kgclInstance.subject
    predicate = kgclInstance.predicate
    object = kgclInstance.object

    language = kgclInstance.language
    datatype = kgclInstance.datatype

    prefix = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "

    deleteQuery = subject + " " + predicate + " ?object . "
    delete = "DELETE {" + deleteQuery + "}"

    whereQuery = deleteQuery

    if datatype is not None:
        whereQuery += " BIND( STRDT(" + object + "," + datatype + ") AS ?object) "
    elif language is not None:
        whereQuery += "BIND( STRLANG(" + object + ',"' + language + '") AS ?object) '
    else:
        whereQuery += "BIND(" + object + " AS ?object)"

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + where

    return updateQuery


def obsolete_by_id(kgclInstance):
    about = kgclInstance.about_node
    replacement = kgclInstance.has_direct_replacement

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "
    prefix += "PREFIX obo: <http://purl.obolibrary.org/obo/> "
    prefix += "PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> "

    deleteQuery = about + "rdfs:label ?label . "
    deleteQuery += about + " rdfs:subClassOf ?superclass . "
    deleteQuery += about + " owl:equivalentClass ?rhs . "
    deleteQuery += "?lhs owl:equivalentClass " + about + " ."

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = "?entity rdfs:label ?tag . "
    insertQuery += about + ' owl:deprecated "true"^^xsd:boolean . '
    insertQuery += "?entity rdfs:subClassOf oboInOwl:ObsoleteClass . "

    if kgclInstance.has_direct_replacement is not None:
        insertQuery += about + " obo:IAO_0100001 " + replacement + "  .  "

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = "{ " + about + " rdfs:subClassOf ?superclass . } "
    whereQuery += " UNION "
    whereQuery += "{ " + about + " owl:equivalentClass ?rhs . } "
    whereQuery += " UNION "
    whereQuery += "{ ?lhs owl:equivalentClass " + about + " . } "
    whereQuery += " UNION "
    whereQuery += "{ ?entity rdfs:label ?label . "
    whereQuery += ' BIND(CONCAT("obsolete ", ?label) AS ?obsolete_label )  '
    whereQuery += " BIND( LANG(?label) AS ?language)  "
    whereQuery += " BIND( STRLANG(?obsolete_label,?language) AS ?tag) }  "

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def obsolete_by_label(kgclInstance):
    about = kgclInstance.about_node

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "
    prefix += "PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> "

    deleteQuery = "?entity rdfs:label ?label . "
    deleteQuery += "?entity rdfs:subClassOf ?superclass . "
    deleteQuery += "?entity owl:equivalentClass ?rhs . "
    deleteQuery += "?lhs owl:equivalentClass ?entity . "

    delete = "DELETE {" + deleteQuery + "}"

    # inner_label = about.replace("'", "")
    obsolete_label = "obsolete " + about

    insertQuery = "?entity rdfs:label ?tag . "
    insertQuery += '?entity owl:deprecated "true"^^xsd:boolean . '
    insertQuery += "?entity rdfs:subClassOf oboInOwl:ObsoleteClass . "

    insert = "INSERT {" + insertQuery + "}"

    # TODO: handle the special case where only a label is present
    # (in that case we need to query for a single triple)
    whereQuery = "{ ?entity rdfs:label ?label .  "
    whereQuery += " ?entity rdfs:subClassOf ?superclass .  "
    whereQuery += " BIND( LANG(?label) AS ?language)  "
    whereQuery += ' BIND( STRLANG("' + obsolete_label + '",?language) AS ?tag)  '
    whereQuery += ' FILTER(STR(?label)="' + about + '") } '

    whereQuery += " UNION "

    whereQuery += "{ ?entity rdfs:label ?label .  "
    whereQuery += " ?entity owl:equivalentClass ?rhs . "
    whereQuery += " BIND( LANG(?label) AS ?language) "
    whereQuery += ' BIND( STRLANG("' + obsolete_label + '",?language) AS ?tag)  '
    whereQuery += ' FILTER(STR(?label)="' + about + '") } '

    whereQuery += " UNION "

    whereQuery += "{ ?entity rdfs:label ?label .  "
    whereQuery += " ?lhs owl:equivalentClass ?entity . "
    whereQuery += " BIND( LANG(?label) AS ?language) "
    whereQuery += ' BIND( STRLANG("' + obsolete_label + '",?language) AS ?tag)  '
    whereQuery += ' FILTER(STR(?label)="' + about + '") } '

    whereQuery += " UNION "

    whereQuery += "{ ?entity rdfs:label ?label .  "
    whereQuery += " ?entity rdf:type ?type .  "
    whereQuery += " BIND( LANG(?label) AS ?language) "
    whereQuery += ' BIND( STRLANG("' + obsolete_label + '",?language) AS ?tag)  '
    whereQuery += ' FILTER(STR(?label)="' + about + '") } '

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def obsolete_curie(kgclInstance):
    about = kgclInstance.about_node
    replacement = kgclInstance.has_direct_replacement

    curie_prefix = get_prefix(about)
    curie_uri = prefix_2_uri[curie_prefix]

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "
    prefix += "PREFIX obo: <http://purl.obolibrary.org/obo/> "
    prefix += "PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> "
    prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    deleteQuery = about + " rdfs:label ?label . "
    deleteQuery += about + " rdfs:subClassOf ?superclass . "
    deleteQuery += about + " owl:equivalentClass ?rhs . "
    deleteQuery += "?lhs owl:equivalentClass " + about + " ."

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = "?entity rdfs:label ?tag . "
    insertQuery += about + ' owl:deprecated "true"^^xsd:boolean . '
    insertQuery += "?entity rdfs:subClassOf oboInOwl:ObsoleteClass . "

    if kgclInstance.has_direct_replacement is not None:
        insertQuery += about + " obo:IAO_0100001 " + replacement + "  .  "

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = "{ " + about + " rdfs:subClassOf ?superclass . } "
    whereQuery += " UNION "
    whereQuery += "{ " + about + " owl:equivalentClass ?rhs . } "
    whereQuery += " UNION "
    whereQuery += "{ ?lhs owl:equivalentClass " + about + " . } "
    whereQuery += " UNION "
    whereQuery += "{ ?entity rdfs:label ?label . "
    whereQuery += ' BIND(CONCAT("obsolete ", ?label) AS ?obsolete_label )  '
    whereQuery += " BIND( LANG(?label) AS ?language)  "
    whereQuery += " BIND( STRLANG(?obsolete_label,?language) AS ?tag) }  "

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def new_synonym_for_uri(kgclInstance):
    about = kgclInstance.about_node
    synonym = kgclInstance.new_value
    language = kgclInstance.language
    qualifier = kgclInstance.qualifier

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "
    prefix += "PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> "

    if qualifier is None:
        insertQuery = about + " oboInOwl:hasSynonym "  # + synonym + " . "
    if qualifier == "exact":
        insertQuery = about + " oboInOwl:hasExactSynonym "  # + synonym + " . "
    if qualifier == "narrow":
        insertQuery = about + " oboInOwl:hasNarrowSynonym "  # + synonym + " . "
    if qualifier == "broad":
        insertQuery = about + " oboInOwl:hasBroadSynonym "  # + synonym + " . "
    if qualifier == "related":
        insertQuery = about + " oboInOwl:hasRelatedSynonym "  # + synonym + " . "

    if language is None:
        whereQuery = ""
        insertQuery += synonym + " ."
    else:
        insertQuery += "?tag ."
        whereQuery = " BIND( STRLANG(" + synonym + ',"' + language + '") AS ?tag) '

    insert = "INSERT {" + insertQuery + "}"
    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def new_synonym_for_label(kgclInstance):
    about = kgclInstance.about_node  # this is a label for a node
    synonym = kgclInstance.new_value
    language = kgclInstance.language
    qualifier = kgclInstance.qualifier

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "
    prefix += "PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> "

    if qualifier is None:
        insertQuery = "?about oboInOwl:hasSynonym "  # + synonym + " . "
    if qualifier == "exact":
        insertQuery = "?about oboInOwl:hasExactSynonym "  # + synonym + " . "
    if qualifier == "narrow":
        insertQuery = "?about oboInOwl:hasNarrowSynonym "  # + synonym + " . "
    if qualifier == "broad":
        insertQuery = "?about oboInOwl:hasBroadSynonym "  # + synonym + " . "
    if qualifier == "related":
        insertQuery = "?about oboInOwl:hasRelatedSynonym "  # + synonym + " . "

    # this ignores language tags
    whereQuery = " ?about rdfs:label ?label . "
    whereQuery += ' FILTER(STR(?label)="' + about + '") '

    if language is None:
        insertQuery += synonym + " ."
    else:
        insertQuery += "?tag ."
        whereQuery += " BIND( STRLANG(" + synonym + ',"' + language + '") AS ?tag) '

    insert = "INSERT {" + insertQuery + "}"
    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def new_synonym_for_curie(kgclInstance):
    about = kgclInstance.about_node  # this is a curie
    synonym = kgclInstance.new_value
    language = kgclInstance.language
    qualifier = kgclInstance.qualifier

    curie_prefix = get_prefix(about)
    curie_uri = prefix_2_uri[curie_prefix]

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "
    prefix += "PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> "
    prefix += "PREFIX " + curie_prefix + ": " + curie_uri + " "

    if qualifier is None:
        insertQuery = about + " oboInOwl:hasSynonym "  # + synonym + " . "
    if qualifier == "exact":
        insertQuery = about + " oboInOwl:hasExactSynonym "  # + synonym + " . "
    if qualifier == "narrow":
        insertQuery = about + " oboInOwl:hasNarrowSynonym "  # + synonym + " . "
    if qualifier == "broad":
        insertQuery = about + " oboInOwl:hasBroadSynonym "  # + synonym + " . "
    if qualifier == "related":
        insertQuery = about + " oboInOwl:hasRelatedSynonym "  # + synonym + " . "

    if language is None:
        whereQuery = ""
        insertQuery += synonym + " ."
    else:
        insertQuery += "?tag ."
        whereQuery += " BIND( STRLANG(" + synonym + ',"' + language + '") AS ?tag) '

    insert = "INSERT {" + insertQuery + "}"
    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def create_existential_restriction(kgclInstance):
    subclass = kgclInstance.subclass
    property = kgclInstance.property
    filler = kgclInstance.filler

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "
    prefix += "PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> "

    insertQuery = subclass + "rdfs:subClassOf ?bnode . "
    insertQuery += "?bnode owl:someValuesFrom " + filler + " . "
    insertQuery += "?bnode owl:onProperty " + property + " . "
    insertQuery += "?bnode rdf:type owl:Restriction ."

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = ' BIND(BNODE("existential") AS ?bnode) '
    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def delete_existential_restriction(kgclInstance):
    subclass = kgclInstance.subclass
    property = kgclInstance.property
    filler = kgclInstance.filler

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "
    prefix += "PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> "

    deleteQuery = subclass + "rdfs:subClassOf ?bnode . "
    deleteQuery += "?bnode owl:someValuesFrom " + filler + " . "
    deleteQuery += "?bnode owl:onProperty " + property + " . "
    deleteQuery += "?bnode rdf:type owl:Restriction ."

    delete = "DELETE {" + deleteQuery + "}"

    whereQuery = deleteQuery
    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + where

    return updateQuery
