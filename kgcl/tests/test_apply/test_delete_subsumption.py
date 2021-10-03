from kgcl.tests.test_apply.util import run_test


def test_delete_subsumption_with_ids():
    input_graph = "<http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/superclass> ."
    kgcl_patch = "delete <http://example.org/subclass> SubClassOf <http://example.org/superclass>"
    expected_graph = ""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_delete_subsumption_with_curies():
    input_graph = "<http://example.org/subclass> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://example.org/superclass> ."
    kgcl_patch = "delete ex:subclass SubClassOf ex:superclass"
    expected_graph = ""

    run_test(input_graph, kgcl_patch, expected_graph)
