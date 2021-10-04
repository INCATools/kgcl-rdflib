from .kgcl_2_sparql import convert
import rdflib


def apply_patch(kgclInstances, graph):
    for i in kgclInstances:
        print(i)
        query = convert(i)
        print(query)
        graph.update(query)


def apply_command(kgclInstance, graph):
    query = convert(kgclInstance)
    graph.update(query)
