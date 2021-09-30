# Auto generated from ontology_model.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-09-23 19:44
# Schema: kgcl-ontology-model
#
# id: https://w3id.org/kgcl/ontology
# description: A basic bare-bones model of an ontology or ontology-like structure. The purpose is not to provide a
#              complete model, rather just sufficient structure for domain and range constraints in the ocl model
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OIO = CurieNamespace('oio', 'http://www.geneontology.org/formats/oboInOwl#')
OM = CurieNamespace('om', 'http://w3id.org/kgcl/om/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
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
    property_type: Optional[str] = None
    filler_type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.property is not None and not isinstance(self.property, NodeId):
            self.property = NodeId(self.property)

        if self.filler is not None and not isinstance(self.filler, str):
            self.filler = str(self.filler)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**as_dict(self.annotation_set))

        if self.property_type is not None and not isinstance(self.property_type, str):
            self.property_type = str(self.property_type)

        if self.filler_type is not None and not isinstance(self.filler_type, str):
            self.filler_type = str(self.filler_type)

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
    owl_type: Optional[Union[str, "OwlTypeEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeId):
            self.id = NodeId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**as_dict(self.annotation_set))

        if self.owl_type is not None and not isinstance(self.owl_type, OwlTypeEnum):
            self.owl_type = OwlTypeEnum(self.owl_type)

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
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
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
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
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
    predicate: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    subject_representation: Optional[str] = None
    predicate_representation: Optional[str] = None
    object_representation: Optional[str] = None
    annotation_set: Optional[Union[dict, Annotation]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.subject is not None and not isinstance(self.subject, NodeId):
            self.subject = NodeId(self.subject)

        if self.predicate is not None and not isinstance(self.predicate, NodeId):
            self.predicate = NodeId(self.predicate)

        if self.object is not None and not isinstance(self.object, NodeId):
            self.object = NodeId(self.object)

        if self.subject_representation is not None and not isinstance(self.subject_representation, str):
            self.subject_representation = str(self.subject_representation)

        if self.predicate_representation is not None and not isinstance(self.predicate_representation, str):
            self.predicate_representation = str(self.predicate_representation)

        if self.object_representation is not None and not isinstance(self.object_representation, str):
            self.object_representation = str(self.object_representation)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**as_dict(self.annotation_set))

        super().__post_init__(**kwargs)


class LogicalDefinition(OntologyElement):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.LogicalDefinition
    class_class_curie: ClassVar[str] = "om:LogicalDefinition"
    class_name: ClassVar[str] = "logical definition"
    class_model_uri: ClassVar[URIRef] = OM.LogicalDefinition


class OntologySubset(OntologyElement):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.OntologySubset
    class_class_curie: ClassVar[str] = "om:OntologySubset"
    class_name: ClassVar[str] = "ontology subset"
    class_model_uri: ClassVar[URIRef] = OM.OntologySubset


# Enumerations
class OwlTypeEnum(EnumDefinitionImpl):

    CLASS = PermissibleValue(text="CLASS",
                                 meaning=OWL.Class)
    OBJECT_PROPERTY = PermissibleValue(text="OBJECT_PROPERTY",
                                                     meaning=OWL.ObjectProperty)
    NAMED_INDIVIDUAL = PermissibleValue(text="NAMED_INDIVIDUAL",
                                                       meaning=OWL.NamedIndividual)

    _defn = EnumDefinition(
        name="OwlTypeEnum",
    )

class SynonymScopeEnum(EnumDefinitionImpl):

    related = PermissibleValue(text="related",
                                     meaning=OIO.hasNarrowSynonym)
    broad = PermissibleValue(text="broad",
                                 meaning=OIO.hasBroadSynonym)
    narrow = PermissibleValue(text="narrow",
                                   meaning=OIO.hasNarrowSynonym)
    exact = PermissibleValue(text="exact",
                                 meaning=OIO.hasExactSynonym)

    _defn = EnumDefinition(
        name="SynonymScopeEnum",
    )

# Slots
class slots:
    pass

slots.owl_type = Slot(uri=OM.owl_type, name="owl type", curie=OM.curie('owl_type'),
                   model_uri=OM.owl_type, domain=None, range=Optional[Union[str, "OwlTypeEnum"]])

slots.name = Slot(uri=OM.name, name="name", curie=OM.curie('name'),
                   model_uri=OM.name, domain=None, range=Optional[str])

slots.subject = Slot(uri=OM.subject, name="subject", curie=OM.curie('subject'),
                   model_uri=OM.subject, domain=None, range=Optional[Union[str, NodeId]])

slots.object = Slot(uri=OM.object, name="object", curie=OM.curie('object'),
                   model_uri=OM.object, domain=None, range=Optional[Union[str, NodeId]])

slots.predicate = Slot(uri=OM.predicate, name="predicate", curie=OM.curie('predicate'),
                   model_uri=OM.predicate, domain=None, range=Optional[Union[str, NodeId]])

slots.annotation_set = Slot(uri=OM.annotation_set, name="annotation set", curie=OM.curie('annotation_set'),
                   model_uri=OM.annotation_set, domain=None, range=Optional[Union[dict, Annotation]])

slots.property = Slot(uri=OM.property, name="property", curie=OM.curie('property'),
                   model_uri=OM.property, domain=None, range=Optional[Union[str, NodeId]])

slots.filler = Slot(uri=OM.filler, name="filler", curie=OM.curie('filler'),
                   model_uri=OM.filler, domain=None, range=Optional[str])

slots.property_type = Slot(uri=OM.property_type, name="property type", curie=OM.curie('property_type'),
                   model_uri=OM.property_type, domain=None, range=Optional[str])

slots.filler_type = Slot(uri=OM.filler_type, name="filler type", curie=OM.curie('filler_type'),
                   model_uri=OM.filler_type, domain=None, range=Optional[str])

slots.subject_representation = Slot(uri=OM.subject_representation, name="subject representation", curie=OM.curie('subject_representation'),
                   model_uri=OM.subject_representation, domain=None, range=Optional[str])

slots.predicate_representation = Slot(uri=OM.predicate_representation, name="predicate representation", curie=OM.curie('predicate_representation'),
                   model_uri=OM.predicate_representation, domain=None, range=Optional[str])

slots.object_representation = Slot(uri=OM.object_representation, name="object representation", curie=OM.curie('object_representation'),
                   model_uri=OM.object_representation, domain=None, range=Optional[str])

slots.property_value_set = Slot(uri=OM.property_value_set, name="property value set", curie=OM.curie('property_value_set'),
                   model_uri=OM.property_value_set, domain=None, range=Optional[Union[Union[dict, PropertyValue], List[Union[dict, PropertyValue]]]])
