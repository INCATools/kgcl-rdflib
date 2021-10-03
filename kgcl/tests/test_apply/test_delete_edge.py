from kgcl.tests.test_apply.util import run_test


def test_delete_edge_with_ids():
    input_graph = "<http://example.org/subject> <http://example.org/predicate> <http://example.org/object> ."
    kgcl_patch = "delete edge <http://example.org/subject> <http://example.org/predicate> <http://example.org/object>"
    expected_graph = ""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_delete_edge_with_curies():
    input_graph = "<http://example.org/subject> <http://example.org/predicate> <http://example.org/object> ."
    kgcl_patch = "delete edge ex:subject ex:predicate ex:object"
    expected_graph = ""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_delete_edge_with_labels():
    input_graph = """<http://example.org/subject> <http://example.org/predicate> <http://example.org/object> .
                     <http://example.org/subject> <http://www.w3.org/2000/01/rdf-schema#label> "subject" ."""
    kgcl_patch = "delete edge 'subject' ex:predicate ex:object"
    expected_graph = '<http://example.org/subject> <http://www.w3.org/2000/01/rdf-schema#label> "subject" .'
    run_test(input_graph, kgcl_patch, expected_graph)
