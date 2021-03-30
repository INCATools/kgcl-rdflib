# Auto generated from prov.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-03-30 09:26
# Schema: KGCL-PROV
#
# id: https://w3id.org/kgcl/prov
# description: See https://www.w3.org/TR/prov-o/
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml.utils.slot import Slot
from linkml.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml.utils.formatutils import camelcase, underscore, sfx
from linkml.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml.utils.curienamespace import CurieNamespace
from linkml_model.types import String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
DEFAULT_ = PROV


# Types

# Class references
class ActivityActivityId(extended_str):
    pass


@dataclass
class Activity(YAMLRoot):
    """
    a provence-generating activity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV.Activity
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "activity"
    class_model_uri: ClassVar[URIRef] = PROV.Activity

    activity_id: Union[str, ActivityActivityId] = None
    started_at_time: Optional[str] = None
    ended_at_time: Optional[str] = None
    was_informed_by: Optional[Union[str, ActivityActivityId]] = None
    was_associated_with: Optional[Union[dict, "Agent"]] = None
    used: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.activity_id is None:
            raise ValueError("activity_id must be supplied")
        if not isinstance(self.activity_id, ActivityActivityId):
            self.activity_id = ActivityActivityId(self.activity_id)

        if self.started_at_time is not None and not isinstance(self.started_at_time, str):
            self.started_at_time = str(self.started_at_time)

        if self.ended_at_time is not None and not isinstance(self.ended_at_time, str):
            self.ended_at_time = str(self.ended_at_time)

        if self.was_informed_by is not None and not isinstance(self.was_informed_by, ActivityActivityId):
            self.was_informed_by = ActivityActivityId(self.was_informed_by)

        if self.was_associated_with is not None and not isinstance(self.was_associated_with, Agent):
            self.was_associated_with = Agent(**self.was_associated_with)

        if self.used is not None and not isinstance(self.used, str):
            self.used = str(self.used)

        super().__post_init__(**kwargs)


@dataclass
class Agent(YAMLRoot):
    """
    a provence-generating agent
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV.Agent
    class_class_curie: ClassVar[str] = "prov:Agent"
    class_name: ClassVar[str] = "agent"
    class_model_uri: ClassVar[URIRef] = PROV.Agent

    acted_on_behalf_of: Optional[Union[dict, "Agent"]] = None
    was_informed_by: Optional[Union[str, ActivityActivityId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.acted_on_behalf_of is not None and not isinstance(self.acted_on_behalf_of, Agent):
            self.acted_on_behalf_of = Agent(**self.acted_on_behalf_of)

        if self.was_informed_by is not None and not isinstance(self.was_informed_by, ActivityActivityId):
            self.was_informed_by = ActivityActivityId(self.was_informed_by)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.activity_id = Slot(uri=PROV.activity_id, name="activity id", curie=PROV.curie('activity_id'),
                   model_uri=PROV.activity_id, domain=None, range=URIRef)

slots.started_at_time = Slot(uri=PROV.started_at_time, name="started at time", curie=PROV.curie('started_at_time'),
                   model_uri=PROV.started_at_time, domain=None, range=Optional[str], mappings = [PROV.startedAtTime])

slots.ended_at_time = Slot(uri=PROV.ended_at_time, name="ended at time", curie=PROV.curie('ended_at_time'),
                   model_uri=PROV.ended_at_time, domain=None, range=Optional[str], mappings = [PROV.endedAtTime])

slots.was_informed_by = Slot(uri=PROV.was_informed_by, name="was informed by", curie=PROV.curie('was_informed_by'),
                   model_uri=PROV.was_informed_by, domain=None, range=Optional[Union[str, ActivityActivityId]], mappings = [PROV.wasInformedBy])

slots.was_associated_with = Slot(uri=PROV.was_associated_with, name="was associated with", curie=PROV.curie('was_associated_with'),
                   model_uri=PROV.was_associated_with, domain=None, range=Optional[Union[dict, Agent]], mappings = [PROV.wasAssociatedWith])

slots.acted_on_behalf_of = Slot(uri=PROV.acted_on_behalf_of, name="acted on behalf of", curie=PROV.curie('acted_on_behalf_of'),
                   model_uri=PROV.acted_on_behalf_of, domain=None, range=Optional[Union[dict, Agent]], mappings = [PROV.actedOnBehalfOf])

slots.was_generated_by = Slot(uri=PROV.was_generated_by, name="was generated by", curie=PROV.curie('was_generated_by'),
                   model_uri=PROV.was_generated_by, domain=None, range=Optional[Union[str, ActivityActivityId]], mappings = [PROV.wasGeneratedBy])

slots.used = Slot(uri=PROV.used, name="used", curie=PROV.curie('used'),
                   model_uri=PROV.used, domain=Activity, range=Optional[str])
