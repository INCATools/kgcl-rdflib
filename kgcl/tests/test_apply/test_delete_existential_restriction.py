from kgcl.tests.test_apply.util import run_test


def test_delete_existential_restriction_with_ids():
    input_graph = """_:Ndb451c3aad3841c88d7042f29b20bea8 <http://www.w3.org/2002/07/owl#onProperty> <http://example.org/predicate> .
                     _:Ndb451c3aad3841c88d7042f29b20bea8 <http://www.w3.org/2002/07/owl#someValuesFrom> <http://example.org/object> .
                     _:Ndb451c3aad3841c88d7042f29b20bea8 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Restriction> .
                     <http://example.org/subject> <http://www.w3.org/2000/01/rdf-schema#subClassOf> _:Ndb451c3aad3841c88d7042f29b20bea8 ."""
    kgcl_patch = "delete <http://example.org/subject> SubClassOf <http://example.org/predicate> some <http://example.org/object>"
    expected_graph = ""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_delete_existential_restriction_with_curies():
    input_graph = """_:Ndb451c3aad3841c88d7042f29b20bea8 <http://www.w3.org/2002/07/owl#onProperty> <http://example.org/predicate> .
                     _:Ndb451c3aad3841c88d7042f29b20bea8 <http://www.w3.org/2002/07/owl#someValuesFrom> <http://example.org/object> .
                     _:Ndb451c3aad3841c88d7042f29b20bea8 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Restriction> .
                     <http://example.org/subject> <http://www.w3.org/2000/01/rdf-schema#subClassOf> _:Ndb451c3aad3841c88d7042f29b20bea8 ."""
    kgcl_patch = "delete ex:subject SubClassOf ex:predicate some ex:object"
    expected_graph = ""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_delete_existential_restriction_with_labels():
    input_graph = """_:Ndb451c3aad3841c88d7042f29b20bea8 <http://www.w3.org/2002/07/owl#onProperty> <http://example.org/predicate> .
                     _:Ndb451c3aad3841c88d7042f29b20bea8 <http://www.w3.org/2002/07/owl#someValuesFrom> <http://example.org/object> .
                     _:Ndb451c3aad3841c88d7042f29b20bea8 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Restriction> .
                     <http://example.org/subject> <http://www.w3.org/2000/01/rdf-schema#subClassOf> _:Ndb451c3aad3841c88d7042f29b20bea8 .
                     <http://example.org/subject> <http://www.w3.org/2000/01/rdf-schema#label> "subject" .
                     <http://example.org/predicate> <http://www.w3.org/2000/01/rdf-schema#label> "predicate" .
                     <http://example.org/object> <http://www.w3.org/2000/01/rdf-schema#label> "object" ."""
    kgcl_patch = "delete 'subject' SubClassOf 'predicate' some 'object'"
    expected_graph = """<http://example.org/subject> <http://www.w3.org/2000/01/rdf-schema#label> "subject" .
                        <http://example.org/predicate> <http://www.w3.org/2000/01/rdf-schema#label> "predicate" .
                        <http://example.org/object> <http://www.w3.org/2000/01/rdf-schema#label> "object" ."""

    run_test(input_graph, kgcl_patch, expected_graph)
