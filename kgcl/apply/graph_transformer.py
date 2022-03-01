from .kgcl_2_sparql import convert


def apply_patch(kgcl_instances, graph):
    for i in kgcl_instances:
        query = convert(i)
        graph.update(query)


def apply_command(kgcl_instance, graph):
    query = convert(kgcl_instance)
    graph.update(query)
