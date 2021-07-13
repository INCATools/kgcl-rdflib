from lark import Lark, Tree, Token


def idGenerator():
    id = 0
    while True:
        yield id
        id += 1

kgcl_parser = Lark.open('kgcl.lark', start='expression')

def getTokens(tree):
    return tree.scan_values(lambda v: isinstance(v, Token))



if __name__ == "__main__":
    ###
    ### MANUAL TESTING
    ###
#TODO: cannot work out how to parse strings without delimiter
    example2 = "rename abnormal to moreg"
    tree2 = kgcl_parser.parse(example2); 
    print(tree2)

    #test = tree.find_data('old')
    #old = next(test)
    #old_token = next(getTokens(old))
    #print(old_token)


    #example2 = "obsolete 'abnormal ear'"
    #tree2 = kgcl_parser.parse(example2); 
    #obsolete_token = next(getTokens(tree2))
    #print(tree2)
    #print(obsolete_token)


