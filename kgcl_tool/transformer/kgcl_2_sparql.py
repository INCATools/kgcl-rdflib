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
)


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
    # TODO: new model only allows to obsolete a node
    if type(kgclInstance) is NodeObsoletion:
        if is_label(kgclInstance.about_node):
            return obsolete_by_label(kgclInstance)
        if is_id(kgclInstance.about_node):
            return obsolete_by_id(kgclInstance)
        # TODO: error handling

    # node obsoletion
    if type(kgclInstance) is NodeUnobsoletion:
        if is_id(kgclInstance.about_node):
            return unobsolete(kgclInstance)
        # TODO: error handling

    # node deletion
    if type(kgclInstance) is NodeDeletion:
        if is_id(kgclInstance.about_node):
            return delete_by_id(kgclInstance)
        if is_label(kgclInstance.about_node):
            return delete_by_label(kgclInstance)
        # TODO: error handling

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
        if (
            is_id(kgclInstance.about_edge.subject)
            and is_id(kgclInstance.old_value)
            and is_id(kgclInstance.new_value)
        ):
            return node_deepening(kgclInstance)

    # node shallowing
    if type(kgclInstance) is NodeShallowing:
        if (
            is_id(kgclInstance.about_edge.subject)
            and is_id(kgclInstance.old_value)
            and is_id(kgclInstance.new_value)
        ):
            return node_shallowing(kgclInstance)

    # edge creation
    if type(kgclInstance) is EdgeCreation:
        if (
            is_id(kgclInstance.subject)
            and is_id(kgclInstance.predicate)
            and (is_id(kgclInstance.object) or is_label(kgclInstance.object))
        ):
            if kgclInstance.annotation_set is None:
                return edge_creation(kgclInstance)
            else:
                return edge_annotation_creation(kgclInstance)

    # edge deletion
    if type(kgclInstance) is EdgeDeletion:
        if (
            is_id(kgclInstance.subject)
            and is_id(kgclInstance.predicate)
            and (is_id(kgclInstance.object) or is_label(kgclInstance.object))
        ):
            return edge_deletion(kgclInstance)

    # node move
    if type(kgclInstance) is NodeMove:
        if (
            is_id(kgclInstance.about_edge.subject)
            and is_id(kgclInstance.old_value)
            and is_id(kgclInstance.new_value)
        ):
            return node_move(kgclInstance)

    if type(kgclInstance) is NewSynonym:
        if is_id(kgclInstance.about_node) and is_label(kgclInstance.new_value):
            return new_synonym(kgclInstance)

    if type(kgclInstance) is PredicateChange:
        if (
            is_id(kgclInstance.about_edge.subject)
            and is_id(kgclInstance.about_edge.object)
            and is_id(kgclInstance.old_value)
            and is_id(kgclInstance.new_value)
        ):
            return change_predicate(kgclInstance)

    if type(kgclInstance) is RemovedNodeFromSubset:
        if is_id(kgclInstance.about_node) and is_id(kgclInstance.subset):
            return remove_node_from_subset(kgclInstance)


def node_move(kgclInstance):
    term_id = kgclInstance.about_edge.subject
    old_value = kgclInstance.old_value
    new_value = kgclInstance.new_value

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "

    deleteQuery = term_id + " ?relation " + old_value + " . "

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = term_id + " ?relation " + new_value + " . "

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = term_id + " ?relation " + old_value + " . "
    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def remove_node_from_subset(kgclInstance):

    about = kgclInstance.about_node
    subset = kgclInstance.subset

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX obo: <http://purl.obolibrary.org/obo/> "

    deleteQuery = about + " obo:inSubset " + subset + " . "

    delete = "DELETE {" + deleteQuery + "}"

    whereQuery = about + " obo:inSubset " + subset + " . "

    where = "WHERE { " + whereQuery + " }"

    updateQuery = prefix + " " + delete + " " + where

    return updateQuery


def change_predicate(kgclInstance):

    subject = kgclInstance.about_edge.subject
    object = kgclInstance.about_edge.object

    old_value = kgclInstance.old_value
    new_value = kgclInstance.new_value

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "

    deleteQuery = subject + " " + old_value + " " + object + " . "

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = subject + " " + new_value + " " + object + " . "

    insert = "INSERT {" + insertQuery + "}"

    where = "WHERE {}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def node_deepening(kgclInstance):

    term_id = kgclInstance.about_edge.subject
    old_value = kgclInstance.old_value
    new_value = kgclInstance.new_value

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "

    deleteQuery = term_id + " ?relation " + old_value + " . "

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = term_id + " ?relation " + new_value + " . "

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = term_id + " ?relation " + old_value + " . "
    whereQuery += new_value + " ?relation " + old_value + " . "
    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def node_shallowing(kgclInstance):

    term_id = kgclInstance.about_edge.subject
    old_value = kgclInstance.old_value
    new_value = kgclInstance.new_value

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "

    deleteQuery = term_id + " ?relation " + old_value + " . "

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = term_id + " ?relation " + new_value + " . "

    insert = "INSERT {" + insertQuery + "}"

    whereQuery = term_id + " ?relation " + old_value + " . "
    whereQuery += old_value + " ?relation " + new_value + " . "
    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


