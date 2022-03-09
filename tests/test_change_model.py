import logging
import os
import unittest

from linkml_runtime.dumpers import JSONDumper

from kgcl.model.kgcl import *
from kgcl.model.ontology_model import Edge, Node, NodeId
from kgcl.utils import from_yaml, to_json, to_rdf

cwd = os.path.abspath(os.path.dirname(__file__))
EXAMPLE_DIR = os.path.join(cwd, "../examples")
OUTPUT_DIR = os.path.join(cwd, "outputs")


class ChangeModelTestSuite(unittest.TestCase):
    def test_create(self):
        c = NewSynonym(id="chg12345", about_node="ANAT:HindLimb", new_value="hindlimb")
        print(c)
        d = JSONDumper()
        print(d.dumps(c))

    def test_predicate_change(self):
        c = PredicateChange(
            id="chg4",
            about_edge=Edge(subject="ANAT:Hand", object="ANAT:Forelimb"),
            new_value="BFO:000005",
        )
        print(c)
        d = JSONDumper()
        print(d.dumps(c))
