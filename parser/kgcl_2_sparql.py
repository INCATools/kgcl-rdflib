import sys
sys.path.append("../")
import python.kgcl
import re

def is_label(input):
    return re.match('\'[^ \s\'].*\'', input)

def is_id(input):
    return re.match('<\S+>', input)

def convert(kgclInstance):

    #label renaming
    #TODO: case for "rename 'old' from 'id' to 'new'
    if(type(kgclInstance) is python.kgcl.NodeRename):
        if(is_label(kgclInstance.old_value) and is_label(kgclInstance.new_value)): 
            return rename(kgclInstance)
        #TODO: error handling

    #node obsoletion
    #TODO: new model only allows to obsolete a node (which is an 'id' and not a 'label'
    if(type(kgclInstance) is python.kgcl.NodeObsoletion):
        if(is_label(kgclInstance.about_node)):
            return obsolete_by_label(kgclInstance)
        if(is_id(kgclInstance.about_node)):
            return obsolete_by_id(kgclInstance)
        #TODO: error handling

    #node obsoletion
    if(type(kgclInstance) is python.kgcl.NodeUnobsoletion):
        if(is_id(kgclInstance.about_node)):
            return unobsolete(kgclInstance)
        #TODO: error handling

    #node deletion
    if(type(kgclInstance) is python.kgcl.NodeDeletion):
        if(is_id(kgclInstance.about_node)):
            return delete_by_id(kgclInstance)
        if(is_label(kgclInstance.about_node)):
            return delete_by_label(kgclInstance)
        #TODO: error handling

    #node creation
    if(type(kgclInstance) is python.kgcl.NodeCreation):
        if(is_id(kgclInstance.node_id) and is_label(kgclInstance.name)):
            return create_node(kgclInstance)

    #class creation
    if(type(kgclInstance) is python.kgcl.ClassCreation):
        if(is_id(kgclInstance.node_id)):
            return create_class(kgclInstance)

    #node deepending
    if(type(kgclInstance) is python.kgcl.NodeDeepening):
        if(is_id(kgclInstance.about_edge.subject) and is_id(kgclInstance.old_value) and is_id(kgclInstance.new_value)):
            return node_deepening(kgclInstance)

    #node shallowing
    if(type(kgclInstance) is python.kgcl.NodeShallowing):
        if(is_id(kgclInstance.about_edge.subject) and is_id(kgclInstance.old_value) and is_id(kgclInstance.new_value)):
            return node_shallowing(kgclInstance)

    #edge creation
    if(type(kgclInstance) is python.kgcl.EdgeCreation):
        if(is_id(kgclInstance.subject) and is_id(kgclInstance.predicate) and (is_id(kgclInstance.object) or is_label(kgclInstance.object))):
            return edge_creation(kgclInstance)

    #edge deletion
    if(type(kgclInstance) is python.kgcl.EdgeDeletion):
        if(is_id(kgclInstance.subject) and is_id(kgclInstance.predicate) and (is_id(kgclInstance.object) or is_label(kgclInstance.object))):
            return edge_deletion(kgclInstance)

    #node move
    if(type(kgclInstance) is python.kgcl.NodeMove): 
        if(is_id(kgclInstance.about_edge.subject) and is_id(kgclInstance.old_value) and is_id(kgclInstance.new_value)):
            return node_move(kgclInstance)

    if(type(kgclInstance) is python.kgcl.NewSynonym): 
        if(is_id(kgclInstance.about_node) and is_label(kgclInstance.new_value)):
            return new_synonym(kgclInstance)

    if(type(kgclInstance) is python.kgcl.PredicateChange): 
        if(is_id(kgclInstance.about_edge.subject) and is_id(kgclInstance.about_edge.object) and is_id(kgclInstance.old_value) and is_id(kgclInstance.new_value)):
            return change_predicate(kgclInstance)

    if(type(kgclInstance) is python.kgcl.RemovedNodeFromSubset): 
        if(is_id(kgclInstance.about_node) and is_id(kgclInstance.subset)):
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

    whereQuery =  term_id + " ?relation " + old_value + " . " 
    where = "WHERE {" + whereQuery + "}"

    updateQuery =  prefix + " " + \
                   delete + " " + \
                   insert + " " + \
                   where

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

    updateQuery =  prefix + " " + \
                   delete + " " + \
                   where

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

    updateQuery =  prefix + " " + \
                   delete + " " + \
                   insert + " " + \
                   where

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

    whereQuery =  term_id + " ?relation " + old_value + " . " 
    whereQuery +=  new_value + " ?relation " + old_value + " . " 
    where = "WHERE {" + whereQuery + "}"

    updateQuery =  prefix + " " + \
                   delete + " " + \
                   insert + " " + \
                   where

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

    whereQuery =  term_id + " ?relation " + old_value + " . " 
    whereQuery +=  old_value + " ?relation " + new_value + " . " 
    where = "WHERE {" + whereQuery + "}"

    updateQuery =  prefix + " " + \
                   delete + " " + \
                   insert + " " + \
                   where

    return updateQuery 

