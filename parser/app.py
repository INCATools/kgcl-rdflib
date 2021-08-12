from flask import (
    Flask,
    render_template,
    request,
)
from kgcl import (
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
import parser
import graph_transformer
import rdflib
import os
import sys
from diff.example_kgcl_operations import generate_diff
from render_kgcl import render

app = Flask(__name__)


# we could store changes in a data base - do we want to
@app.route("/", methods=["POST", "GET"])
def index():
    # TODO: get examples from folder structure
    examples = [
        "rename",
        "nodeCreation",
        "nodeDeletionByLabel",
        "nodeDeletionById",
        "obsoleteByLabel",
        "obsoleteById",
        "unobsoleteById",
        "nodeDeepening",
        "nodeShallowing",
        "move",
        "edgeCreation",
        "edgeDeletion",
    ]

    if request.method == "POST":

        if "apply_changes" in request.form:

            # get input graph from form
            graph = request.form["graph"]

            # get input kgcl statements from form
            kgcl = request.form["kgcl"]

            kgcl_transformation(graph, kgcl)

        if "load_example" in request.form:
            select = request.form.get("comp_select")
            example = str(select)

            f = open("testData/example/" + example + "/graph.nt", "r")
            graph = f.read()
            f.close()

            f = open("testData/example/" + example + "/kgcl", "r")
            kgcl = f.read()
            f.close()

            kgcl_transformation(graph, kgcl)

        # parse KGCL input
        kgcl_model = parse(kgcl)

        # prepare parsed
        kgcl_model_rendering = ""
        for o in kgcl_model:
            kgcl_model_rendering += render(o) + "\n"

        # load transformed graph
        f = open("testData/transformation.nt", "r")
        transformation = f.read()
        f.close()

        return render_template(
            "index.html",
            inputGraph=graph,
            inputKGCL=kgcl,
            parsedKGCL=kgcl_model_rendering,
            outputGraph=transformation,
            examples=examples,
        )

    else:
        # load rename example by default

        # load graph
        f = open("testData/example/rename/graph.nt", "r")
        graph = f.read()
        f.close()

        f = open("testData/graph.nt", "w")
        f.write(graph)
        f.close()

        # load kgcl
        f = open("testData/example/rename/kgcl", "r")
        kgcl = f.read()
        f.close()

        f = open("testData/kgcl", "w")
        f.write(kgcl)
        f.close()

        # parse KGCL input
        output = parse(kgcl)

        # prepare parsed
        output_rendering = ""
        for o in output:
            output_rendering += render(o) + "\n"

        # load input graph from file
        g = rdflib.Graph()
        g.load("testData/graph.nt", format="nt")

        # transform graph
        graph_transformer.transform_graph(output, g)

        # save graph
        g.serialize(destination="testData/transformation.nt", format="nt")

        # load transformed graph
        f = open("testData/transformation.nt", "r")
        transformation = f.read()
        f.close()

        # return render_template("index.html", examples=examples)
        return render_template(
            "index.html",
            inputGraph=graph,
            inputKGCL=kgcl,
            parsedKGCL=output_rendering,
            outputGraph=transformation,
            examples=examples,
        )


@app.route("/diff", methods=["POST", "GET"])
def diff():

    examples = [
        "rename",
        "classCreation",
        "obsoletion",
        "unobsoletion",
        "move",
        "edgeCreation",
        "edgeDeletion",
    ]

    # initialise variables
    inputGraph1 = ""
    inputGraph2 = ""
    kgcl = ""

    if request.method == "POST":

        if "generate_diff" in request.form:
            inputGraph1 = request.form["graph1"]
            inputGraph2 = request.form["graph2"]

            # store graph as file
            f = open("testData/graph1.nt", "w")
            f.write(inputGraph1)
            f.close()

            f = open("testData/graph2.nt", "w")
            f.write(inputGraph2)
            f.close()

            os.system("sh diff/kgcl_diff.sh testData/graph1.nt testData/graph2.nt")
            generate_diff()

        if "load_example_diff" in request.form:
            select = request.form.get("comp_select")
            example = str(select)

            f = open("testData/diffExample/" + example + "/graph1.nt", "r")
            graph1 = f.read()
            f.close()

            f = open("testData/diffExample/" + example + "/graph2.nt", "r")
            graph2 = f.read()
            f.close()

            inputGraph1 = graph1
            inputGraph2 = graph2

            f = open("testData/graph1.nt", "w")
            f.write(graph1)
            f.close()

            f = open("testData/graph2.nt", "w")
            f.write(graph2)
            f.close()

            os.system("sh diff/kgcl_diff.sh testData/graph1.nt testData/graph2.nt")
            generate_diff()

        f = open("diff/stats/all", "r")
        kgcl = f.read()
        f.close()

        return render_template(
            "diff.html",
            examples=examples,
            kgclDiff=kgcl,
            inputGraph1=inputGraph1,
            inputGraph2=inputGraph2,
        )
    else:
        # load rename by default
        example = "rename"

        f = open("testData/diffExample/" + example + "/graph1.nt", "r")
        graph1 = f.read()
        f.close()

        f = open("testData/diffExample/" + example + "/graph2.nt", "r")
        graph2 = f.read()
        f.close()

        inputGraph1 = graph1
        inputGraph2 = graph2

        f = open("testData/graph1.nt", "w")
        f.write(graph1)
        f.close()

        f = open("testData/graph2.nt", "w")
        f.write(graph2)
        f.close()

        os.system("sh diff/kgcl_diff.sh testData/graph1.nt testData/graph2.nt")
        generate_diff()

        f = open("diff/stats/all", "r")
        kgcl = f.read()
        f.close()

        return render_template(
            "diff.html",
            examples=examples,
            kgclDiff=kgcl,
            inputGraph1=inputGraph1,
            inputGraph2=inputGraph2,
        )


def parse(input):
    return parser.parse(input)


def kgcl_transformation(graph, kgcl):
    # store graph as file
    f = open("testData/graph.nt", "w")
    f.write(graph)
    f.close()

    # store kgcl statements
    f = open("testData/kgcl", "w")
    f.write(kgcl)
    f.close()

    # parse KGCL input
    parsed_statements = parse(kgcl)

    # load input graph from file
    g = rdflib.Graph()
    g.load("testData/graph.nt", format="nt")

    # transform graph
    graph_transformer.transform_graph(parsed_statements, g)

    # save graph
    # TODO: get text representation of graph without writing to a file
    g.serialize(destination="testData/transformation.nt", format="nt")


if __name__ == "__main__":
    app.run(debug=True)
