from flask import Flask, render_template, url_for, render_template_string, request, redirect 
import parser

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
        output_rendering =  ""           #render output
        for o in output: 
            output_rendering += render(o) + "\n" 

        return render_template('index.html', input=input, output=output_rendering)
        #return redirect('/') 
    else: 
        return render_template('index.html')

def parse(input):
    return parser.parse(input)

def render(kgclInstance):
    render = ""
    if(isinstance(kgclInstance, python.kgcl.NodeRename)):
        render = render + "NodeRename(" \
                + "ID=" + kgclInstance.id + ", " \
                + "Old Value=" + kgclInstance.old_value + ", " \
                + "New Value=" + kgclInstance.new_value + ")"
    if(isinstance(kgclInstance, python.kgcl.NodeObsoletion)):
        render = render + "NodeObsoletion(" \
                + "ID=" + kgclInstance.id + ", " \
                + "About=" + kgclInstance.about + ")"  
    if(isinstance(kgclInstance, python.kgcl.NodeMove)):
        render = render + "NodeMove(" \
                + "ID=" + kgclInstance.id + ", " \
                + "Old Value=" + kgclInstance.old_value + ", " \
                + "New Value=" + kgclInstance.new_value + ")"

    return render


if __name__ == "__main__":
    app.run(debug=True)

