import parser
import kgcl_2_sparql
import rdflib

# used for local testing
def transform(kgclInstance):

    # test with obi_core
    g = rdflib.Graph()
    g.load("testData/obi_core.nt", format="nt")

    query = kgcl_2_sparql.convert(kgclInstance)
    g.update(query)
    g.serialize(destination="testData/output.nt", format="nt")


# used for local testing
def transform_set(kgclInstance):

    # test with obi_core
    g = rdflib.Graph()
    g.load("testData/obi_core.nt", format="nt")

    for i in kgclInstance:
        query = kgcl_2_sparql.convert(i)
        g.update(query)

    g.serialize(destination="testData/output.nt", format="nt")


def transform_graph(kgclInstance, graph):

    for i in kgclInstance:
        query = kgcl_2_sparql.convert(i)
        graph.update(query)
