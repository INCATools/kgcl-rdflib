import logging
import unittest
import os
from kgcl.utils import from_yaml, to_rdf, to_json
from kgcl.model.ontology_model import ClassNode, OwlTypeEnum
from linkml_runtime.dumpers import JSONDumper

cwd = os.path.abspath(os.path.dirname(__file__))
EXAMPLE_DIR = os.path.join(cwd, '../examples')
OUTPUT_DIR = os.path.join(cwd, 'outputs')

class OntologyModelTestSuite(unittest.TestCase):

    def test_create(self):
        c = ClassNode(id='X:1', owl_type=OwlTypeEnum.CLASS)
        print(c)
        d = JSONDumper()
        print(d.dumps(c))
