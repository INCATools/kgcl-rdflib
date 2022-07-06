from flask import (
    Flask,
    render_template,
    request,
)

from kgcl_rdflib.apply.graph_transformer import apply_patch

# from kgcl.diff.example_kgcl_operations import generate_diff
import rdflib
from kgcl_schema.grammar import parse

import kgcl_rdflib.diff.diff_2_kgcl_single as single
import kgcl_rdflib.diff.diff_2_kgcl_existential as existential
import kgcl_rdflib.diff.diff_2_kgcl_triple_annotation as annotation

from kgcl_rdflib.diff.pretty_print_kgcl import render_instances

# from diff.example_kgcl_operations import generate_diff
from kgcl_rdflib.render_kgcl import render


def generate_diff():
    pass


app = Flask(__name__)


# we could store changes in a data base - do we want to
@app.route("/", methods=["POST", "GET"])
def index():
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
        "changeRelationship",
        "createSynonym",
        "edgeCreation",
        "edgeDeletion",
        "addSubsumptionAxiom",
        "deleteSubsumptionAxiom",
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
        f = open("examples/kgcl/tmp/transformation.nt", "r")
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
        f = open("examples/kgcl/tmp/transformation.nt", "r")
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

        f = open("examples/kgcl/tmp/patch.kgcl", "r")
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

        f = open("examples/kgcl/tmp/patch.kgcl", "r")
        kgcl = f.read()
        f.close()

        return render_template(
            "diff.html",
            examples=examples,
            kgclDiff=kgcl,
            inputGraph1=graph1,
            inputGraph2=graph2,
        )


# def parse(input):
#     return parsing.parse(input)


def kgcl_transformation(graph, kgcl):
    # store graph as file
    f = open("examples/kgcl/tmp/graph.nt", "w")
    f.write(graph)
    f.close()

    # store kgcl statements
    f = open("examples/kgcl/tmp/kgcl", "w")
    f.write(kgcl)
    f.close()

    # parse KGCL input
    parsed_statements = parse(kgcl)

    # load input graph from file
    g = rdflib.Graph()
    g.load("examples/kgcl/tmp/graph.nt", format="nt")

    # transform graph
    apply_patch(parsed_statements, g)

    # save graph
    # TODO: get text representation of graph without writing to a file
    g.serialize(destination="examples/kgcl/tmp/transformation.nt", format="nt")


def kgcl_diff(graph1, graph2):
    # store graph as file
    f = open("examples/kgcl/tmp/graph1.nt", "w")
    f.write(graph1)
    f.close()

    f = open("examples/kgcl/tmp/graph2.nt", "w")
    f.write(graph2)
    f.close()

    # generate diff
    # load graphs
    g1 = rdflib.Graph()
    g2 = rdflib.Graph()
    g1.load("examples/kgcl/tmp/graph1.nt", format="nt")
    g2.load("examples/kgcl/tmp/graph2.nt", format="nt")

    # compute diff
    existential_summary = existential.generate_atomic_existential_commands(g1, g2)
    triple_annotation_summary = annotation.generate_triple_annotation_commands(g1, g2)
    single_triple_summary = single.generate_thin_triple_commands(g1, g2)

    # get KGCL commands
    kgcl_commands = existential_summary.get_commands()
    kgcl_commands += triple_annotation_summary.get_commands()
    kgcl_commands += single_triple_summary.get_commands()

    # pretty printing of KGCL commands
    kgcl_commands = render_instances(kgcl_commands, g1)

    # write KGCL commands
    with open("examples/kgcl/tmp/patch.kgcl", "w") as f:
        for k in kgcl_commands:
            f.write(k)
            f.write("\n")


if __name__ == "__main__":
    app.run(debug=True)
