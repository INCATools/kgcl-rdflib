from kgcl.tests.test_apply.util import run_test


def test_create_subsumption_with_ids():
    input_graph = ""
    kgcl_patch = (
        "add <http://example.org/subclass> SubClassOf <http://example.org/superclass>"
    )
    expected_graph = "<http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/superclass> ."

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_subsumption_with_curies():
    input_graph = ""
    kgcl_patch = "add ex:subclass SubClassOf ex:superclass"
    expected_graph = "<http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/superclass> ."

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_subsumption_with_labels():
    input_graph = """<http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#label> "subclass" .
                     <http://example.org/superclass> <http://www.w3.org/2000/01/rdf-schema#label> "superclass" ."""
    kgcl_patch = "add 'subclass' SubClassOf 'superclass'"
    expected_graph = """<http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/superclass> .
                        <http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#label> "subclass" .
                        <http://example.org/superclass> <http://www.w3.org/2000/01/rdf-schema#label> "superclass" ."""

    run_test(input_graph, kgcl_patch, expected_graph)