# TODO: handling of language tags
# look things up at https://www.ebi.ac.uk/ols/ontologies/iao
def unobsolete(kgclInstance):
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


def rename(kgclInstance):
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

    # this changes only the label of an entity
    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"
    deleteQuery = subject + " rdfs:label ?label ."
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


def delete_by_label(kgclInstance):
    about = kgclInstance.about_node
    about = about.replace("'", "")  # remove single quotes from label input

    deleteQuery = "?s1 ?p1 ?label . "
    deleteQuery += "?s1 ?p2 ?o1 . "

    delete = "DELETE {" + deleteQuery + "}"

    whereQuery = "?s1 ?p1 ?label . "
    whereQuery += "?s1 ?p2 ?o1 . "
    whereQuery += ' FILTER(STR(?label)="' + about + '") '  # ignore language tags

    where = "WHERE {" + whereQuery + "}"

    updateQuery = delete + " " + where

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

    whereQuery = ' BIND(BNODE("what") AS ?bnode) '
    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def edge_creation(kgclInstance):
    subject = kgclInstance.subject
    predicate = kgclInstance.predicate
    object = kgclInstance.object

    prefix = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "

    insertQuery = subject + " " + predicate + " " + object + " . "
    insert = "INSERT {" + insertQuery + "}"

    where = "WHERE {}"

    updateQuery = prefix + " " + insert + " " + where

    return updateQuery


def edge_deletion(kgclInstance):
    subject = kgclInstance.subject
    predicate = kgclInstance.predicate
    object = kgclInstance.object

    prefix = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "

    deleteQuery = subject + " " + predicate + " " + object + " . "
    delete = "DELETE {" + deleteQuery + "}"

    where = "WHERE {" + deleteQuery + "}"

    updateQuery = prefix + " " + delete + " " + where

    return updateQuery


def obsolete_by_id(kgclInstance):
    about = kgclInstance.about_node
    replacement = kgclInstance.has_direct_replacement

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> "
    prefix += "PREFIX obo: <http://purl.obolibrary.org/obo/> "

    deleteQuery = about + "rdfs:label ?label . "
    deleteQuery += about + " rdfs:subClassOf ?superclass . "
    deleteQuery += about + " owl:equivalentClass ?rhs . "
    deleteQuery += "?lhs owl:equivalentClass " + about + " ."

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = "?entity rdfs:label ?tag . "
    insertQuery += about + ' owl:deprecated "true"^^xsd:boolean . '
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

    deleteQuery = "?entity rdfs:label ?label . "
    deleteQuery += "?entity rdfs:subClassOf ?superclass . "
    deleteQuery += "?entity owl:equivalentClass ?rhs . "
    deleteQuery += "?lhs owl:equivalentClass ?entity . "

    delete = "DELETE {" + deleteQuery + "}"

    inner_label = about.replace("'", "")
    obsolete_label = "obsolete " + inner_label

    insertQuery = "?entity rdfs:label ?tag . "
    insertQuery += '?entity owl:deprecated "true"^^xsd:boolean . '

    insert = "INSERT {" + insertQuery + "}"

    # TODO: handle the special case where only a label is present
    # (in that case we need to query for a single triple)
    whereQuery = "{ ?entity rdfs:label ?label .  "
    whereQuery += " ?entity rdfs:subClassOf ?superclass .  "
    whereQuery += " BIND( LANG(?label) AS ?language)  "
    whereQuery += ' BIND( STRLANG("' + obsolete_label + '",?language) AS ?tag)  '
    whereQuery += ' FILTER(STR(?label)="' + inner_label + '") } '

    whereQuery += " UNION "

    whereQuery += "{ ?entity rdfs:label ?label .  "
    whereQuery += " ?entity owl:equivalentClass ?rhs . "
    whereQuery += " BIND( LANG(?label) AS ?language) "
    whereQuery += ' BIND( STRLANG("' + obsolete_label + '",?language) AS ?tag)  '
    whereQuery += ' FILTER(STR(?label)="' + inner_label + '") } '

    whereQuery += " UNION "

    whereQuery += "{ ?entity rdfs:label ?label .  "
    whereQuery += " ?lhs owl:equivalentClass ?entity . "
    whereQuery += " BIND( LANG(?label) AS ?language) "
    whereQuery += ' BIND( STRLANG("' + obsolete_label + '",?language) AS ?tag)  '
    whereQuery += ' FILTER(STR(?label)="' + inner_label + '") } '

    whereQuery += " UNION "

    whereQuery += "{ ?entity rdfs:label ?label .  "
    whereQuery += " ?entity rdf:type ?type .  "
    whereQuery += " BIND( LANG(?label) AS ?language) "
    whereQuery += ' BIND( STRLANG("' + obsolete_label + '",?language) AS ?tag)  '
    whereQuery += ' FILTER(STR(?label)="' + inner_label + '") } '

    where = "WHERE {" + whereQuery + "}"

    updateQuery = prefix + " " + delete + " " + insert + " " + where

    return updateQuery


def new_synonym(kgclInstance):
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
