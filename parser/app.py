from flask import Flask, render_template, url_for, render_template_string, request, redirect 
import parser
import kgcl_2_sparql
import graph_transformer

import sys
sys.path.append("../")
import python.kgcl 

app = Flask(__name__)

#we could store changes in a data base - do we want to
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        input = request.form['content']  #get input from web app
        output = parse(input)            #parse input string into data model

        #graph_transformer.transform_set(output)

        output_rendering =  ""           #render output
        for o in output: 
            output_rendering += render(o) + "\n" 

        return render_template('index.html', input=input, output=output_rendering)
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
                + "About=" + kgclInstance.about + ")"  

    if(type(kgclInstance) is python.kgcl.NodeDeletion):
        render = render + "NodeDeletion(" \
                + "ID=" + kgclInstance.id + ", " \
                + "About=" + kgclInstance.about + ")"  

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
                + "Term id=" + kgclInstance.about + ")" 

    if(type(kgclInstance) is python.kgcl.NodeDeepening):
        render = render + "NodeDeepening(" \
                + "ID=" + kgclInstance.id + ", " \
                + "Term ID=" + kgclInstance.about + ", " \
                + "Old Value=" + kgclInstance.old_value + ", " \
                + "New Value=" + kgclInstance.new_value + ")"

    if(type(kgclInstance) is python.kgcl.NodeShallowing):
        render = render + "NodeShallowing(" \
                + "ID=" + kgclInstance.id + ", " \
                + "Term ID=" + kgclInstance.about + ", " \
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

    return render 

if __name__ == "__main__":
    app.run(debug=True)

