from kgcl.tests.test_apply.util import run_test


def test_create_synonym_with_ids():
    input_graph = '<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .'
    kgcl_patch = (
        "create synonym 'Virus' for <http://purl.obolibrary.org/obo/NCBITaxon_2>"
    )
    expected_graph = """<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .
                        <http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.geneontology.org/formats/oboInOwl#hasSynonym> "Virus" ."""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_synonym_with_language_tag():
    input_graph = '<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .'
    kgcl_patch = (
        "create synonym 'Virus'@en for <http://purl.obolibrary.org/obo/NCBITaxon_2>"
    )
    expected_graph = """<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .
                        <http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.geneontology.org/formats/oboInOwl#hasSynonym> "Virus"@en ."""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_broad_synonym_with_ids():
    input_graph = '<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .'
    kgcl_patch = (
        "create broad synonym 'Virus' for <http://purl.obolibrary.org/obo/NCBITaxon_2>"
    )
    expected_graph = """<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .  
                        <http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym> "Virus" ."""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_broad_synonym_with_curies():
    input_graph = '<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .'
    kgcl_patch = "create broad synonym 'Virus' for obo:NCBITaxon_2"
    expected_graph = """<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .  
                        <http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym> "Virus" ."""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_broad_synonym_with_labels():
    input_graph = '<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .'
    kgcl_patch = "create broad synonym 'Virus' for 'Bacteria'"
    expected_graph = """<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .  
                        <http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym> "Virus" ."""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_exact_synonym_with_ids():
    input_graph = '<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .'
    kgcl_patch = (
        "create exact synonym 'Virus' for <http://purl.obolibrary.org/obo/NCBITaxon_2>"
    )
    expected_graph = """<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .
                        <http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.geneontology.org/formats/oboInOwl#hasExactSynonym> "Virus" ."""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_narrow_synonym_with_ids():
    input_graph = '<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .'
    kgcl_patch = (
        "create narrow synonym 'Virus' for <http://purl.obolibrary.org/obo/NCBITaxon_2>"
    )
    expected_graph = """<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .
                        <http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym> "Virus" ."""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_related_synonym_with_ids():
    input_graph = '<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .'
    kgcl_patch = "create related synonym 'Virus' for <http://purl.obolibrary.org/obo/NCBITaxon_2>"
    expected_graph = """<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .
                        <http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym> "Virus" ."""

    run_test(input_graph, kgcl_patch, expected_graph)


def test_create_related_synonym_with_language_tags_and_labels():
    input_graph = '<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .'
    kgcl_patch = "create related synonym 'Virus'@en for 'Bacteria'"
    expected_graph = """<http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.w3.org/2000/01/rdf-schema#label> "Bacteria" .
                        <http://purl.obolibrary.org/obo/NCBITaxon_2> <http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym> "Virus"@en ."""

    run_test(input_graph, kgcl_patch, expected_graph)
