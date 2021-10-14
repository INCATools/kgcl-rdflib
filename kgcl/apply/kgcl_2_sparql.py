import re
from kgcl.model.kgcl import (
    NodeRename,
    NodeObsoletion,
    NodeUnobsoletion,
    NodeDeletion,
    NodeMove,
    NodeDeepening,
    NodeShallowing,
    NodeAnnotationChange,
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


def get_prefix(curie):
    return curie.split(":")[0]


# TODO; JSON LD obo context look at robot
prefix_2_uri = {
    "obo": "<http://purl.obolibrary.org/obo/>",
    "ex": "<http://example.org/>",
    "oboInOwl": "<http://www.geneontology.org/formats/oboInOwl#>",
    "rdfs": "<http://www.w3.org/2000/01/rdf-schema#>",
    "xsd": "<http://www.w3.org/2001/XMLSchema#>",
    "rdf": "<http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
    "owl": "<http://www.w3.org/2002/07/owl#>",
    "swrl": "<http://www.w3.org/2003/11/swrl#>",
    "oio": "<http://www.geneontology.org/formats/oboInOwl#>",
    "dce": "<http://purl.org/dc/elements/1.1/>",
    "dct": "<http://purl.org/dc/terms/>",
    "foaf": "<http://xmlns.com/foaf/0.1/>",
    "protege": "<http://protege.stanford.edu/plugins/owl/protege#>",
    "BFO": "<http://purl.obolibrary.org/obo/BFO_>",
    "CHEBI": "<http://purl.obolibrary.org/obo/CHEBI_>",
    "CL": "<http://purl.obolibrary.org/obo/CL_>",
    "IAO": "<http://purl.obolibrary.org/obo/IAO_>",
    "NCBITaxon": "<http://purl.obolibrary.org/obo/NCBITaxon_>",
    "OBI": "<http://purl.obolibrary.org/obo/OBI_>",
    "PR": "<http://purl.obolibrary.org/obo/PR_>",
    "obo": "<http://purl.obolibrary.org/obo/>",
    "UP": "<http://purl.uniprot.org/uniprot/>",
    "UC": "<http://purl.uniprot.org/core/>",
    "PRO": "<http://www.uniprot.org/annotation/PRO_>",
    "faldo": "<http://biohackathon.org/resource/faldo#>",
    # TODO add more prefixes
}


def is_label(input):
    return re.match(r"\'[^ \s\'].*\'", input)


def is_id(input):
    return re.match(r"<\S+>", input)


def build_curie_prefix(entity):
    curie_prefix = get_prefix(entity)
    curie_uri = prefix_2_uri[curie_prefix]
    return "PREFIX " + curie_prefix + ": " + curie_uri + " "


# TODO proper escape handling
def escape_literal(literal):
    return literal.replace("\\", "\\\\").replace('"', '\\"')
    # .replace("\\'", "\\\\'")


def convert(kgcl_instance):
    """Given a KGCL dataclass,
    return a SPARQL UPDATE query corresponding to the encoded change.
    """

    # label renaming
    if type(kgcl_instance) is NodeRename:
        return rename(kgcl_instance)

    # node obsoletion
    if type(kgcl_instance) is NodeObsoletion:
        representation = kgcl_instance.about_node_representation
        if representation == "uri":
            return obsolete_by_id(kgcl_instance)
        if representation == "label":
            return obsolete_by_label(kgcl_instance)
        if representation == "curie":
            return obsolete_curie(kgcl_instance)

    # node obsoletion
    if type(kgcl_instance) is NodeUnobsoletion:
        representation = kgcl_instance.about_node_representation
        if representation == "uri":
            return unobsolete_by_id(kgcl_instance)
        if representation == "label":
            return unobsolete_by_label(kgcl_instance)
        if representation == "curie":
            return unobsolete_curie(kgcl_instance)

    # node deletion
    if type(kgcl_instance) is NodeDeletion:
        representation = kgcl_instance.about_node_representation
        if representation == "uri":
            return delete_by_id(kgcl_instance)
        if representation == "label":
            return delete_by_label(kgcl_instance)
        if representation == "curie":
            return delete_curie(kgcl_instance)

    # node creation
    if type(kgcl_instance) is NodeCreation:
        return create_node(kgcl_instance)

    # class creation
    if type(kgcl_instance) is ClassCreation:
        return create_class(kgcl_instance)

    # node deepending
    if type(kgcl_instance) is NodeDeepening:
        return node_deepening(kgcl_instance)

    # node shallowing
    if type(kgcl_instance) is NodeShallowing:
        return node_shallowing(kgcl_instance)

    if type(kgcl_instance) is NodeAnnotationChange:
        return node_annotation_change(kgcl_instance)

    # node move
    if type(kgcl_instance) is NodeMove:
        return node_move(kgcl_instance)

    if type(kgcl_instance) is NewSynonym:
        representation = kgcl_instance.about_node_representation

        if representation == "uri":
            return new_synonym_for_uri(kgcl_instance)
        if representation == "label":
            return new_synonym_for_label(kgcl_instance)
        if representation == "curie":
            return new_synonym_for_curie(kgcl_instance)

    if type(kgcl_instance) is PredicateChange:
        return change_predicate(kgcl_instance)

    if type(kgcl_instance) is RemovedNodeFromSubset:
        if is_id(kgcl_instance.about_node) and is_id(kgcl_instance.subset):
            return remove_node_from_subset(kgcl_instance)

    if type(kgcl_instance) is PlaceUnder:
        return triple_creation(kgcl_instance)

    if type(kgcl_instance) is RemoveUnder:
        return triple_deletion(kgcl_instance)

    if type(kgcl_instance) is EdgeCreation:
        return create_existential_restriction(kgcl_instance)

    if type(kgcl_instance) is EdgeDeletion:
        return delete_existential_restriction(kgcl_instance)


def node_move(kgcl_instance):

    # NB: object and old_value are the (necessarily) the same
    subject = kgcl_instance.about_edge.subject
    predicate = kgcl_instance.about_edge.predicate
    object = kgcl_instance.about_edge.object

    subject_type = kgcl_instance.about_edge.subject_representation
    predicate_type = kgcl_instance.about_edge.predicate_representation
    object_type = kgcl_instance.about_edge.object_representation

    old_value = kgcl_instance.old_value
    new_value = kgcl_instance.new_value

    old_type = kgcl_instance.old_object_type
    new_type = kgcl_instance.new_object_type

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "

    # set up prefixes  for curies as needed
    if subject_type == "curie":
        prefix += build_curie_prefix(subject)

    if predicate_type == "curie":
        prefix += build_curie_prefix(predicate)

    if object_type == "curie":
        prefix += build_curie_prefix(object)

    if old_type == "curie":
        prefix += build_curie_prefix(old_value)

    if new_type == "curie":
        prefix += build_curie_prefix(new_value)

    deleteQuery = "?subject ?predicate ?old . "

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = "?subject ?predicate ?new . "

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

    if predicate_type == "label":
        whereQuery += "?predicate rdfs:label ?predicate_label . "
        whereQuery += ' FILTER(STR(?predicate_label)="' + predicate + '") '
    else:
        whereQuery += " BIND(" + predicate + " AS ?predicate) "

    whereQuery += "?subject ?predicate ?old . "

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def remove_node_from_subset(kgcl_instance):

    about = kgcl_instance.about_node
    subset = kgcl_instance.subset

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


def change_predicate(kgcl_instance):

    subject = kgcl_instance.about_edge.subject
    object = kgcl_instance.about_edge.object

    old_value = kgcl_instance.old_value
    new_value = kgcl_instance.new_value

    language = kgcl_instance.language
    datatype = kgcl_instance.datatype

    subject_type = kgcl_instance.about_edge.subject_representation
    object_type = kgcl_instance.about_edge.object_representation

    old_value_type = kgcl_instance.old_value_type
    new_value_type = kgcl_instance.new_value_type

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "

    if subject_type == "curie":
        prefix += build_curie_prefix(subject)

    if object_type == "curie":
        prefix += build_curie_prefix(object)

    if old_value_type == "curie":
        prefix += build_curie_prefix(old_value)

    if new_value_type == "curie":
        prefix += build_curie_prefix(new_value)

    deleteQuery = "?subject ?old ?object . "

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = "?subject ?new ?object . "

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = deleteQuery

    if subject_type == "label":
        whereQuery += "?subject rdfs:label ?subject_label . "
        whereQuery += ' FILTER(STR(?subject_label)="' + subject + '") '

    if subject_type == "uri" or subject_type == "curie":
        whereQuery += " BIND(" + subject + " AS ?subject) "

    if object_type == "label":
        whereQuery += "?object rdfs:label ?object_label . "
        whereQuery += ' FILTER(STR(?object_label)="' + object + '") '

    if object_type == "uri" or object_type == "curie":
        whereQuery += " BIND(" + object + " AS ?object) "

    if object_type == "literal":
        object = escape_literal(object)
        if datatype is not None:
            # TODO: accept CURIES for data types
            whereQuery += ' BIND( STRDT("' + object + '",' + datatype + ") AS ?object) "
        elif language is not None:
            whereQuery += (
                'BIND( STRLANG("' + object + '","' + language + '") AS ?object) '
            )
        else:
            whereQuery += 'BIND("' + object + '" AS ?object)'

    if new_value_type == "label":
        whereQuery += "?new rdfs:label ?new_label . "
        whereQuery += ' FILTER(STR(?new_label)="' + new_value + '") '
    else:
        whereQuery += " BIND(" + new_value + " AS ?new) "

    if old_value_type == "label":
        whereQuery += "?old rdfs:label ?old_label . "
        whereQuery += ' FILTER(STR(?old_label)="' + old_value + '") '
    else:
        whereQuery += " BIND(" + old_value + " AS ?old) "

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def node_deepening(kgcl_instance):

    entity = kgcl_instance.about_edge.subject
    old_value = kgcl_instance.old_value
    new_value = kgcl_instance.new_value

    entity_type = kgcl_instance.about_edge.subject_representation
    old_type = kgcl_instance.old_object_type
    new_type = kgcl_instance.new_object_type

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "

    # set up prefixes  for curies as needed
    if entity_type == "curie":
        prefix += build_curie_prefix(entity)

    if old_type == "curie":
        prefix += build_curie_prefix(old_value)

    if new_type == "curie":
        prefix += build_curie_prefix(new_value)

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


def node_shallowing(kgcl_instance):

    entity = kgcl_instance.about_edge.subject
    old_value = kgcl_instance.old_value
    new_value = kgcl_instance.new_value

    entity_type = kgcl_instance.about_edge.subject_representation
    old_type = kgcl_instance.old_object_type
    new_type = kgcl_instance.new_object_type

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "

    if entity_type == "curie":
        prefix += build_curie_prefix(entity)

    if old_type == "curie":
        prefix += build_curie_prefix(old_value)

    if new_type == "curie":
        prefix += build_curie_prefix(new_value)

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
def unobsolete_by_id(kgcl_instance):
    about = kgcl_instance.about_node
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


def unobsolete_by_label(kgcl_instance):
    about = kgcl_instance.about_node
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


def unobsolete_curie(kgcl_instance):
    about = kgcl_instance.about_node
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
def rename(kgcl_instance):
    oldValue = kgcl_instance.old_value
    newValue = kgcl_instance.new_value

    # strip label's single quotes
    oldValue = oldValue[1:-1]
    newValue = newValue[1:-1]

    old_language = kgcl_instance.old_language
    new_language = kgcl_instance.new_language

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"

    if kgcl_instance.about_node is None:
        subject = "?entity"
    else:
        subject = kgcl_instance.about_node
        if kgcl_instance.about_node_representation == "curie":
            prefix += build_curie_prefix(subject)

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
def rename_preserve(kgcl_instance):
    oldValue = kgcl_instance.old_value
    newValue = kgcl_instance.new_value
    oldValue = oldValue.replace("'", "")
    old_language = kgcl_instance.old_language
    new_language = kgcl_instance.new_language

    # initialise subject
    if kgcl_instance.about_node is None:
        subject = "?entity"
    else:
        subject = kgcl_instance.about_node

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


def delete_by_id(kgcl_instance):
    about = kgcl_instance.about_node  # this needs to be an ID - not a label

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


def delete_curie(kgcl_instance):
    about = kgcl_instance.about_node

    prefix = build_curie_prefix(about)

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


def delete_by_label(kgcl_instance):
    about = kgcl_instance.about_node

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


def create_class(kgcl_instance):
    termId = kgcl_instance.node_id
    id_type = kgcl_instance.about_node_representation

    prefix = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "

    if id_type == "curie":
        prefix += build_curie_prefix(termId)

    insertQuery = termId + " rdf:type owl:Class  . "
    insert = "INSERT {" + insertQuery + "}"
    where = "WHERE {}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def create_node(kgcl_instance):
    termId = kgcl_instance.node_id
    label = kgcl_instance.name
    language = kgcl_instance.language
    id_type = kgcl_instance.about_node_representation

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "

    if id_type == "curie":
        prefix += build_curie_prefix(termId)

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


def node_annotation_change(kgcl_instance):
    subject = kgcl_instance.about_node
    predicate = kgcl_instance.annotation_property
    old_object = kgcl_instance.old_value
    new_object = kgcl_instance.new_value

    subject_type = kgcl_instance.about_node_representation
    predicate_type = kgcl_instance.annotation_property_type
    old_type = kgcl_instance.old_value_type
    new_type = kgcl_instance.new_value_type

    # TODO: allow language tags and datattypes for
    # both the old and new annotation value
    old_language = kgcl_instance.old_language
    new_language = kgcl_instance.new_language
    old_datatype = kgcl_instance.old_datatype
    new_datatype = kgcl_instance.new_datatype

    prefix = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "

    if subject_type == "curie":
        prefix += build_curie_prefix(subject)

    if predicate_type == "curie":
        prefix += build_curie_prefix(predicate)

    if old_type == "curie":
        prefix += build_curie_prefix(old_object)

    if new_type == "curie":
        prefix += build_curie_prefix(new_object)

        # todo: delete query
    deleteQuery = "?subject ?predicate ?old_object . "

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = "?subject ?predicate ?new_object . "

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = ""
    if subject_type == "label":
        whereQuery += "?subject rdfs:label ?subject_label . "
        whereQuery += ' FILTER(STR(?subject_label)="' + subject + '") '
    else:
        whereQuery += " BIND(" + subject + " AS ?subject)"

    if predicate_type == "label":
        whereQuery += "?predicate rdfs:label ?predicate_label . "
        whereQuery += ' FILTER(STR(?predicate_label)="' + predicate + '") '
    else:
        whereQuery += "?predicate rdf:type owl:AnnotationProperty . "
        whereQuery += " BIND(" + predicate + " AS ?predicate)"

    if old_type == "label":
        whereQuery += "?old_object rdfs:label ?old_object_label . "
        whereQuery += ' FILTER(STR(?old_object_label)="' + old_object + '") '

    if old_type == "uri" or old_type == "curie":
        whereQuery += " BIND(" + old_object + " AS ?old_object) "

    if old_type == "literal":
        old_object = escape_literal(old_object)
        if old_datatype is not None:
            whereQuery += (
                ' BIND(STRDT("'
                + old_object
                + '",'
                + old_datatype
                + ") AS ?old_object) "
            )
        elif old_language is not None:
            whereQuery += (
                ' BIND(STRLANG("'
                + old_object
                + '","'
                + old_language
                + '") AS ?old_object) '
            )
        else:
            whereQuery += ' BIND("' + old_object + '" AS ?old_object)'

    if new_type == "label":
        whereQuery += "?new_object rdfs:label ?new_object_label . "
        whereQuery += ' FILTER(STR(?new_object_label)="' + new_object + '") '

    if new_type == "uri" or old_type == "curie":
        whereQuery += " BIND(" + new_object + " AS ?new_object) "

    if new_type == "literal":
        new_object = escape_literal(new_object)
        if new_datatype is not None:
            whereQuery += (
                ' BIND(STRDT("'
                + new_object
                + '",'
                + new_datatype
                + ") AS ?new_object) "
            )
        elif new_language is not None:
            whereQuery += (
                ' BIND(STRLANG("'
                + new_object
                + '","'
                + new_language
                + '") AS ?new_object) '
            )
        else:
            whereQuery += ' BIND("' + new_object + '" AS ?new_object)'

    where = "WHERE { " + whereQuery + " }"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def edge_annotation_creation(kgcl_instance):
    subject = kgcl_instance.subject
    predicate = kgcl_instance.predicate
    object = kgcl_instance.object

    subject_type = kgcl_instance.subject_type
    predicate_type = kgcl_instance.predicate_type
    object_type = kgcl_instance.object_type

    annotation = kgcl_instance.annotation_set

    # annotation.property_type
    # annotation.filler_type

    prefix = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "

    if subject_type == "curie":
        prefix += build_curie_prefix(subject)

    if predicate_type == "curie":
        prefix += build_curie_prefix(predicate)

    if object_type == "curie":
        prefix += build_curie_prefix(object)

    if annotation.property_type == "curie":
        prefix += build_curie_prefix(annotation.property)

    if annotation.filler_type == "curie":
        prefix += build_curie_prefix(annotation.filler)

    insertQuery = "?bnode owl:annotatedSource ?subject . "
    insertQuery += "?bnode owl:annotatedProperty ?predicate . "
    insertQuery += "?bnode owl:annotatedTarget ?object . "
    insertQuery += "?bnode ?annotation_property ?filler . "
    insertQuery += "?bnode rdf:type owl:Axiom ."
    insert = "INSERT {" + insertQuery + "}"

    whereQuery = ' BIND(BNODE("reification") AS ?bnode) '
    if subject_type == "label":
        whereQuery += "?subject rdfs:label ?subject_label . "
        whereQuery += ' FILTER(STR(?subject_label)="' + subject + '") '
    else:
        whereQuery += "BIND(" + subject + " AS ?subject) "

    if predicate_type == "label":
        whereQuery += "?predicate rdfs:label ?predicate_label . "
        whereQuery += ' FILTER(STR(?predicate_label)="' + predicate + '") '
    else:
        whereQuery += "BIND(" + predicate + " AS ?predicate) "

    if annotation.property_type == "label":
        whereQuery += "?annotation_property rdfs:label ?ap_label . "
        whereQuery += ' FILTER(STR(?ap_label)="' + annotation.property + '") '
    else:
        whereQuery += "BIND(" + annotation.property + " AS ?annotation_property) "

    if annotation.filler_type == "label":
        whereQuery += "?filler rdfs:label ?filler_label . "
        whereQuery += ' FILTER(STR(?filler_label)="' + annotation.filler + '") '

    if annotation.filler_type == "literal":
        whereQuery += 'BIND("' + escape_literal(annotation.filler) + '" AS ?filler) '

    if annotation.filler_type == "uri" or annotation.filler_type == "curie":
        whereQuery += "BIND(" + annotation.filler + " AS ?filler) "

    if object_type == "label":
        whereQuery += "?object rdfs:label ?object_label . "
        whereQuery += ' FILTER(STR(?object_label)="' + object + '") '

    if object_type == "literal":
        whereQuery += 'BIND("' + escape_literal(object) + '" AS ?object) '

    if object_type == "uri" or object_type == "curie":
        whereQuery += "BIND(" + object + " AS ?object) "

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def triple_creation(kgcl_instance):
    subject = kgcl_instance.subject
    predicate = kgcl_instance.predicate
    object = kgcl_instance.object

    subject_type = kgcl_instance.subject_type
    predicate_type = kgcl_instance.predicate_type
    object_type = kgcl_instance.object_type

    language = kgcl_instance.language
    datatype = kgcl_instance.datatype  # TODO: currently only accepting full IRIs

    prefix = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "

    if subject_type == "curie":
        prefix += build_curie_prefix(subject)

    if predicate_type == "curie":
        prefix += build_curie_prefix(predicate)

    if object_type == "curie":
        prefix += build_curie_prefix(object)

    insertQuery = "?subject ?predicate ?object . "

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = ""
    if subject_type == "label":
        whereQuery += "?subject rdfs:label ?subject_label . "
        whereQuery += ' FILTER(STR(?subject_label)="' + subject + '") '
    else:
        whereQuery += " BIND(" + subject + " AS ?subject)"

    if predicate_type == "label":
        whereQuery += "?predicate rdfs:label ?predicate_label . "
        whereQuery += ' FILTER(STR(?predicate_label)="' + predicate + '") '
    else:
        whereQuery += " BIND(" + predicate + " AS ?predicate)"

    if object_type == "label":
        whereQuery += "?object rdfs:label ?object_label . "
        whereQuery += ' FILTER(STR(?object_label)="' + object + '") '

    if object_type == "uri" or object_type == "curie":
        whereQuery += " BIND(" + object + " AS ?object) "

    if object_type == "literal":
        object = escape_literal(object)
        if datatype is not None:
            whereQuery += ' BIND(STRDT("' + object + '",' + datatype + ") AS ?object) "
        elif language is not None:
            whereQuery += (
                ' BIND(STRLANG("' + object + '","' + language + '") AS ?object) '
            )
        else:
            whereQuery += ' BIND("' + object + '" AS ?object)'

    where = "WHERE { " + whereQuery + " }"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


# TODO: language tags + data types
def edge_annotation_deletion(kgcl_instance):
    subject = kgcl_instance.subject
    predicate = kgcl_instance.predicate
    object = kgcl_instance.object

    subject_type = kgcl_instance.subject_type
    predicate_type = kgcl_instance.predicate_type
    object_type = kgcl_instance.object_type

    annotation = kgcl_instance.annotation_set

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

    if subject_type == "curie":
        prefix += build_curie_prefix(subject)

    if predicate_type == "curie":
        prefix += build_curie_prefix(predicate)

    if object_type == "curie":
        prefix += build_curie_prefix(object)

    if annotation.property_type == "curie":
        prefix += build_curie_prefix(annotation.property)

    if annotation.filler_type == "curie":
        prefix += build_curie_prefix(annotation.filler)

    insert = "INSERT { }"

    deleteQuery = "?bnode owl:annotatedSource ?subject  . "
    deleteQuery += "?bnode owl:annotatedProperty ?predicate . "
    deleteQuery += "?bnode owl:annotatedTarget ?object . "
    deleteQuery += "?bnode ?annotation_property ?filler . "
    deleteQuery += "?bnode rdf:type owl:Axiom ."

    delete = "DELETE {" + deleteQuery + "}"

    whereQuery = "SELECT ?bnode ?subject ?predicate ?object ?filler ?annotation_property WHERE { "
    whereQuery += "?bnode ?ap ?p . "
    whereQuery += "?bnode owl:annotatedSource ?subject .  "

    if subject_type == "label":
        whereQuery += "?subject rdfs:label ?subject_label . "
        whereQuery += ' FILTER(STR(?subject_label)="' + subject + '") '
    else:
        whereQuery += "BIND(" + subject + " AS ?subject) "

    if annotation.property_type == "label":
        whereQuery += "?annotation_property rdfs:label ?ap_label . "
        whereQuery += ' FILTER(STR(?ap_label)="' + annotation.property + '") '
    else:
        whereQuery += "BIND(" + annotation.property + " AS ?annotation_property) "

    if predicate_type == "label":
        whereQuery += "?predicate rdfs:label ?predicate_label . "
        whereQuery += ' FILTER(STR(?predicate_label)="' + predicate + '") '
    else:
        whereQuery += "BIND(" + predicate + " AS ?predicate) "

    if annotation.filler_type == "label":
        whereQuery += "?filler rdfs:label ?filler_label . "
        whereQuery += ' FILTER(STR(?filler_label)="' + annotation.filler + '") '

    if annotation.filler_type == "uri" or annotation.filler_type == "curie":
        whereQuery += "BIND(" + annotation.filler + " AS ?filler) "

    if annotation.filler_type == "literal":
        whereQuery += 'BIND("' + escape_literal(annotation.filler) + '" AS ?filler) '

    if object_type == "label":
        whereQuery += "?object rdfs:label ?object_label . "
        whereQuery += ' FILTER(STR(?object_label)="' + object + '") '

    if object_type == "literal":
        whereQuery += 'BIND("' + escape_literal(object) + '" AS ?object) '

    if object_type == "uri" or object_type == "curie":
        whereQuery += "BIND(" + object + " AS ?object)  "

    whereQuery += "} "
    whereQuery += "HAVING((COUNT(?ap) <= 5) && (COUNT(?p) <= 5)) "

    where = "WHERE {" + whereQuery + "}"

    subquery1 = prefix + " " + delete + " " + insert + " " + where

    # Query for (b)
    deleteQuery = "?bnode ?annotation_property ?filler . "
    delete = "DELETE {" + deleteQuery + "}"

    whereQuery = "SELECT ?bnode ?subject ?object ?annotation_property ?filler WHERE {"
    whereQuery += "?bnode ?ap ?p . "
    whereQuery += "?bnode owl:annotatedSource ?subject .  "

    if subject_type == "label":
        whereQuery += "?subject rdfs:label ?subject_label . "
        whereQuery += ' FILTER(STR(?subject_label)="' + subject + '") '
    else:
        whereQuery += "BIND(" + subject + " AS ?subject) "

    if annotation.property_type == "label":
        whereQuery += "?annotation_property rdfs:label ?ap_label . "
        whereQuery += ' FILTER(STR(?ap_label)="' + annotation.property + '") '
    else:
        whereQuery += "BIND(" + annotation.property + " AS ?annotation_property) "

    if annotation.filler_type == "label":
        whereQuery += "?filler rdfs:label ?filler_label . "
        whereQuery += ' FILTER(STR(?filler_label)="' + annotation.filler + '") '

    if annotation.filler_type == "uri" or annotation.filler_type == "curie":
        whereQuery += "BIND(" + annotation.filler + " AS ?filler) "
    if annotation.filler_type == "literal":
        whereQuery += 'BIND("' + escape_literal(annotation.filler) + '" AS ?filler) '

    if object_type == "label":
        whereQuery += "?object rdfs:label ?object_label . "
        whereQuery += ' FILTER(STR(?object_label)="' + object + '") '

    if object_type == "literal":
        whereQuery += 'BIND("' + escape_literal(object) + '" AS ?object) '

    if object_type == "uri" or object_type == "curie":
        whereQuery += "BIND(" + object + " AS ?object)  "

    whereQuery += "} "
    whereQuery += "HAVING((COUNT(?ap) > 5) || (COUNT(?ap) > 5)) "

    where = "WHERE {" + whereQuery + "}"

    subquery2 = prefix + " " + delete + " " + insert + " " + where

    # putting (a) and (b) together
    updateQuery = subquery1 + " ; " + subquery2

    return updateQuery


def triple_deletion(kgcl_instance):
    subject = kgcl_instance.subject
    predicate = kgcl_instance.predicate
    object = kgcl_instance.object

    subject_type = kgcl_instance.subject_type
    predicate_type = kgcl_instance.predicate_type
    object_type = kgcl_instance.object_type

    language = kgcl_instance.language
    datatype = kgcl_instance.datatype

    prefix = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "

    if subject_type == "curie":
        prefix += build_curie_prefix(subject)

    if predicate_type == "curie":
        prefix += build_curie_prefix(predicate)

    if object_type == "curie":
        prefix += build_curie_prefix(object)

    deleteQuery = "?subject ?predicate ?object . "
    delete = "DELETE {" + deleteQuery + "}"

    whereQuery = ""

    whereQuery = ""
    if subject_type == "label":
        whereQuery += "?subject rdfs:label ?object_label . "
        whereQuery += ' FILTER(STR(?object_label)="' + subject + '") '
    else:
        whereQuery += "BIND(" + subject + " AS ?subject)"

    if predicate_type == "label":
        whereQuery += "?predicate rdfs:label ?predicate_label . "
        whereQuery += ' FILTER(STR(?predicate_label)="' + predicate + '") '
    else:
        whereQuery += "BIND(" + predicate + " AS ?predicate)"

    if object_type == "label":
        whereQuery += "?object rdfs:label ?object_label . "
        whereQuery += ' FILTER(STR(?object_label)="' + object + '") '

    if object_type == "uri" or object_type == "curie":
        whereQuery += " BIND(" + object + " AS ?object) "

    if object_type == "literal":
        object = escape_literal(object)
        if datatype is not None:
            whereQuery += ' BIND( STRDT("' + object + '",' + datatype + ") AS ?object) "
        elif language is not None:
            whereQuery += (
                'BIND( STRLANG("' + object + '","' + language + '") AS ?object) '
            )
        else:
            whereQuery += 'BIND("' + object + '" AS ?object)'

    where = "WHERE { " + whereQuery + " }"

    updateQuery = prefix + " " + delete + " " + where

    return updateQuery


def obsolete_by_id(kgcl_instance):
    about = kgcl_instance.about_node
    replacement = kgcl_instance.has_direct_replacement

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

    if kgcl_instance.has_direct_replacement is not None:
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


def obsolete_by_label(kgcl_instance):
    about = kgcl_instance.about_node

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


def obsolete_curie(kgcl_instance):
    about = kgcl_instance.about_node
    replacement = kgcl_instance.has_direct_replacement

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

    if kgcl_instance.has_direct_replacement is not None:
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


def new_synonym_for_uri(kgcl_instance):

    about = kgcl_instance.about_node
    synonym = kgcl_instance.new_value
    language = kgcl_instance.language
    qualifier = kgcl_instance.qualifier

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

    whereQuery = ""
    if language is None:
        insertQuery += '"' + synonym + '" .'
    else:
        insertQuery += "?tag ."
        whereQuery = ' BIND( STRLANG("' + synonym + '","' + language + '") AS ?tag) '

    insert = "INSERT {" + insertQuery + "}"
    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def new_synonym_for_label(kgcl_instance):
    about = kgcl_instance.about_node  # this is a label for a node
    synonym = kgcl_instance.new_value
    language = kgcl_instance.language
    qualifier = kgcl_instance.qualifier

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
        insertQuery += '"' + synonym + '" .'
    else:
        insertQuery += "?tag ."
        whereQuery += ' BIND( STRLANG("' + synonym + '","' + language + '") AS ?tag) '

    insert = "INSERT {" + insertQuery + "}"
    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def new_synonym_for_curie(kgcl_instance):
    about = kgcl_instance.about_node  # this is a curie
    synonym = kgcl_instance.new_value
    language = kgcl_instance.language
    qualifier = kgcl_instance.qualifier

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

    whereQuery = ""
    if language is None:
        insertQuery += '"' + synonym + '" .'
    else:
        insertQuery += "?tag ."
        whereQuery += ' BIND( STRLANG("' + synonym + '","' + language + '") AS ?tag) '

    insert = "INSERT {" + insertQuery + "}"
    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def create_existential_restriction(kgcl_instance):
    subclass = kgcl_instance.subject
    property = kgcl_instance.predicate
    filler = kgcl_instance.object

    subclass_type = kgcl_instance.subject_type
    property_type = kgcl_instance.predicate_type
    filler_type = kgcl_instance.object_type

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "

    if subclass_type == "curie":
        prefix += build_curie_prefix(subclass)
    if property_type == "curie":
        prefix += build_curie_prefix(property)
    if filler_type == "curie":
        prefix += build_curie_prefix(filler)

    insertQuery = "?subclass rdfs:subClassOf ?bnode . "
    insertQuery += "?bnode owl:someValuesFrom ?filler . "
    insertQuery += "?bnode owl:onProperty ?property . "
    insertQuery += "?bnode rdf:type owl:Restriction ."

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = ""
    if subclass_type == "label":
        whereQuery += "?subclass rdfs:label ?subclass_label . "
        whereQuery += ' FILTER(STR(?subclass_label)="' + subclass + '") '
    else:
        whereQuery += " BIND(" + subclass + " AS ?subclass) "

    if property_type == "label":
        whereQuery += "?property rdfs:label ?property_label . "
        whereQuery += ' FILTER(STR(?property_label)="' + property + '") '
    else:
        whereQuery += " BIND(" + property + " AS ?property) "

    if filler_type == "label":
        whereQuery += "?filler rdfs:label ?filler_label . "
        whereQuery += ' FILTER(STR(?filler_label)="' + filler + '") '
    else:
        whereQuery += " BIND(" + filler + " AS ?filler) "

    whereQuery += ' BIND(BNODE("existential") AS ?bnode) '
    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def delete_existential_restriction(kgcl_instance):
    subclass = kgcl_instance.subject
    property = kgcl_instance.predicate
    filler = kgcl_instance.object

    subclass_type = kgcl_instance.subject_type
    property_type = kgcl_instance.predicate_type
    filler_type = kgcl_instance.object_type

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "
    prefix += "PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> "

    if subclass_type == "curie":
        prefix += build_curie_prefix(subclass)
    if property_type == "curie":
        prefix += build_curie_prefix(property)
    if filler_type == "curie":
        prefix += build_curie_prefix(filler)

    deleteQuery = "?subclass rdfs:subClassOf ?bnode . "
    deleteQuery += "?bnode owl:someValuesFrom ?filler . "
    deleteQuery += "?bnode owl:onProperty ?property . "
    deleteQuery += "?bnode rdf:type owl:Restriction ."

    delete = "DELETE {" + deleteQuery + "}"

    whereQuery = deleteQuery

    if subclass_type == "label":
        whereQuery += "?subclass rdfs:label ?subclass_label . "
        whereQuery += ' FILTER(STR(?subclass_label)="' + subclass + '") '
    else:
        whereQuery += " BIND(" + subclass + " AS ?subclass) "

    if property_type == "label":
        whereQuery += "?property rdfs:label ?property_label . "
        whereQuery += ' FILTER(STR(?property_label)="' + property + '") '
    else:
        whereQuery += " BIND(" + property + " AS ?property) "

    if filler_type == "label":
        whereQuery += "?filler rdfs:label ?filler_label . "
        whereQuery += ' FILTER(STR(?filler_label)="' + filler + '") '
    else:
        whereQuery += " BIND(" + filler + " AS ?filler) "

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + where

    return updateQuery
