from .kgcl_2_sparql import convert
import rdflib


# def transform_graph(kgclInstances, graph):
def apply_patch(kgclInstances, graph):
    for i in kgclInstances:
        print(i)
        query = convert(i)
        print(query)
        graph.update(query)


# def transform_single(kgclInstance, graph):
def apply_command(kgclInstance, graph):
    query = convert(kgclInstance)
    graph.update(query)
