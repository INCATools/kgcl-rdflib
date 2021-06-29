import logging
import unittest
import os
from kgcl.utils import from_yaml, to_rdf, to_json
from kgcl.model.kgcl import *
from linkml_runtime.dumpers import JSONDumper

cwd = os.path.abspath(os.path.dirname(__file__))
EXAMPLE_DIR = os.path.join(cwd, '../examples')
OUTPUT_DIR = os.path.join(cwd, 'outputs')

class ChangeModelTestSuite(unittest.TestCase):

    def test_create(self):
        c = NewSynonym(id='chg12345', about='ANAT:HindLimb', new_value='hindlimb')
        print(c)
        d = JSONDumper()
        print(d.dumps(c))