#look things up at https://www.ebi.ac.uk/ols/ontologies/iao
def unobsolete(kgclInstance):
    about =  kgclInstance.about_node
    #http://wiki.geneontology.org/index.php/Restoring_an_Obsolete_Ontology_Term
    #1. remove 'obsolete' from label
    #2. remove 'OBSOLETE' from definition 
    #3. update comment to "Note that this term was reinstated from obsolete"
    #   TODO: no we remove the previous comment? 
    #4. Remove any replaced_by and consider tags 
    #5. Remove the owl:deprecated: true tag

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> " 
    prefix += "PREFIX obo: <http://purl.obolibrary.org/obo/> "
    prefix += "PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> " 

    deleteQuery = about + " rdfs:label ?label . "
    deleteQuery += about + " owl:deprecated \"true\"^^xsd:boolean . " 
    deleteQuery += about + " obo:IAO_0000115 ?unobsolete_definition . " 
    deleteQuery += about + " obo:IAO_0100001 ?replacedBy .  " 
    deleteQuery += about + " oboInOwl:consider ?consider . " 

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = about + " rdfs:label ?unobsolete_label . " 
    insertQuery += about + " obo:IAO_0000115 ?unobsolete_definition . " 
    insertQuery += "?entity rdfs:comment \"Note that this term was reinstated from obsolete.\" . "

    insert = "INSERT {" + insertQuery + "}" 

    whereQuery = "{ " + about + " rdfs:label ?label . " 
    whereQuery += "BIND(IF(STRSTARTS(?label, \"obsolete \"),SUBSTR(?label,10),?label) AS ?unobsolete_label ) } " 
    whereQuery += " UNION "
    whereQuery += "{ " + about + " rdfs:label ?label . " 
    whereQuery +=        about + " obo:IAO_0000115 ?definition . " 
    whereQuery += "BIND(IF(STRSTARTS(?definition, \"OBSOLETE \"),SUBSTR(?definition,10),?definition) AS ?unobsolete_definition ) } " 
    whereQuery += " UNION "
    whereQuery += "{ " + about + " rdfs:label ?label . " 
    whereQuery +=        about + " obo:IAO_0100001 ?replacedBy . } " 
    whereQuery += " UNION "
    whereQuery += "{ " + about + " rdfs:label ?label . " 
    whereQuery +=        about + " oboInOwl:consider ?consider . } " 


    where = "WHERE {" + whereQuery + "}"

    updateQuery =  prefix + " " + \
                   delete + " " + \
                   insert + " " + \
                   where

    return updateQuery 


def rename(kgclInstance):
    #TODO: do we require the user to specify both the label and an ID?
    #"rename {about} from {old value} to {new value}"?
    oldValue = kgclInstance.old_value
    newValue = kgclInstance.new_value

    #initialise subject
    if(kgclInstance.about_node is None):
        subject = "?entity"
    else:
        subject = kgclInstance.about_node

    #this chances only the label of an entity
    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"
    #deleteQuery = "?entity rdfs:label " + oldValue + " ."
    deleteQuery = subject + " rdfs:label " + oldValue + " ."
    delete = "DELETE {" + deleteQuery + "}"

    #insertQuery = "?entity rdfs:label " + newValue + " ."
    insertQuery = subject + " rdfs:label " + newValue + " ."
    insert = "INSERT {" + insertQuery + "}"

    where = "WHERE {" + deleteQuery + "}"

    updateQuery =  prefix + " " + \
                   delete + " " + \
                   insert + " " + \
                   where

    return updateQuery 

def delete_by_id(kgclInstance):
    about = kgclInstance.about_node #this needs to be an ID - not a label

    deleteQuery = "?s1 ?p1 " + about + " . " #this does not delete triples with blank nodes
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

    updateQuery =  delete + " " + \
                   where

    return updateQuery

def delete_by_label(kgclInstance):
    about = kgclInstance.about_node

    deleteQuery = "?s1 ?p1 " + about + " . "
    deleteQuery += "?s1 ?p2 ?o1 . "

    delete = "DELETE {" + deleteQuery + "}"

    whereQuery = "?s1 ?p1 " + about + " . "
    whereQuery += "?s1 ?p2 ?o1 . "

    where = "WHERE {" + whereQuery + "}"

    updateQuery =  delete + " " + \
                   where

    return updateQuery

def create_class(kgclInstance):
    termId =  kgclInstance.node_id;

    prefix = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    insertQuery = termId + " rdf:type owl:Class  . " 
    insert = "INSERT {" + insertQuery + "}"
    where = "WHERE {}"

    updateQuery =  prefix + " " + \
                   insert + " " + \
                   where

    return updateQuery 

