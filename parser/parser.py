from lark import Lark, Tree, Token

import sys
sys.path.append("../")
import python.kgcl

def idGenerator():
    id = 0
    while True:
        yield id
        id += 1

kgcl_parser = Lark.open('kgcl.lark', start='expression')
id_gen = idGenerator()

#input may be a set of KGCL statements separated by \n
def parse(input):
    statements = input.splitlines()
    parsed = []

    for s in statements:
        parsed.append(parseStatement(s))
        #parsed.append((s,parseStatement(s))) 
    return parsed 

def parseStatement(input): 

    try: 
        tree = kgcl_parser.parse(input); 

        id = "test_id_" + str(next(id_gen))

        command = tree.data

        if(command == "rename"): 
            old = next(tree.find_data('old'))#node with data 'old' is unique
            old_token = next(getTokens(old))#node only as one token

            new = next(tree.find_data('new'))
            new_token = next(getTokens(new))

            return python.kgcl.NodeRename(id=id, old_value=old_token, new_value=new_token)

        if(command == "obsolete"):
            label = next(tree.find_data('old'))
            label_token = next(getTokens(label))
            return python.kgcl.NodeObsoletion(id=id, about=label_token)

        if(command == "move"):
            old = next(tree.find_data('old'))
            old_token = next(getTokens(old))

            new = next(tree.find_data('new'))
            new_token = next(getTokens(new))
            return python.kgcl.NodeMove(id=id, old_value=old_token, new_value=new_token)


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
        #if(command == "create"): 

    except:
        print("Failed to parse expression:")
        print(input)

def getTokens(tree):
    return tree.scan_values(lambda v: isinstance(v, Token))

if __name__ == "__main__":
    ###
    ### MANUAL TESTING
    ### 
    example1 = "rename 'abnormal ear' to 'abnormal ear morphology'"
    tree = kgcl_parser.parse(example1); 
    print(tree)
    old = next(tree.find_data('old')) 
    print(old)
    old_token = next(getTokens(old))
    print(old_token) 
