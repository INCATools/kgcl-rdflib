import logging
import unittest
import os
from kgcl.utils import from_yaml, to_rdf, to_json
#from test import EXAMPLE_DIR
cwd = os.path.abspath(os.path.dirname(__file__))
EXAMPLE_DIR = os.path.join(cwd, '../examples')
OUTPUT_DIR = os.path.join(cwd, 'outputs')

class ConversionTestSuite(unittest.TestCase):

    def setUp(self) -> None:
        self.session = from_yaml(f'{EXAMPLE_DIR}/de-novo.yaml')

    def test_convert(self):
        print(f'Session: {self.session}')
        json = to_json(self.session)
        ofn = os.path.join(OUTPUT_DIR, "test.json")
        with open(ofn, "w") as stream:
            stream.write(json)
