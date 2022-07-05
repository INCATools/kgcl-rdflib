"""Test ontology model."""
import os
import unittest

from linkml_runtime.dumpers import JSONDumper, json_dumper

from kgcl.datamodel.ontology_model import ClassNode, OwlTypeEnum
from linkml_runtime.loaders import json_loader

from tests.util import roundtrip


class OntologyModelTestSuite(unittest.TestCase):
    """Test ontology model."""

    def test_create(self):
        """Test create."""
        c = ClassNode(id="X:1", owl_type=OwlTypeEnum.CLASS)
        c2 = roundtrip(c)
        self.assertEqual(c, c2)


