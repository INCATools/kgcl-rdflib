# Auto generated from ontology_model.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-03-30 09:26
# Schema: kgcl-ontology-model
#
# id: https://w3id.org/kgcl/ontology
# description: A basic bare-bones model of an ontology or ontology-like structure. The purpose is not to provide a
#              complete model, rather just sufficient structure for domain and range constraints in the ocl model
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
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OM = CurieNamespace('om', 'http://w3id.org/kgcl/om')
OWL = CurieNamespace('owl', 'http://example.org/UNKNOWN/owl/')
RDF = CurieNamespace('rdf', 'http://example.org/UNKNOWN/rdf/')
DEFAULT_ = OM


# Types

# Class references
class NodeId(extended_str):
    pass


class ClassNodeId(NodeId):
    pass


class InstanceNodeId(NodeId):
    pass


class OntologyElement(YAMLRoot):
    """
    Any component of an ontology or knowledge graph
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.OntologyElement
    class_class_curie: ClassVar[str] = "om:OntologyElement"
    class_name: ClassVar[str] = "ontology element"
    class_model_uri: ClassVar[URIRef] = OM.OntologyElement


@dataclass
class PropertyValue(OntologyElement):
    """
    a property-value pair
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.PropertyValue
    class_class_curie: ClassVar[str] = "om:PropertyValue"
    class_name: ClassVar[str] = "property value"
    class_model_uri: ClassVar[URIRef] = OM.PropertyValue

    property: Optional[Union[str, NodeId]] = None
    filler: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.property is not None and not isinstance(self.property, NodeId):
            self.property = NodeId(self.property)

        if self.filler is not None and not isinstance(self.filler, str):
            self.filler = str(self.filler)

        super().__post_init__(**kwargs)


@dataclass
class Annotation(PropertyValue):
    """
    owl annotations. Not to be confused with annotations sensu GO
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.Annotation
    class_class_curie: ClassVar[str] = "om:Annotation"
    class_name: ClassVar[str] = "annotation"
    class_model_uri: ClassVar[URIRef] = OM.Annotation

    property: Optional[Union[str, NodeId]] = None
    filler: Optional[str] = None
    annotation_set: Optional[Union[dict, "Annotation"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.property is not None and not isinstance(self.property, NodeId):
            self.property = NodeId(self.property)

        if self.filler is not None and not isinstance(self.filler, str):
            self.filler = str(self.filler)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**self.annotation_set)

        super().__post_init__(**kwargs)


@dataclass
class Node(OntologyElement):
    """
    Any named entity in an ontology. May be a class, individual, property
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.Node
    class_class_curie: ClassVar[str] = "om:Node"
    class_name: ClassVar[str] = "node"
    class_model_uri: ClassVar[URIRef] = OM.Node

    id: Union[str, NodeId] = None
    name: Optional[str] = None
    annotation_set: Optional[Union[dict, Annotation]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is None:
            raise ValueError("id must be supplied")
        if not isinstance(self.id, NodeId):
            self.id = NodeId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**self.annotation_set)

        super().__post_init__(**kwargs)


@dataclass
class ClassNode(Node):
    """
    A node that is a class
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Class
    class_class_curie: ClassVar[str] = "owl:Class"
    class_name: ClassVar[str] = "class node"
    class_model_uri: ClassVar[URIRef] = OM.ClassNode

    id: Union[str, ClassNodeId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is None:
            raise ValueError("id must be supplied")
        if not isinstance(self.id, ClassNodeId):
            self.id = ClassNodeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class InstanceNode(Node):
    """
    A node that is an individual
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.NamedIndividual
    class_class_curie: ClassVar[str] = "owl:NamedIndividual"
    class_name: ClassVar[str] = "instance node"
    class_model_uri: ClassVar[URIRef] = OM.InstanceNode

    id: Union[str, InstanceNodeId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is None:
            raise ValueError("id must be supplied")
        if not isinstance(self.id, InstanceNodeId):
            self.id = InstanceNodeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Edge(OntologyElement):
    """
    A relationship between two nodes. We assume owlstar or similar for existential restrictions
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.Edge
    class_class_curie: ClassVar[str] = "om:Edge"
    class_name: ClassVar[str] = "edge"
    class_model_uri: ClassVar[URIRef] = OM.Edge

    subject: Optional[Union[str, NodeId]] = None
    edge_label: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    annotation_set: Optional[Union[dict, Annotation]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.subject is not None and not isinstance(self.subject, NodeId):
            self.subject = NodeId(self.subject)

        if self.edge_label is not None and not isinstance(self.edge_label, NodeId):
            self.edge_label = NodeId(self.edge_label)

        if self.object is not None and not isinstance(self.object, NodeId):
            self.object = NodeId(self.object)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**self.annotation_set)

        super().__post_init__(**kwargs)


class LogicalDefinition(OntologyElement):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.LogicalDefinition
    class_class_curie: ClassVar[str] = "om:LogicalDefinition"
    class_name: ClassVar[str] = "logical definition"
    class_model_uri: ClassVar[URIRef] = OM.LogicalDefinition


class Subset(OntologyElement):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.Subset
    class_class_curie: ClassVar[str] = "om:Subset"
    class_name: ClassVar[str] = "subset"
    class_model_uri: ClassVar[URIRef] = OM.Subset


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=OM.id, name="id", curie=OM.curie('id'),
                   model_uri=OM.id, domain=None, range=URIRef)

slots.name = Slot(uri=OM.name, name="name", curie=OM.curie('name'),
                   model_uri=OM.name, domain=None, range=Optional[str])

slots.subject = Slot(uri=OM.subject, name="subject", curie=OM.curie('subject'),
                   model_uri=OM.subject, domain=None, range=Optional[Union[str, NodeId]])

slots.object = Slot(uri=OM.object, name="object", curie=OM.curie('object'),
                   model_uri=OM.object, domain=None, range=Optional[Union[str, NodeId]])

slots.edge_label = Slot(uri=OM.edge_label, name="edge label", curie=OM.curie('edge_label'),
                   model_uri=OM.edge_label, domain=None, range=Optional[Union[str, NodeId]])

slots.annotation_set = Slot(uri=OM.annotation_set, name="annotation set", curie=OM.curie('annotation_set'),
                   model_uri=OM.annotation_set, domain=None, range=Optional[Union[dict, Annotation]])

slots.property = Slot(uri=OM.property, name="property", curie=OM.curie('property'),
                   model_uri=OM.property, domain=None, range=Optional[Union[str, NodeId]])

slots.filler = Slot(uri=OM.filler, name="filler", curie=OM.curie('filler'),
                   model_uri=OM.filler, domain=None, range=Optional[str])

slots.property_value_set = Slot(uri=OM.property_value_set, name="property value set", curie=OM.curie('property_value_set'),
                   model_uri=OM.property_value_set, domain=None, range=Optional[Union[Union[dict, PropertyValue], List[Union[dict, PropertyValue]]]])
