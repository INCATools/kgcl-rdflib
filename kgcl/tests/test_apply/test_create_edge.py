from kgcl.tests.test_apply.util import run_test


def test_create_edge_with_ids():
    input_graph = ""
    kgcl_patch = "create edge <http://example.org/subject> <http://example.org/predicate> <http://example.org/object>"
    expected_graph = "<http://example.org/subject> <http://example.org/predicate> <http://example.org/object> ."

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_edge_with_curies():
    input_graph = ""
    kgcl_patch = "create edge ex:subject ex:predicate ex:object"
    expected_graph = "<http://example.org/subject> <http://example.org/predicate> <http://example.org/object> ."

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_edge_with_labels():
    input_graph = """<http://example.org/subject> <http://example.org/predicate> <http://example.org/object> .
                     <http://example.org/subject> <http://www.w3.org/2000/01/rdf-schema#label> "subject" ."""
    kgcl_patch = "create edge 'subject' <http://example.org/predicate> <http://example.org/object>"
    expected_graph = """<http://example.org/subject> <http://example.org/predicate> <http://example.org/object> .
                        <http://example.org/subject> <http://www.w3.org/2000/01/rdf-schema#label> "subject" ."""

    run_test(input_graph, kgcl_patch, expected_graph)
