"""Test node move."""
from util import run_test


def test_node_move_with_ids():
    input_graph = "<http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/A> ."
    kgcl_patch = "move <http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/A> from <http://example.org/A> to <http://example.org/B>"
    expected_graph = "<http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/B> ."

    run_test(input_graph, kgcl_patch, expected_graph)


def test_node_move_with_curies():
    input_graph = "<http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/A> ."
    kgcl_patch = "move ex:targetClass <http://www.w3.org/2000/01/rdf-schema#subClassOf> ex:A from ex:A to ex:B"
    expected_graph = "<http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/B> ."

    run_test(input_graph, kgcl_patch, expected_graph)


def test_node_move_with_labels():
    input_graph = """<http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/A> .
                     <http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#label> "targetClass" .
                     <http://example.org/A> <http://www.w3.org/2000/01/rdf-schema#label> "A" .
                     <http://example.org/B> <http://www.w3.org/2000/01/rdf-schema#label> "B" ."""
    kgcl_patch = "move 'targetClass' <http://www.w3.org/2000/01/rdf-schema#subClassOf> 'A' from 'A' to 'B'"
    expected_graph = """<http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/B> .
                        <http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#label> "targetClass" .
                        <http://example.org/A> <http://www.w3.org/2000/01/rdf-schema#label> "A" .
                        <http://example.org/B> <http://www.w3.org/2000/01/rdf-schema#label> "B" ."""

    run_test(input_graph, kgcl_patch, expected_graph)
