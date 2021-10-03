from kgcl.tests.test_apply.util import run_test


def test_create_existential_restriction_with_ids():
    input_graph = ""
    kgcl_patch = "add <http://example.org/subject> SubClassOf <http://example.org/predicate> some <http://example.org/object>"
    expected_graph = """_:Nfb1ff91c88fe4e328efb4ceea0a11730 <http://www.w3.org/2002/07/owl#onProperty> <http://example.org/predicate> .
                        _:Nfb1ff91c88fe4e328efb4ceea0a11730 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Restriction> .
                        <http://example.org/subject> <http://www.w3.org/2000/01/rdf-schema#subClassOf> _:Nfb1ff91c88fe4e328efb4ceea0a11730 .
                        _:Nfb1ff91c88fe4e328efb4ceea0a11730 <http://www.w3.org/2002/07/owl#someValuesFrom> <http://example.org/object> ."""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_existential_restriction_with_curies():
    input_graph = ""
    kgcl_patch = "add ex:subject SubClassOf ex:predicate some ex:object"
    expected_graph = """_:Nfb1ff91c88fe4e328efb4ceea0a11730 <http://www.w3.org/2002/07/owl#onProperty> <http://example.org/predicate> .
                        _:Nfb1ff91c88fe4e328efb4ceea0a11730 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Restriction> .
                        <http://example.org/subject> <http://www.w3.org/2000/01/rdf-schema#subClassOf> _:Nfb1ff91c88fe4e328efb4ceea0a11730 .
                        _:Nfb1ff91c88fe4e328efb4ceea0a11730 <http://www.w3.org/2002/07/owl#someValuesFrom> <http://example.org/object> ."""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_existential_restriction_with_labels():
    input_graph = """<http://example.org/subject> <http://www.w3.org/2000/01/rdf-schema#label> "subject" .
                     <http://example.org/predicate> <http://www.w3.org/2000/01/rdf-schema#label> "predicate" .
                     <http://example.org/object> <http://www.w3.org/2000/01/rdf-schema#label> "object" ."""
    kgcl_patch = "add 'subject' SubClassOf 'predicate' some 'object'"
    expected_graph = """_:Nfb1ff91c88fe4e328efb4ceea0a11730 <http://www.w3.org/2002/07/owl#onProperty> <http://example.org/predicate> .
                        _:Nfb1ff91c88fe4e328efb4ceea0a11730 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Restriction> .
                        <http://example.org/subject> <http://www.w3.org/2000/01/rdf-schema#subClassOf> _:Nfb1ff91c88fe4e328efb4ceea0a11730 .
                        _:Nfb1ff91c88fe4e328efb4ceea0a11730 <http://www.w3.org/2002/07/owl#someValuesFrom> <http://example.org/object> .
                        <http://example.org/subject> <http://www.w3.org/2000/01/rdf-schema#label> "subject" .
                        <http://example.org/predicate> <http://www.w3.org/2000/01/rdf-schema#label> "predicate" .
                        <http://example.org/object> <http://www.w3.org/2000/01/rdf-schema#label> "object" ."""

    run_test(input_graph, kgcl_patch, expected_graph)
