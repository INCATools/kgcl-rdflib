# Auto generated from ocl.yaml by pythongen.py version: 0.4.0
# Generation date: 2020-06-29 18:44
# Schema: ocl
#
# id: ocl
# description: A data model for describing change operations at a high level on an ontology or ontology-like
#              artefact
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from biolinkml.utils.slot import Slot
from biolinkml.utils.metamodelcore import empty_list, empty_dict, bnode
from biolinkml.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
if sys.version_info < (3, 7, 6):
    from biolinkml.utils.dataclass_extensions_375 import dataclasses_init_fn_with_kwargs
else:
    from biolinkml.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from biolinkml.utils.formatutils import camelcase, underscore, sfx
from rdflib import Namespace, URIRef
from biolinkml.utils.curienamespace import CurieNamespace
from includes.types import String

metamodel_version = "1.4.4"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
BIOLINKML = CurieNamespace('biolinkml', 'https://w3id.org/biolink/biolinkml/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
OCL = CurieNamespace('ocl', 'http://w3id.org/ocl')
OM = CurieNamespace('om', 'http://w3id.org/ocl/om')
OWL = CurieNamespace('owl', 'http://example.org/UNKNOWN/owl/')
RDF = CurieNamespace('rdf', 'http://example.org/UNKNOWN/rdf/')
DEFAULT_ = OCL


# Types

# Class references
class NodeCreationId(extended_str):
    pass


class NodeId(extended_str):
    pass


class ClassNodeId(NodeId):
    pass


class InstanceNodeId(NodeId):
    pass


class Change(YAMLRoot):
    """
    Any change perform on an ontology or knowledge graph
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.Change
    class_class_curie: ClassVar[str] = "ocl:Change"
    class_name: ClassVar[str] = "change"
    class_model_uri: ClassVar[URIRef] = OCL.Change


class SimpleChange(YAMLRoot):
    """
    A change that is about a single ontology element
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.SimpleChange
    class_class_curie: ClassVar[str] = "ocl:SimpleChange"
    class_name: ClassVar[str] = "simple change"
    class_model_uri: ClassVar[URIRef] = OCL.SimpleChange


class ComplexChange(YAMLRoot):
    """
    A change that is is a composition of other changes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.ComplexChange
    class_class_curie: ClassVar[str] = "ocl:ComplexChange"
    class_name: ClassVar[str] = "complex change"
    class_model_uri: ClassVar[URIRef] = OCL.ComplexChange


@dataclass
class Transaction(YAMLRoot):
    """
    A unified set of changes. Could be a single change, or the results of an ontology diff
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.Transaction
    class_class_curie: ClassVar[str] = "ocl:Transaction"
    class_name: ClassVar[str] = "transaction"
    class_model_uri: ClassVar[URIRef] = OCL.Transaction

    change_set: List[Union[dict, Change]] = empty_list()

    def __post_init__(self, **kwargs: Dict[str, Any]):
        self.change_set = [v if isinstance(v, Change)
                           else Change(**v) for v in self.change_set]
        super().__post_init__(**kwargs)


@dataclass
class EdgeChange(SimpleChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.EdgeChange
    class_class_curie: ClassVar[str] = "ocl:EdgeChange"
    class_name: ClassVar[str] = "edge change"
    class_model_uri: ClassVar[URIRef] = OCL.EdgeChange

    about: Optional[str] = None

class NodeMove(EdgeChange):
    """
    A node move is a combination of deleting a parent edge and adding a parent edge, where the edge label is preserved
    and the object/parent node changes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeMove
    class_class_curie: ClassVar[str] = "ocl:NodeMove"
    class_name: ClassVar[str] = "node move"
    class_model_uri: ClassVar[URIRef] = OCL.NodeMove


class EdgeLabelChange(EdgeChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.EdgeLabelChange
    class_class_curie: ClassVar[str] = "ocl:EdgeLabelChange"
    class_name: ClassVar[str] = "edge label change"
    class_model_uri: ClassVar[URIRef] = OCL.EdgeLabelChange


@dataclass
class NodeChange(SimpleChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeChange
    class_class_curie: ClassVar[str] = "ocl:NodeChange"
    class_name: ClassVar[str] = "node change"
    class_model_uri: ClassVar[URIRef] = OCL.NodeChange

    about: Optional[str] = None

@dataclass
class NodeRename(NodeChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeRename
    class_class_curie: ClassVar[str] = "ocl:NodeRename"
    class_name: ClassVar[str] = "node rename"
    class_model_uri: ClassVar[URIRef] = OCL.NodeRename

    old_value: Optional[str] = None
    new_value: Optional[str] = None

class DatatypeChange(Change):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.DatatypeChange
    class_class_curie: ClassVar[str] = "ocl:DatatypeChange"
    class_name: ClassVar[str] = "datatype change"
    class_model_uri: ClassVar[URIRef] = OCL.DatatypeChange


class NodeObsoletion(NodeChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeObsoletion
    class_class_curie: ClassVar[str] = "ocl:NodeObsoletion"
    class_name: ClassVar[str] = "node obsoletion"
    class_model_uri: ClassVar[URIRef] = OCL.NodeObsoletion


@dataclass
class NodeCreation(NodeChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeCreation
    class_class_curie: ClassVar[str] = "ocl:NodeCreation"
    class_name: ClassVar[str] = "node creation"
    class_model_uri: ClassVar[URIRef] = OCL.NodeCreation

    id: Union[str, NodeCreationId] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.id is None:
            raise ValueError(f"id must be supplied")
        if not isinstance(self.id, NodeCreationId):
            self.id = NodeCreationId(self.id)
        super().__post_init__(**kwargs)


class NodeDeletion(NodeChange):
    """
    Deletion of a node from the graph. Note it is recommended nodes are obsoleted and never merged, but this operation
    exists to represent deletions in ontologies, accidental or otherwise
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeDeletion
    class_class_curie: ClassVar[str] = "ocl:NodeDeletion"
    class_name: ClassVar[str] = "node deletion"
    class_model_uri: ClassVar[URIRef] = OCL.NodeDeletion


class NodeObsoletionWithMerge(NodeObsoletion):
    """
    An obsoletion change in which information from the obsoleted node is moved to a single target
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeObsoletionWithMerge
    class_class_curie: ClassVar[str] = "ocl:NodeObsoletionWithMerge"
    class_name: ClassVar[str] = "node obsoletion with merge"
    class_model_uri: ClassVar[URIRef] = OCL.NodeObsoletionWithMerge


class NodeObsoletionWithSplit(NodeObsoletion):
    """
    An obsoletion change in which information from the obsoleted node is moved selectively to multiple targets
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeObsoletionWithSplit
    class_class_curie: ClassVar[str] = "ocl:NodeObsoletionWithSplit"
    class_name: ClassVar[str] = "node obsoletion with split"
    class_model_uri: ClassVar[URIRef] = OCL.NodeObsoletionWithSplit


class OntologyElement(YAMLRoot):
    """
    Any component of an ontology or knowledge graph
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.OntologyElement
    class_class_curie: ClassVar[str] = "om:OntologyElement"
    class_name: ClassVar[str] = "ontology element"
    class_model_uri: ClassVar[URIRef] = OCL.OntologyElement


@dataclass
class Annotation(OntologyElement):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.Annotation
    class_class_curie: ClassVar[str] = "om:Annotation"
    class_name: ClassVar[str] = "annotation"
    class_model_uri: ClassVar[URIRef] = OCL.Annotation

    property: Optional[Union[str, NodeId]] = None
    filler: Optional[str] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.property is not None and not isinstance(self.property, NodeId):
            self.property = NodeId(self.property)
        super().__post_init__(**kwargs)


@dataclass
class Node(OntologyElement):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.Node
    class_class_curie: ClassVar[str] = "om:Node"
    class_name: ClassVar[str] = "node"
    class_model_uri: ClassVar[URIRef] = OCL.Node

    id: Union[str, NodeId] = None
    name: Optional[str] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.id is None:
            raise ValueError(f"id must be supplied")
        if not isinstance(self.id, NodeId):
            self.id = NodeId(self.id)
        super().__post_init__(**kwargs)


@dataclass
class ClassNode(Node):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Class
    class_class_curie: ClassVar[str] = "owl:Class"
    class_name: ClassVar[str] = "class node"
    class_model_uri: ClassVar[URIRef] = OCL.ClassNode

    id: Union[str, ClassNodeId] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.id is None:
            raise ValueError(f"id must be supplied")
        if not isinstance(self.id, ClassNodeId):
            self.id = ClassNodeId(self.id)
        super().__post_init__(**kwargs)


@dataclass
class InstanceNode(Node):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.NamedIndividual
    class_class_curie: ClassVar[str] = "owl:NamedIndividual"
    class_name: ClassVar[str] = "instance node"
    class_model_uri: ClassVar[URIRef] = OCL.InstanceNode

    id: Union[str, InstanceNodeId] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.id is None:
            raise ValueError(f"id must be supplied")
        if not isinstance(self.id, InstanceNodeId):
            self.id = InstanceNodeId(self.id)
        super().__post_init__(**kwargs)


@dataclass
class Edge(OntologyElement):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.Edge
    class_class_curie: ClassVar[str] = "om:Edge"
    class_name: ClassVar[str] = "edge"
    class_model_uri: ClassVar[URIRef] = OCL.Edge

    subject: Optional[Union[str, NodeId]] = None
    edge_label: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    annotation_set: Optional[Union[dict, Annotation]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.subject is not None and not isinstance(self.subject, NodeId):
            self.subject = NodeId(self.subject)
        if self.edge_label is not None and not isinstance(self.edge_label, NodeId):
            self.edge_label = NodeId(self.edge_label)
        if self.object is not None and not isinstance(self.object, NodeId):
            self.object = NodeId(self.object)
        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**self.annotation_set)
        super().__post_init__(**kwargs)



# Slots
class slots:
    pass

slots.about = Slot(uri=OCL.about, name="about", curie=OCL.curie('about'),
                      model_uri=OCL.about, domain=None, range=Optional[str])

slots.target = Slot(uri=OCL.target, name="target", curie=OCL.curie('target'),
                      model_uri=OCL.target, domain=None, range=Optional[str])

slots.old_value = Slot(uri=OCL.old_value, name="old value", curie=OCL.curie('old_value'),
                      model_uri=OCL.old_value, domain=None, range=Optional[str])

slots.new_value = Slot(uri=OCL.new_value, name="new value", curie=OCL.curie('new_value'),
                      model_uri=OCL.new_value, domain=None, range=Optional[str])

slots.change_description = Slot(uri=OCL.change_description, name="change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.change_description, domain=None, range=Optional[str])

slots.change_set = Slot(uri=OCL.change_set, name="change set", curie=OCL.curie('change_set'),
                      model_uri=OCL.change_set, domain=None, range=List[Union[dict, Change]])

slots.id = Slot(uri=OM.id, name="id", curie=OM.curie('id'),
                      model_uri=OCL.id, domain=None, range=URIRef)

slots.name = Slot(uri=OM.name, name="name", curie=OM.curie('name'),
                      model_uri=OCL.name, domain=None, range=Optional[str])

slots.subject = Slot(uri=OM.subject, name="subject", curie=OM.curie('subject'),
                      model_uri=OCL.subject, domain=None, range=Optional[Union[str, NodeId]])

slots.object = Slot(uri=OM.object, name="object", curie=OM.curie('object'),
                      model_uri=OCL.object, domain=None, range=Optional[Union[str, NodeId]])

slots.edge_label = Slot(uri=OM.edge_label, name="edge label", curie=OM.curie('edge_label'),
                      model_uri=OCL.edge_label, domain=None, range=Optional[Union[str, NodeId]])

slots.annotation_set = Slot(uri=OM.annotation_set, name="annotation set", curie=OM.curie('annotation_set'),
                      model_uri=OCL.annotation_set, domain=None, range=Optional[Union[dict, Annotation]])

slots.property = Slot(uri=OM.property, name="property", curie=OM.curie('property'),
                      model_uri=OCL.property, domain=None, range=Optional[Union[str, NodeId]])

slots.filler = Slot(uri=OM.filler, name="filler", curie=OM.curie('filler'),
                      model_uri=OCL.filler, domain=None, range=Optional[str])

slots.edge_change_about = Slot(uri=OCL.about, name="edge change_about", curie=OCL.curie('about'),
                      model_uri=OCL.edge_change_about, domain=EdgeChange, range=Optional[str])

slots.node_move_change_description = Slot(uri=OCL.change_description, name="node move_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.node_move_change_description, domain=NodeMove, range=Optional[str])

slots.edge_label_change_change_description = Slot(uri=OCL.change_description, name="edge label change_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.edge_label_change_change_description, domain=EdgeLabelChange, range=Optional[str])

slots.node_change_about = Slot(uri=OCL.about, name="node change_about", curie=OCL.curie('about'),
                      model_uri=OCL.node_change_about, domain=NodeChange, range=Optional[str])

slots.node_rename_old_value = Slot(uri=OCL.old_value, name="node rename_old value", curie=OCL.curie('old_value'),
                      model_uri=OCL.node_rename_old_value, domain=NodeRename, range=Optional[str])

slots.node_rename_new_value = Slot(uri=OCL.new_value, name="node rename_new value", curie=OCL.curie('new_value'),
                      model_uri=OCL.node_rename_new_value, domain=NodeRename, range=Optional[str])

slots.node_rename_change_description = Slot(uri=OCL.change_description, name="node rename_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.node_rename_change_description, domain=NodeRename, range=Optional[str])

slots.node_obsoletion_change_description = Slot(uri=OCL.change_description, name="node obsoletion_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.node_obsoletion_change_description, domain=NodeObsoletion, range=Optional[str])

slots.node_creation_change_description = Slot(uri=OCL.change_description, name="node creation_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.node_creation_change_description, domain=NodeCreation, range=Optional[str])

slots.node_deletion_change_description = Slot(uri=OCL.change_description, name="node deletion_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.node_deletion_change_description, domain=NodeDeletion, range=Optional[str])

slots.node_obsoletion_with_merge_target = Slot(uri=OCL.target, name="node obsoletion with merge_target", curie=OCL.curie('target'),
                      model_uri=OCL.node_obsoletion_with_merge_target, domain=NodeObsoletionWithMerge, range=Optional[str])

slots.node_obsoletion_with_merge_change_description = Slot(uri=OCL.change_description, name="node obsoletion with merge_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.node_obsoletion_with_merge_change_description, domain=NodeObsoletionWithMerge, range=Optional[str])

slots.node_obsoletion_with_split_target = Slot(uri=OCL.target, name="node obsoletion with split_target", curie=OCL.curie('target'),
                      model_uri=OCL.node_obsoletion_with_split_target, domain=NodeObsoletionWithSplit, range=List[str])

slots.node_obsoletion_with_split_change_description = Slot(uri=OCL.change_description, name="node obsoletion with split_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.node_obsoletion_with_split_change_description, domain=NodeObsoletionWithSplit, range=Optional[str])
