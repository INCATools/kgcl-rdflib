from kgcl.tests.test_apply.util import run_test


def test_rename():
    input_graph = '<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .'
    kgcl_patch = "rename 'Bacteria' to 'Virus'"
    expected_graph = '<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Virus" .'

    run_test(input_graph, kgcl_patch, expected_graph)


def test_test_rename_with_language_tag():
    input_graph = '<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria"@en .'
    kgcl_patch = "rename 'Bacteria'@en to 'Virus'@fr"
    expected_graph = '<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Virus"@fr .'

    run_test(input_graph, kgcl_patch, expected_graph)


def test_rename_with_id():
    input_graph = """<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .
                    <http://purl.obolibrary.org/obo/NCBITaxon_8> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" ."""
    kgcl_patch = (
        "rename <http://purl.obolibrary.org/obo/NCBITaxon_2> from 'Bacteria' to 'Virus'"
    )
    expected_graph = """<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Virus" .
                        <http://purl.obolibrary.org/obo/NCBITaxon_8> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" ."""

    run_test(input_graph, kgcl_patch, expected_graph)
