from lark import Lark, Tree, Token

import sys
sys.path.append("../")
import python.kgcl
import python.ontology_model

def id_generator():
    id = 0
    while True:
        yield id
        id += 1

kgcl_parser = Lark.open('kgcl.lark', start='expression')
id_gen = id_generator()

#input may be a set of KGCL statements separated by \n
def parse(input):
    statements = input.splitlines()
    parsed = []

    for s in statements:
        parsed.append(parse_statement(s))
        #parsed.append((s,parse_statement(s))) 
    return parsed 

def parse_statement(input): 

    tree = kgcl_parser.parse(input)

    id = "test_id_" + str(next(id_gen))

    command = tree.data
    #print("Command: " + command)

    if(command == "rename"): 
        old = next(tree.find_data('old_label')) #node with data 'old_label' is unique
        old_token = next(get_tokens(old))       #and this node only has one token

        new = next(tree.find_data('new_label'))
        new_token = next(get_tokens(new)) 

        term_id = tree.find_data('id')

        term_id_list = list(tree.find_data('id'))
        if(term_id_list):#test whether there is an element in the generator
            t = next(term_id)
            term_id_token = next(get_tokens(t)) 
            return python.kgcl.NodeRename(id=id, about_node=term_id_token, old_value=old_token, new_value=new_token) 
        else: 
            return python.kgcl.NodeRename(id=id, old_value=old_token, new_value=new_token)

    if(command == "obsolete"):
        label = next(tree.find_data('entity'))
        label_token = next(get_tokens(label))


        replacement_id = tree.find_data('replacement')

        replacement_id_list = list(tree.find_data('replacement'))
        if(replacement_id_list):
            t = next(replacement_id)
            replacement_token = next(get_tokens(t))
            return python.kgcl.NodeObsoletion(id=id, about_node=label_token, has_direct_replacement=replacement_token) 
        else: 
            return python.kgcl.NodeObsoletion(id=id, about_node=label_token)

    if(command == "unobsolete"):
        term_id = next(tree.find_data('id'))
        term_id_token = next(get_tokens(term_id))

        return python.kgcl.NodeUnobsoletion(id=id, about_node=term_id_token) 

    if(command == "delete"):
        label = next(tree.find_data('entity'))#TODO check whether we want to delete nodes by label 
        label_token = next(get_tokens(label))

        return python.kgcl.NodeDeletion(id=id, about_node=label_token)

    if(command == "move"): 
        term_id = next(tree.find_data('id'))
        term_id_token = next(get_tokens(term_id))

        old = next(tree.find_data('old_id'))
        old_token = next(get_tokens(old))

        new = next(tree.find_data('new_id'))
        new_token = next(get_tokens(new))

        edge = python.ontology_model.Edge(subject=term_id_token, object=old_token)

        return python.kgcl.NodeMove(id=id, about_edge=edge, old_value=old_token, new_value=new_token) 
    if(command == "deepen"): 
        term_id = next(tree.find_data('id'))
        term_id_token = next(get_tokens(term_id))

        old = next(tree.find_data('old_id'))
        old_token = next(get_tokens(old))

        new = next(tree.find_data('new_id'))
        new_token = next(get_tokens(new))

        edge = python.ontology_model.Edge(subject=term_id_token, object=old_token)

        return python.kgcl.NodeDeepening(id=id, about_edge=edge, old_value=old_token, new_value=new_token)

    if(command == "shallow"): 
        term_id = next(tree.find_data('id'))
        term_id_token = next(get_tokens(term_id))

        old = next(tree.find_data('old_id'))
        old_token = next(get_tokens(old))

        new = next(tree.find_data('new_id'))
        new_token = next(get_tokens(new))

        edge = python.ontology_model.Edge(subject=term_id_token, object=old_token)

        return python.kgcl.NodeShallowing(id=id, about_edge=edge, old_value=old_token, new_value=new_token)

    if(command == "create_edge"): 
        subject = next(tree.find_data('subject'))
        subject_token = next(get_tokens(subject))

        predicate = next(tree.find_data('predicate'))
        predicate_token = next(get_tokens(predicate))

        object = next(tree.find_data('object'))
        object_token = next(get_tokens(object))

        return python.kgcl.EdgeCreation(id=id, subject=subject_token, predicate=predicate_token, object=object_token)

    if(command == "delete_edge"): 
        subject = next(tree.find_data('subject'))
        subject_token = next(get_tokens(subject))

        predicate = next(tree.find_data('predicate'))
        predicate_token = next(get_tokens(predicate))

        object = next(tree.find_data('object'))
        object_token = next(get_tokens(object))

        return python.kgcl.EdgeDeletion(id=id, subject=subject_token, predicate=predicate_token, object=object_token)

    #if(command == "change_relationship"): #TODO:: there is no field for 'object' in the data model
    #    subject = next(tree.find_data('subject'))
    #    subject_token = next(get_tokens(subject))

    #    object = next(tree.find_data('object'))
    #    object_token = next(get_tokens(object))

    #    old = next(tree.find_data('old'))
    #    old_token = next(get_tokens(old))

    #    new = next(tree.find_data('new'))
    #    new_token = next(get_tokens(new))
    #    return python.kgcl.NodeMove(id=id, about=term_id_token, old_value=old_token, new_value=new_token)

    #the KGCL model suggests the command
    #'create node {id} {label} with {annotation set}'
    #TODO: handling of {annotation set}
    if(command == "create"):
        term_id = next(tree.find_data('id'))
        term_id_token = next(get_tokens(term_id))

        label = next(tree.find_data('label'))
        label_token = next(get_tokens(label)) 
        #TODO: where is the difference between
        #a 'node_id' provided by 'NodeCreation'
        #and 'about_node' inherited by 'NodeChange'?
        return python.kgcl.NodeCreation(id=id, about_node=term_id_token, node_id=term_id_token, name=label_token) 

    if(command == "create_class"): 
        term_id = next(tree.find_data('id'))
        term_id_token = next(get_tokens(term_id))
        return python.kgcl.ClassCreation(id=id, node_id=term_id_token)


    #TODO: more cases
    #if(command == "merge"):
    #if(command == "add"):
    #if(command == "add_parent"):
    #if(command == "add_annotation"):
    #if(command == "add_synonym"):
    #if(command == "add_axiom"): (in Manchester Syntax?)
    #if(command == "add_class"):
    #if(command == "add_text_definition"):
    #if(command == "merge"): 

def get_tokens(tree):
    return tree.scan_values(lambda v: isinstance(v, Token))

if __name__ == "__main__":
    ###
    ### MANUAL TESTING
    ### 
    example1 = "renamea 'abnormal ear' to 'abnormal ear morphology'"
    tree = kgcl_parser.parse(example1); 
    print(tree)
    old = next(tree.find_data('old_label')) 
    print(old)
    old_token = next(get_tokens(old))
    print(old_token) 
