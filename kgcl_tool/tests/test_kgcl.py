from rdflib.namespace import (
    OWL,
    RDF,
    RDFS,
    XSD,
)
from rdflib import URIRef, Literal
from rdflib.compare import to_isomorphic, graph_diff

import rdflib
from grammar.parser import parse
from transformer.graph_transformer import transform_graph
import os


def compare_graphs(actual, expected):
    actual_iso = to_isomorphic(actual)
    expected_iso = to_isomorphic(expected)

    error = ""

    if actual_iso != expected_iso:
        _, in_first, in_second = graph_diff(actual_iso, expected_iso)
        error += "\tThe actual and expected graphs differ\n"
        error += "\t----- Contents of actual graph not in expected graph -----\n"
        # error += "\t" + in_first.serialize(format="nt").decode("utf-8") + "\n"
        error += (
            "\t"
            + "\t".join(
                in_first.serialize(format="nt").decode("utf-8").splitlines(True)
            )
            + "\n"
        )

        # dump_ttl_sorted(in_first)
        error += "\t----- Contents of expected graph not in actual graph -----\n"
        # error += "\t" + in_second.serialize(format="nt").decode("utf-8") + "\n"
        error += (
            "\t"
            + "\t".join(
                in_second.serialize(format="nt").decode("utf-8").splitlines(True)
            )
            + "\n"
        )
        # dump_ttl_sorted(in_second)

    comp = actual_iso == expected_iso
    return comp, error


def kgcl_transformation(graphPath, kgclPath):

    f = open(kgclPath, "r")
    kgcl = f.read()
    f.close()

    # parse KGCL input
    parsed_statements = parse(kgcl)

    # load input graph from file
    g = rdflib.Graph()
    g.load(graphPath, format="nt")

    # transform graph
    transform_graph(parsed_statements, g)

    return g


def test_examples():
    directory = os.path.join(os.getcwd(), "tests/data/kgcl")
    for filename in os.listdir(directory):
        path = directory + "/" + filename
        inputGraphPath = path + "/inputGraph.nt"
        outputGraphPath = path + "/outputGraph.nt"
        kgclPath = path + "/kgcl"

        transformation = kgcl_transformation(inputGraphPath, kgclPath)
        expectedGraph = rdflib.Graph()
        expectedGraph.load(outputGraphPath, format="nt")

        res, error = compare_graphs(transformation, expectedGraph)
        if res:
            print("Test {name} passes".format(name=filename))
        else:
            print("Test {name} fails".format(name=filename))
            print(error)


if __name__ == "__main__":
    test_examples()
