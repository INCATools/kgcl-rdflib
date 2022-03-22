"""Test node deepening."""
from util import run_test


def test_node_deepening_with_ids():
    input_graph = """<http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/superclass> .
                   <http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/superclass> ."""
    kgcl_patch = "deepen <http://example.org/targetClass> from <http://example.org/superclass> to <http://example.org/subclass>"
    expected_graph = """<http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/superclass> .
                        <http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/subclass> ."""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_node_deepening_with_curies():
    input_graph = """<http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/superclass> .
                   <http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/superclass> ."""
    kgcl_patch = "deepen ex:targetClass from ex:superclass to ex:subclass"
    expected_graph = """<http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/superclass> .
                        <http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/subclass> ."""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_node_deepening_with_labels():
    input_graph = """<http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/superclass> .
                     <http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/superclass> .
                     <http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#label> "targetClass" .
                     <http://example.org/superclass> <http://www.w3.org/2000/01/rdf-schema#label> "superclass" .
                     <http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#label> "subclass" ."""
    kgcl_patch = "deepen 'targetClass' from 'superclass' to 'subclass'"
    expected_graph = """<http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/superclass> .
                        <http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/subclass> .
                        <http://example.org/targetClass> <http://www.w3.org/2000/01/rdf-schema#label> "targetClass" .
                        <http://example.org/superclass> <http://www.w3.org/2000/01/rdf-schema#label> "superclass" .
                        <http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#label> "subclass" ."""

    run_test(input_graph, kgcl_patch, expected_graph)
