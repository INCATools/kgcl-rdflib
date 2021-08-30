import rdflib
from .owlstar_sublanguage import (
    get_thin_triples,
    get_atomic_existentials,
    get_triple_annotations,
    get_atomic_subsumptions,
)


# NB this returns an rdflib graph
def get_added_thin_triples(g1, g2):
    thin1 = get_thin_triples(g1)
    thin2 = get_thin_triples(g2)

    return thin2 - thin1


def get_deleted_thin_triples(g1, g2):
    thin1 = get_thin_triples(g1)
    thin2 = get_thin_triples(g2)

    return thin1 - thin2


# this is an rdflib graph too
def get_added_subsumptions(g1, g2):
    sub1 = get_atomic_subsumptions(g1)
    sub2 = get_atomic_subsumptions(g2)

    return sub2 - sub1


def get_deleted_subsumptions(g1, g2):
    sub1 = get_atomic_subsumptions(g1)
    sub2 = get_atomic_subsumptions(g2)

    return sub1 - sub2


def get_added_existentials(g1, g2):
    ex1 = set(get_atomic_existentials(g1))
    ex2 = set(get_atomic_existentials(g2))

    return ex2 - ex1


def get_deleted_existentials(g1, g2):
    ex1 = set(get_atomic_existentials(g1))
    ex2 = set(get_atomic_existentials(g2))

    return ex1 - ex2


def get_added_triple_annotations(g1, g2):
    annotations1 = set(get_triple_annotations(g1))
    annotations2 = set(get_triple_annotations(g2))

    return annotations2 - annotations1


def get_deleted_triple_annotations(g1, g2):
    annotations1 = set(get_triple_annotations(g1))
    annotations2 = set(get_triple_annotations(g2))

    return annotations1 - annotations2


if __name__ == "__main__":
    g1 = rdflib.Graph()
    g2 = rdflib.Graph()

    g1.load("n3/obi/obi_1.nt", format="nt")
    g2.load("n3/obi/obi_2.nt", format="nt")

    deleted = get_deleted_triples(g1, g2)
