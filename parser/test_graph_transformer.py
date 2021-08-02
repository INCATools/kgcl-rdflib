import unittest
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD 
from rdflib import URIRef, BNode, Literal 
from rdflib.compare import to_isomorphic, graph_diff

import rdflib
import parser
import kgcl_2_sparql
import graph_transformer

def compare_graphs(actual, expected):
     actual_iso = to_isomorphic(actual)
     expected_iso = to_isomorphic(expected)
 
     if actual_iso != expected_iso: 
         _, in_first, in_second = graph_diff(actual_iso, expected_iso)
         print("The actual and expected graphs differ")
         print("----- Contents of actual graph not in expected graph -----") 
         print(in_first.serialize(format="nt").decode("utf-8")) 
         #dump_ttl_sorted(in_first)
         print("----- Contents of expected graph not in actual graph -----")
         print(in_second.serialize(format="nt").decode("utf-8")) 
         #dump_ttl_sorted(in_second)     

     assert actual_iso == expected_iso

class TestRenaming(unittest.TestCase):

    def test_command(self): 
        #KGCL statement
        command = "rename 'Bacteria' to 'RenamedBacteria'"

        #create test graph (containing only one triple)
        g = rdflib.Graph() 
        taxon = URIRef("http://purl.obolibrary.org/obo/NCBITaxon_2") 
        bacteriaLabel = Literal('Bacteria')
        g.add((taxon, RDFS.label, bacteriaLabel))

        expectedGraph = rdflib.Graph() 
        #taxon = URIRef("http://purl.obolibrary.org/obo/NCBITaxon_2") 
        renamedBacteriaLabel = Literal('RenamedBacteria')
        expectedGraph.add((taxon, RDFS.label, renamedBacteriaLabel)) 

        #parse KGCL statement into data model
        kgclModel = parser.parse(command)

        graph_transformer.transform_graph(kgclModel, g)

        compare_graphs(g,expectedGraph)

class TestNodeCreation(unittest.TestCase):

    def test_command_with_label(self): 
        #KGCL statement
        command = "create node <http://purl.obolibrary.org/obo/NCBITaxon_2> 'Bacteria'"

        #create test graph (containing only one triple)
        g = rdflib.Graph() 

        expectedGraph = rdflib.Graph() 
        taxon = URIRef("http://purl.obolibrary.org/obo/NCBITaxon_2") 
        label = Literal('Bacteria')
        expectedGraph.add((taxon, RDFS.label, label)) 

        #parse KGCL statement into data model
        kgclModel = parser.parse(command)

        graph_transformer.transform_graph(kgclModel, g)

        compare_graphs(g,expectedGraph) 

    def test_command_without_label(self): 
        #KGCL statement
        command = "create <http://purl.obolibrary.org/obo/NCBITaxon_2>"

        #create test graph (containing only one triple)
        g = rdflib.Graph() 

        expectedGraph = rdflib.Graph() 
        taxon = URIRef("http://purl.obolibrary.org/obo/NCBITaxon_2") 
        expectedGraph.add((taxon, RDF.type, OWL.Class)) 

        #parse KGCL statement into data model
        kgclModel = parser.parse(command)

        graph_transformer.transform_graph(kgclModel, g)

        compare_graphs(g,expectedGraph) 

class TestNodeDeletion(unittest.TestCase):

    def test_command_with_label(self): 
        #KGCL statement
        command = "delete 'Bacteria'"

        #create test graph (containing only one triple)
        g = rdflib.Graph() 
        taxon = URIRef("http://purl.obolibrary.org/obo/NCBITaxon_2") 
        obiClass = URIRef("http://purl.obolibrary.org/obo/OBI_0100026") 
        label = Literal('Bacteria')
        g.add((taxon, RDFS.label, label)) 
        g.add((taxon, RDF.type, OWL.Class)) 
        g.add((obiClass, RDF.type, OWL.Class)) 
        g.add((taxon, RDFS.subClassOf, obiClass))

        expectedGraph = rdflib.Graph() 
        expectedGraph.add((obiClass, RDF.type, OWL.Class)) 

        #parse KGCL statement into data model
        kgclModel = parser.parse(command)

        graph_transformer.transform_graph(kgclModel, g)

        compare_graphs(g,expectedGraph) 


    def test_command_with_id(self): 
        #KGCL statement
        command = "delete <http://purl.obolibrary.org/obo/NCBITaxon_2>"

        #create test graph (containing only one triple)
        g = rdflib.Graph() 
        taxon = URIRef("http://purl.obolibrary.org/obo/NCBITaxon_2") 
        obiClass = URIRef("http://purl.obolibrary.org/obo/OBI_0100026") 
        label = Literal('Bacteria')
        g.add((taxon, RDFS.label, label)) 
        g.add((taxon, RDF.type, OWL.Class)) 
        g.add((obiClass, RDF.type, OWL.Class)) 
        g.add((taxon, RDFS.subClassOf, obiClass))

        expectedGraph = rdflib.Graph() 
        expectedGraph.add((obiClass, RDF.type, OWL.Class)) 

        #parse KGCL statement into data model
        kgclModel = parser.parse(command)

        graph_transformer.transform_graph(kgclModel, g)

        compare_graphs(g,expectedGraph) 

