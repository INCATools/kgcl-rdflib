import rdflib
from rdflib.namespace import (
    RDFS,
    OWL,
    RDF,
)
from rdflib import BNode


def get_thin_triples(g):
    # NOTE: using FILTER(!isBlank(?subject)), etc slows things down considerably
    query = """
    SELECT DISTINCT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object .
    }"""

    qres = g.query(query)
    axioms = []

    for row in qres:
        if (
            not isinstance(row.subject, BNode)
            and not isinstance(row.predicate, BNode)
            and not isinstance(row.object, BNode)
        ):
            axioms.append((row.subject, row.predicate, row.object))

    return axioms


def get_atomic_subclassOf_axioms(g):
    # these are handled as normal triples

    query = """
    SELECT DISTINCT ?subclass ?superclass
    WHERE {
        ?subclass rdfs:subClassOf ?superclass .
    }"""

    qres = g.query(query)

    for row in qres:
        if not isinstance(row.subclass, BNode) and not isinstance(
            row.superclass, BNode
        ):
            print(f"{row.subclass} is-a {row.superclass}")


def get_atomic_existential_restrictions(g):
    query = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT DISTINCT ?subclass ?property ?filler
    WHERE {
        ?subclass rdfs:subClassOf ?b .
        ?b rdf:type owl:Restriction .
        ?b owl:onProperty ?property .
        ?b owl:someValuesFrom ?filler .
        FILTER(!isBlank(?subclass))
    }"""

    qres = g.query(query)
    axioms = []

    for row in qres:
        if (
            not isinstance(row.subclass, BNode)
            and not isinstance(row.property, BNode)
            and not isinstance(row.filler, BNode)
        ):
            axioms.append((row.subclass, row.property, row.filler))
    return axioms


def atomic_existential_2_owlstar(axiom):
    subject = axiom[0]
    predicate = axiom[1]
    object = axiom[2]

    return (
        f"<<{subject} {predicate} {object}>> os:interpretation os:AllSomeInterpretation"
    )


def get_triple_annotations(g):
    query = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT DISTINCT ?source ?property ?target ?aproperty ?annotation ?b
    WHERE {
        ?b ?aproperty ?annotation .
        ?b owl:annotatedTarget ?target .
        ?b owl:annotatedProperty ?property .
        ?b owl:annotatedSource ?source .
        ?b rdf:type ?type .
        FILTER(?aproperty != owl:annotatedProperty)
        FILTER(?aproperty != owl:annotatedTarget)
        FILTER(?aproperty != owl:annotatedSource)
        FILTER(?aproperty != rdf:type)

    }"""

    qres = g.query(query)
    axioms = []

    for row in qres:
        if (
            not isinstance(row.source, BNode)
            and not isinstance(row.property, BNode)
            and not isinstance(row.target, BNode)
            and not isinstance(row.aproperty, BNode)
            and not isinstance(row.annotation, BNode)
        ):
            axioms.append(
                (row.source, row.property, row.target, row.aproperty, row.annotation)
            )
    return axioms


def annotation_2_owlstar(triple):
    source = triple[0]
    property = triple[1]
    object = triple[2]
    annotation_property = triple[3]
    annotation = triple[4]
    return f"<<{source} {property} {object}>> {annotation_property} {annotation}"


if __name__ == "__main__":
    g = rdflib.Graph()
    g.load("n3/obi/obi_1.nt", format="nt")
    # g.load("n3/uberon/uberon_1.nt", format="nt")

    # get_atomic_subclassOf_axioms(g)

    existentials = get_atomic_existential_restrictions(g)
    annotations = get_triple_annotations(g)
    print(len(existentials))
    print(len(annotations))
    # triples = get_thin_triples(g)
    # print(len(triples))
