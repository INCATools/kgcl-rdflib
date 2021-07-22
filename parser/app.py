from flask import Flask, render_template, url_for, render_template_string, request, redirect 
import parser
import kgcl_2_sparql
import graph_transformer
import rdflib

import sys
sys.path.append("../")
import python.kgcl 

app = Flask(__name__)

#we could store changes in a data base - do we want to
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        if "load_data" in request.form:
            #expect input RDF graph as triples
            input = request.form['content']
            f = open("testData/graph.nt", "w")
            f.write(input)
            f.close()

        if "load_kgcl" in request.form:
            input = request.form['content']
            f = open("testData/kgcl", "w")
            f.write(input)
            f.close() 

        #if "parse_kgcl" in request.form: 
        #    f = open("testData/kgcl", "r") 
        #    kgcl = f.read()
        #    f.close()
        #    #read kgcl file and parse from there
        #    output = parse(kgcl)            #parse input string into data model 
        #    output_rendering =  ""           #render output
        #    for o in output: 
        #        output_rendering += render(o) + "\n" 
        #    return render_template('index.html', inputKGCL=kgcl, parsedKGCL=output_rendering)

        if "apply_changes" in request.form:

            #load KGCL input
            f = open("testData/kgcl", "r") 
            kgcl = f.read()
            f.close() 

            #parse KGCL input
            parsed_statements = parse(kgcl) 

            #load graph
            g = rdflib.Graph()
            g.load("testData/graph.nt", format="nt") 

            #transform graph 
            graph_transformer.transform_graph(parsed_statements, g)

            #save graph
            g.serialize(destination="testData/transformation.nt", format='nt') 

        if "load_example" in request.form:

            f = open("testData/example/graph.nt", "r") 
            graph = f.read()
            f.close() 

            f = open("testData/graph.nt", "w")
            f.write(graph)
            f.close()

            f = open("testData/example/kgcl", "r") 
            kgcl = f.read()
            f.close()

            f = open("testData/kgcl", "w")
            f.write(kgcl)
            f.close()

        #load graph
        f = open("testData/graph.nt", "r") 
        graph = f.read()
        f.close() 

        #load KGCL input
        f = open("testData/kgcl", "r") 
        kgcl = f.read()
        f.close() 

        #parse KGCL input
        output = parse(kgcl)

        #prepare parsed 
        output_rendering = "" 
        for o in output: 
            output_rendering += render(o) + "\n" 

        #load transformed graph
        f = open("testData/transformation.nt", "r") 
        transformation = f.read()
        f.close() 

        return render_template('index.html', inputGraph=graph, inputKGCL=kgcl, parsedKGCL=output_rendering, outputGraph=transformation) 

    else: 
        return render_template('index.html')

def parse(input):
    return parser.parse(input)

def render(kgclInstance):
    render = ""
    if(type(kgclInstance) is python.kgcl.NodeRename):
        render = render + "NodeRename(" \
                + "ID=" + kgclInstance.id + ", " \
                + "Old Value=" + kgclInstance.old_value + ", " \
                + "New Value=" + kgclInstance.new_value + ")"

    if(type(kgclInstance) is python.kgcl.NodeObsoletion): 
        render = render + "NodeObsoletion(" \
                + "ID=" + kgclInstance.id + ", " \
                + "Repacelement=" + str(kgclInstance.has_direct_replacement) + ", " \
                + "About=" + kgclInstance.about_node + ")"  

    if(type(kgclInstance) is python.kgcl.NodeDeletion):
        render = render + "NodeDeletion(" \
                + "ID=" + kgclInstance.id + ", " \
                + "About=" + kgclInstance.about_node + ")"  

    if(type(kgclInstance) is python.kgcl.ClassCreation):
        render = render + "ClassCreation(" \
                + "ID=" + kgclInstance.id + ", " \
                + "Term_ID" + kgclInstance.node_id + ")"

    if(type(kgclInstance) is python.kgcl.NodeCreation):
        render = render + "NodeCreation(" \
                + "ID=" + kgclInstance.id + ", " \
                + "Term ID=" + kgclInstance.node_id + ", " \
                + "Label=" + kgclInstance.name + ")"  

    if(type(kgclInstance) is python.kgcl.NodeMove):
        render = render + "NodeMove(" \
                + "ID=" + kgclInstance.id + ", " \
                + "Old Value=" + kgclInstance.old_value + ", " \
                + "New Value=" + kgclInstance.new_value + ")"

    if(type(kgclInstance) is python.kgcl.NodeUnobsoletion):
        render = render + "NodeUnobsoletion(" \
                + "ID=" + kgclInstance.id + ", " \
                + "Term id=" + kgclInstance.about_node + ")" 

    if(type(kgclInstance) is python.kgcl.NodeDeepening):
        render = render + "NodeDeepening(" \
                + "ID=" + kgclInstance.id + ", " \
                + "Term ID=" + kgclInstance.about_edge.subject + ", " \
                + "Old Value=" + kgclInstance.old_value + ", " \
                + "New Value=" + kgclInstance.new_value + ")"

    if(type(kgclInstance) is python.kgcl.NodeShallowing):
        render = render + "NodeShallowing(" \
                + "ID=" + kgclInstance.id + ", " \
                + "Term ID=" + kgclInstance.about_edge.suject + ", " \
                + "Old Value=" + kgclInstance.old_value + ", " \
                + "New Value=" + kgclInstance.new_value + ")"

    if(type(kgclInstance) is python.kgcl.EdgeCreation):
        render = render + "EdgeCreation(" \
                + "ID=" + kgclInstance.id + ", " \
                + "Subject=" + kgclInstance.subject + ", " \
                + "Predicate=" + kgclInstance.predicate + ", " \
                + "Object=" + kgclInstance.object + ")"

    if(type(kgclInstance) is python.kgcl.EdgeDeletion):
        render = render + "EdgeDeletion(" \
                + "ID=" + kgclInstance.id + ", " \
                + "Subject=" + kgclInstance.subject + ", " \
                + "Predicate=" + kgclInstance.predicate + ", " \
                + "Object=" + kgclInstance.object + ")"

    if(type(kgclInstance) is python.kgcl.NewSynonym):
        render = render + "NewSynonym(" \
                + "ID=" + kgclInstance.id + ", " \
                + "About Node=" + kgclInstance.about_node + ", " \
                + "Synonym=" + kgclInstance.new_value + ")"

    return render 

if __name__ == "__main__":
    app.run(debug=True)

