import unittest

from kgcl_schema.grammar.parser import parse_statement
from kgcl_schema.schema import get_schemaview
from linkml_runtime.dumpers import json_dumper

from tests.cases import CASES


class ParserTestSuite(unittest.TestCase):
    def setUp(self) -> None:
        self.schemaview = get_schemaview()

    def test_parse(self):
        """Test parsing KGCL DSL into objects."""
        for txt, _, obj, _ in CASES:
            # print(txt)
            change = parse_statement(txt)
            change.id = obj.id
            change_json = json_dumper.dumps(change)
            obj_json = json_dumper.dumps(obj)
            # print(f"{change_json} == {obj_json}")
            self.assertEqual(change_json, obj_json)
            # infer_slot_value(change,
            #                 slot_name='change description',
            #                 schemaview=self.schemaview)
