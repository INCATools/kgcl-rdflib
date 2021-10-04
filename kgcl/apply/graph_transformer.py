from .kgcl_2_sparql import convert


def apply_patch(kgclInstances, graph):
    for i in kgclInstances:
        query = convert(i)
        graph.update(query)


def apply_command(kgclInstance, graph):
    query = convert(kgclInstance)
    graph.update(query)
