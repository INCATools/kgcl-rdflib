from kgcl.tests.test_apply.util import run_test


def test_create_annotated_edge_with_ids():
    input_graph = ""
    kgcl_patch = 'create edge <<<http://purl.obolibrary.org/obo/UBERON_0002706> <http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym> "area posterior hypothalami">> <http://www.geneontology.org/formats/oboInOwl#hasDbXref> "NeuroNames:420"'
    expected_graph = """_:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.geneontology.org/formats/oboInOwl#hasDbXref> "NeuroNames:420" .
                        _:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.w3.org/2002/07/owl#annotatedTarget> "area posterior hypothalami" .
                        _:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.w3.org/2002/07/owl#annotatedProperty> <http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym> .
                        _:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.w3.org/2002/07/owl#annotatedSource> <http://purl.obolibrary.org/obo/UBERON_0002706> .
                        _:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Axiom> ."""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_annotated_edge_with_curies():
    input_graph = ""
    kgcl_patch = 'create edge <<obo:UBERON_0002706 oboInOwl:hasRelatedSynonym "area posterior hypothalami">> oboInOwl:hasDbXref "NeuroNames:420"'
    expected_graph = """_:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.geneontology.org/formats/oboInOwl#hasDbXref> "NeuroNames:420" .
                        _:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.w3.org/2002/07/owl#annotatedTarget> "area posterior hypothalami" .
                        _:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.w3.org/2002/07/owl#annotatedProperty> <http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym> .
                        _:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.w3.org/2002/07/owl#annotatedSource> <http://purl.obolibrary.org/obo/UBERON_0002706> .
                        _:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Axiom> ."""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_annotated_edge_with_labels():
    input_graph = '<http://purl.obolibrary.org/obo/UBERON_0002706> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .'
    kgcl_patch = 'create edge <<obo:UBERON_0002706 oboInOwl:hasRelatedSynonym "area posterior hypothalami">> oboInOwl:hasDbXref "NeuroNames:420"'
    expected_graph = """<http://purl.obolibrary.org/obo/UBERON_0002706> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .
                        _:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.geneontology.org/formats/oboInOwl#hasDbXref> "NeuroNames:420" .
                        _:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.w3.org/2002/07/owl#annotatedTarget> "area posterior hypothalami" .
                        _:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.w3.org/2002/07/owl#annotatedProperty> <http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym> .
                        _:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.w3.org/2002/07/owl#annotatedSource> <http://purl.obolibrary.org/obo/UBERON_0002706> .
                        _:B87731996X2Da8f5X2D439eX2D9885X2Dcbb590a679f5 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Axiom> ."""

    run_test(input_graph, kgcl_patch, expected_graph)