class TestNodeObsoletion(unittest.TestCase):

    def test_command_with_label(self): 
        #KGCL statement
        command = "obsolete 'Bacteria'"

        #create test graph (containing only one triple)
        g = rdflib.Graph() 
        taxon = URIRef("http://purl.obolibrary.org/obo/NCBITaxon_2") 
        label = Literal('Bacteria')
        g.add((taxon, RDFS.label, label)) 
        g.add((taxon, RDF.type, OWL.Class)) 

        expectedGraph = rdflib.Graph() 
        obsoleteLabel = Literal('obsolete Bacteria') 
        true_bool = rdflib.Literal("true", datatype=XSD.boolean) 
        #trueLiteral = Literal('\"true\"^^xsd:boolean') 
        expectedGraph.add((taxon, RDFS.label,obsoleteLabel)) 
        expectedGraph.add((taxon, RDF.type, OWL.Class)) 
        expectedGraph.add((taxon, OWL.deprecated, true_bool)) 

        #parse KGCL statement into data model
        kgclModel = parser.parse(command)

        graph_transformer.transform_graph(kgclModel, g)

        compare_graphs(g,expectedGraph) 


    def test_command_with_id(self): 
        #KGCL statement
        command = "obsolete <http://purl.obolibrary.org/obo/NCBITaxon_2>"

        #create test graph (containing only one triple)
        g = rdflib.Graph() 
        taxon = URIRef("http://purl.obolibrary.org/obo/NCBITaxon_2") 
        label = Literal('Bacteria')
        g.add((taxon, RDFS.label, label)) 
        g.add((taxon, RDF.type, OWL.Class)) 

        expectedGraph = rdflib.Graph() 
        obsoleteLabel = Literal('obsolete Bacteria') 
        true_bool = rdflib.Literal("true", datatype=XSD.boolean) 
        #trueLiteral = Literal('\"true\"^^xsd:boolean') 
        expectedGraph.add((taxon, RDFS.label,obsoleteLabel)) 
        expectedGraph.add((taxon, RDF.type, OWL.Class)) 
        expectedGraph.add((taxon, OWL.deprecated, true_bool)) 

        #parse KGCL statement into data model
        kgclModel = parser.parse(command)

        graph_transformer.transform_graph(kgclModel, g)

        compare_graphs(g,expectedGraph) 

class TestNodeUnobsoletion(unittest.TestCase): 
    def test_command_with_id(self): 
        #KGCL statement
        command = "unobsolete <http://purl.obolibrary.org/obo/NCBITaxon_2>"

        #create test graph (containing only one triple) 
        g = rdflib.Graph() 
        taxon = URIRef("http://purl.obolibrary.org/obo/NCBITaxon_2") 
        obsoleteLabel = Literal('obsolete Bacteria') 
        true_bool = rdflib.Literal("true", datatype=XSD.boolean) 
        g.add((taxon, RDFS.label, obsoleteLabel)) 
        g.add((taxon, RDF.type, OWL.Class)) 
        g.add((taxon, OWL.deprecated, true_bool)) 

        expectedGraph = rdflib.Graph() 
        label = Literal('Bacteria') 
        expectedGraph.add((taxon, RDFS.label,label)) 
        expectedGraph.add((taxon, RDF.type, OWL.Class)) 

        #parse KGCL statement into data model
        kgclModel = parser.parse(command)

        graph_transformer.transform_graph(kgclModel, g)

        compare_graphs(g,expectedGraph) 

