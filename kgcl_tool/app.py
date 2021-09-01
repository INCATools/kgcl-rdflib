from flask import (
    Flask,
    render_template,
    request,
)
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
from grammar.parser import parse
from transformer.graph_transformer import transform_graph
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
        "annotatedEdgeCreation",
        "annotatedEdgeDeletion",
        "changeRelationship",
        "createSynonym",
        "addSubsumptionAxiom",
        "deleteSubsumptionAxiom",
        "addExistential",
        "deleteExistential",
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

            f = open("examples/kgcl/" + example + "/graph.nt", "r")
            graph = f.read()
            f.close()

            f = open("examples/kgcl/" + example + "/kgcl", "r")
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
        f = open("examples/kgcl/rename/graph.nt", "r")
        graph = f.read()
        f.close()

        # load kgcl
        f = open("examples/kgcl/rename/kgcl", "r")
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

        # return render_template("index.html", examples=examples)
        return render_template(
            "index.html",
            inputGraph=graph,
            inputKGCL=kgcl,
            parsedKGCL=kgcl_model_rendering,
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
    graph1 = ""
    graph2 = ""
    kgcl = ""

    if request.method == "POST":

        if "generate_diff" in request.form:
            graph1 = request.form["graph1"]
            graph2 = request.form["graph2"]

            kgcl_diff(graph1, graph2)

        if "load_example_diff" in request.form:
            select = request.form.get("comp_select")
            example = str(select)

            f = open("examples/diff/" + example + "/graph1.nt", "r")
            graph1 = f.read()
            f.close()

            f = open("examples/diff/" + example + "/graph2.nt", "r")
            graph2 = f.read()
            f.close()

            kgcl_diff(graph1, graph2)

        f = open("diff/stats/all", "r")
        kgcl = f.read()
        f.close()

        return render_template(
            "diff.html",
            examples=examples,
            kgclDiff=kgcl,
            inputGraph1=graph1,
            inputGraph2=graph2,
        )
    else:
        # load rename by default
        example = "rename"

        f = open("examples/diff/" + example + "/graph1.nt", "r")
        graph1 = f.read()
        f.close()

        f = open("examples/diff/" + example + "/graph2.nt", "r")
        graph2 = f.read()
        f.close()

        kgcl_diff(graph1, graph2)

        f = open("diff/stats/all", "r")
        kgcl = f.read()
        f.close()

        return render_template(
            "diff.html",
            examples=examples,
            kgclDiff=kgcl,
            inputGraph1=graph1,
            inputGraph2=graph2,
        )


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
    transform_graph(parsed_statements, g)

    # save graph
    # TODO: get text representation of graph without writing to a file
    g.serialize(destination="testData/transformation.nt", format="nt")


def kgcl_diff(graph1, graph2):
    # store graph as file
    f = open("testData/graph1.nt", "w")
    f.write(graph1)
    f.close()

    f = open("testData/graph2.nt", "w")
    f.write(graph2)
    f.close()

    os.system("sh diff/kgcl_diff.sh testData/graph1.nt testData/graph2.nt")
    generate_diff()


if __name__ == "__main__":
    app.run(debug=True)