def create_node(kgclInstance):
    termId =  kgclInstance.node_id;
    label = kgclInstance.name;

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    insertQuery = termId + " rdfs:label " + label + "  . " 
    insert = "INSERT {" + insertQuery + "}"
    where = "WHERE {}"

    updateQuery =  prefix + " " + \
                   insert + " " + \
                   where

    return updateQuery 

def edge_creation(kgclInstance):
    subject =  kgclInstance.subject
    predicate =  kgclInstance.predicate
    object =  kgclInstance.object

    prefix = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "

    insertQuery = subject + " " + predicate + " " + object + " . "
    insert = "INSERT {" + insertQuery + "}"

    where = "WHERE {}"

    updateQuery =  prefix + " " + \
                   insert + " " + \
                   where

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

    updateQuery =  prefix + " " + \
                   delete + " " + \
                   where

    return updateQuery 

def obsolete_by_id(kgclInstance):
    about = kgclInstance.about_node
    replacement = kgclInstance.has_direct_replacement 

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> " 
    prefix += "PREFIX obo: <http://purl.obolibrary.org/obo/> "

    deleteQuery = about + "rdfs:label ?label . "
    deleteQuery += about +" rdfs:subClassOf ?superclass . "
    deleteQuery += about +" owl:equivalentClass ?rhs . "
    deleteQuery += "?lhs owl:equivalentClass " + about + " ." 

    delete = "DELETE {" + deleteQuery + "}"

    insertQuery = "?entity rdfs:label ?obsolete_label . " 
    insertQuery += about + " owl:deprecated \"true\"^^xsd:boolean . " 
    if(not kgclInstance.has_direct_replacement is None): 
        insertQuery += about + " obo:IAO_0100001 " + replacement +  "  .  " 

    insert = "INSERT {" + insertQuery + "}" 

    whereQuery = "{ " + about + " rdfs:subClassOf ?superclass . } "
    whereQuery += " UNION "
    whereQuery += "{ " + about + " owl:equivalentClass ?rhs . } "
    whereQuery += " UNION "
    whereQuery += "{ ?lhs owl:equivalentClass " + about + " . } " 
    whereQuery += " UNION "
    whereQuery += "{ ?entity rdfs:label ?label . "
    whereQuery += "BIND(CONCAT(\"obsolete \", ?label) AS ?obsolete_label ) } " 

    where = "WHERE {" + whereQuery + "}"

    updateQuery =  prefix + " " + \
                   delete + " " + \
                   insert + " " + \
                   where

    return updateQuery 



#TODO: This doesn't handle language tags
#since, I canont query for any language tag, 
def obsolete_by_label(kgclInstance): 
    about = kgclInstance.about_node

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> " 

    deleteQuery = "?entity rdfs:label " + about + " . "
    deleteQuery += "?entity rdfs:subClassOf ?superclass . "
    deleteQuery += "?entity owl:equivalentClass ?rhs . "
    deleteQuery += "?lhs owl:equivalentClass ?entity . "

    delete = "DELETE {" + deleteQuery + "}"

    inner_label = about.replace("'","")
    obsolete_label = "'obsolete " + inner_label + "'" 

    insertQuery = "?entity rdfs:label " + obsolete_label + " . "
    insertQuery += "?entity owl:deprecated \"true\"^^xsd:boolean . " 

    insert = "INSERT {" + insertQuery + "}"

    #TODO: handle the special case where only a label is present
    #(in that case we need to query for a single triple)
    whereQuery = "{ ?entity rdfs:label " + about + " .  "
    whereQuery += " ?entity rdfs:subClassOf ?superclass . } "
    whereQuery += " UNION "
    whereQuery += "{ ?entity rdfs:label " + about + " .  "
    whereQuery += " ?entity owl:equivalentClass ?rhs . } "
    whereQuery += " UNION "
    whereQuery += "{ ?entity rdfs:label " + about + " .  "
    whereQuery += " ?lhs owl:equivalentClass ?entity . } " 
    whereQuery += " UNION "
    whereQuery += "{ ?entity rdfs:label " + about + " .  "
    whereQuery += " ?entity rdf:type ?type . } " 

    where = "WHERE {" + whereQuery + "}"

    updateQuery =  prefix + " " + \
                   delete + " " + \
                   insert + " " + \
                   where 

    return updateQuery 

def new_synonym(kgclInstance): 
    about = kgclInstance.about_node
    synonym = kgclInstance.new_value

    prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  "
    prefix += "PREFIX owl: <http://www.w3.org/2002/07/owl#>  "
    prefix += "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#> " 
    prefix += "PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> " 

    #TODO: check whether this way of creating synonyms is OK
    #or whether we want to include qualifiers, e.g. broader, exact, related, narrower
    insertQuery = about + " oboInOwl:Synonym " + synonym + " . " 

    #"<oboInOwl:hasExactSynonym rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">reproductive physiological process</oboInOwl:hasExactSynonym>"

    insert = "INSERT {" + insertQuery + "}"

    where = "WHERE {}"

    updateQuery =  prefix + " " + \
                   insert + " " + \
                   where 

    return updateQuery 