class TestNodeDeepening(unittest.TestCase): 
    def test_command(self): 
        #KGCL statement
        command = "deepen <http://example.org/targetClass> from <http://example.org/superclass> to <http://example.org/subclass>"

        #create test graph (containing only one triple) 
        g = rdflib.Graph() 
        targetClass = URIRef("http://example.org/targetClass") 
        subClass = URIRef("http://example.org/subclass") 
        superClass = URIRef("http://example.org/superclass") 

        g.add((targetClass, RDFS.subClassOf, superClass)) 
        g.add((subClass, RDFS.subClassOf, superClass)) 

        expectedGraph = rdflib.Graph() 
        expectedGraph.add((targetClass, RDFS.subClassOf, subClass)) 
        expectedGraph.add((subClass, RDFS.subClassOf, superClass)) 

        #parse KGCL statement into data model
        kgclModel = parser.parse(command)

        graph_transformer.transform_graph(kgclModel, g)

        compare_graphs(g,expectedGraph) 

class TestNodeShallowing(unittest.TestCase): 
    def test_command(self): 
        #KGCL statement
        command = "shallow <http://example.org/targetClass> from <http://example.org/subclass> to <http://example.org/superclass>"

        #create test graph (containing only one triple) 
        g = rdflib.Graph() 
        targetClass = URIRef("http://example.org/targetClass") 
        subClass = URIRef("http://example.org/subclass") 
        superClass = URIRef("http://example.org/superclass") 

        g.add((targetClass, RDFS.subClassOf, subClass)) 
        g.add((subClass, RDFS.subClassOf, superClass)) 

        expectedGraph = rdflib.Graph() 
        expectedGraph.add((targetClass, RDFS.subClassOf, superClass)) 
        expectedGraph.add((subClass, RDFS.subClassOf, superClass)) 

        #parse KGCL statement into data model
        kgclModel = parser.parse(command)

        graph_transformer.transform_graph(kgclModel, g)

        compare_graphs(g,expectedGraph) 

class TestNodeMove(unittest.TestCase): 
    def test_command(self): 
        #KGCL statement
        command = "move <http://example.org/targetClass> from <http://example.org/A> to <http://example.org/B>"

        #create test graph (containing only one triple) 
        g = rdflib.Graph() 
        targetClass = URIRef("http://example.org/targetClass") 
        A = URIRef("http://example.org/A") 

        g.add((targetClass, RDFS.subClassOf, A)) 

        B = URIRef("http://example.org/B") 

        expectedGraph = rdflib.Graph() 
        expectedGraph.add((targetClass, RDFS.subClassOf, B)) 

        #parse KGCL statement into data model
        kgclModel = parser.parse(command)

        graph_transformer.transform_graph(kgclModel, g)

        compare_graphs(g,expectedGraph) 

class TestEdgeCreation(unittest.TestCase): 
    def test_command(self): 
        #KGCL statement
        command = "create edge <http://example.org/predicate> from <http://example.org/subject> to <http://example.org/object>"

        #create test graph (containing only one triple) 
        g = rdflib.Graph() 
        subject = URIRef("http://example.org/subject") 
        predicate = URIRef("http://example.org/predicate") 
        object = URIRef("http://example.org/object") 

        expectedGraph = rdflib.Graph() 
        expectedGraph.add((subject, predicate, object)) 

        #parse KGCL statement into data model
        kgclModel = parser.parse(command)

        graph_transformer.transform_graph(kgclModel, g)

        compare_graphs(g,expectedGraph) 

class TestEdgeDeletion(unittest.TestCase): 
    def test_command(self): 
        #KGCL statement
        command = "delete edge <http://example.org/predicate> from <http://example.org/subject> to <http://example.org/object>"

        #create test graph (containing only one triple) 
        g = rdflib.Graph() 
        subject = URIRef("http://example.org/subject") 
        predicate = URIRef("http://example.org/predicate") 
        object = URIRef("http://example.org/object") 

        g.add((subject, predicate, object)) 

        expectedGraph = rdflib.Graph() 

        #parse KGCL statement into data model
        kgclModel = parser.parse(command)

        graph_transformer.transform_graph(kgclModel, g)

        compare_graphs(g,expectedGraph) 


if __name__ == '__main__':
    unittest.main()
