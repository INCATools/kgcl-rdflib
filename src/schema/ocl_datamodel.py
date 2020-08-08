# Auto generated from ocl.yaml by pythongen.py version: 0.4.0
# Generation date: 2020-08-08 11:19
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
from biolinkml.utils.metamodelcore import URIorCURIE
from includes.types import Integer, String, Uriorcurie

metamodel_version = "1.5.3"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
BIOLINKML = CurieNamespace('biolinkml', 'https://w3id.org/biolink/biolinkml/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
OCL = CurieNamespace('ocl', 'http://w3id.org/ocl')
OM = CurieNamespace('om', 'http://w3id.org/ocl/om')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = OCL


# Types
class ChangeClassType(Uriorcurie):
    """ CURIE for a class within this datamodel. E.g. ocl:NodeObsoletion """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "change class type"
    type_model_uri = OCL.ChangeClassType


# Class references
class NodeCreationId(extended_str):
    pass


class NodeId(extended_str):
    pass


class ClassNodeId(NodeId):
    pass


class InstanceNodeId(NodeId):
    pass


class ActivityActivityId(extended_str):
    pass


@dataclass
class Change(YAMLRoot):
    """
    Any change perform on an ontology or knowledge graph
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.Change
    class_class_curie: ClassVar[str] = "ocl:Change"
    class_name: ClassVar[str] = "change"
    class_model_uri: ClassVar[URIRef] = OCL.Change

    was_generated_by: Optional[Union[str, ActivityActivityId]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.was_generated_by is not None and not isinstance(self.was_generated_by, ActivityActivityId):
            self.was_generated_by = ActivityActivityId(self.was_generated_by)
        super().__post_init__(**kwargs)


@dataclass
class SimpleChange(Change):
    """
    A change that is about a single ontology element
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.SimpleChange
    class_class_curie: ClassVar[str] = "ocl:SimpleChange"
    class_name: ClassVar[str] = "simple change"
    class_model_uri: ClassVar[URIRef] = OCL.SimpleChange

    about: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None

@dataclass
class ComplexChange(Change):
    """
    A change that is is a composition of other changes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.ComplexChange
    class_class_curie: ClassVar[str] = "ocl:ComplexChange"
    class_name: ClassVar[str] = "complex change"
    class_model_uri: ClassVar[URIRef] = OCL.ComplexChange

    change_set: List[Union[dict, Change]] = empty_list()

    def __post_init__(self, **kwargs: Dict[str, Any]):
        self.change_set = [Change(*e) for e in self.change_set.items()] if isinstance(self.change_set, dict) \
                           else [v if isinstance(v, Change) else Change(**v)
                                 for v in ([self.change_set] if isinstance(self.change_set, str) else self.change_set)]
        super().__post_init__(**kwargs)


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
        self.change_set = [Change(*e) for e in self.change_set.items()] if isinstance(self.change_set, dict) \
                           else [v if isinstance(v, Change) else Change(**v)
                                 for v in ([self.change_set] if isinstance(self.change_set, str) else self.change_set)]
        super().__post_init__(**kwargs)


@dataclass
class ChangeSetSummaryStatistic(YAMLRoot):
    """
    A summary statistic for a set of changes of the same type, grouped by zero or more node properties
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.ChangeSetSummaryStatistic
    class_class_curie: ClassVar[str] = "ocl:ChangeSetSummaryStatistic"
    class_name: ClassVar[str] = "change set summary statistic"
    class_model_uri: ClassVar[URIRef] = OCL.ChangeSetSummaryStatistic

    property_value_set: List[Union[dict, "PropertyValue"]] = empty_list()

    def __post_init__(self, **kwargs: Dict[str, Any]):
        self.property_value_set = [PropertyValue(*e) for e in self.property_value_set.items()] if isinstance(self.property_value_set, dict) \
                                   else [v if isinstance(v, PropertyValue) else PropertyValue(**v)
                                         for v in ([self.property_value_set] if isinstance(self.property_value_set, str) else self.property_value_set)]
        super().__post_init__(**kwargs)


@dataclass
class EdgeChange(SimpleChange):
    """
    A change in which the entity changes is an edge
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.EdgeChange
    class_class_curie: ClassVar[str] = "ocl:EdgeChange"
    class_name: ClassVar[str] = "edge change"
    class_model_uri: ClassVar[URIRef] = OCL.EdgeChange

    about: Optional[str] = None

@dataclass
class EdgeCreation(EdgeChange):
    """
    An edge change in which a de-novo edge is created. The edge is potentially annotated in the same action.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.EdgeCreation
    class_class_curie: ClassVar[str] = "ocl:EdgeCreation"
    class_name: ClassVar[str] = "edge creation"
    class_model_uri: ClassVar[URIRef] = OCL.EdgeCreation

    subject: Optional[Union[str, NodeId]] = None
    edge_label: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    annotation_set: Optional[Union[dict, "Annotation"]] = None
    change_description: Optional[str] = None

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


@dataclass
class EdgeDeletion(EdgeChange):
    """
    An edge change in which an edge is removed. All edge annotations/properies are removed in the same action.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.EdgeDeletion
    class_class_curie: ClassVar[str] = "ocl:EdgeDeletion"
    class_name: ClassVar[str] = "edge deletion"
    class_model_uri: ClassVar[URIRef] = OCL.EdgeDeletion

    subject: Optional[Union[str, NodeId]] = None
    edge_label: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    annotation_set: Optional[Union[dict, "Annotation"]] = None
    change_description: Optional[str] = None

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


@dataclass
class EdgeObsoletion(EdgeChange):
    """
    An edge change in which an edge is obsoleted.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.EdgeObsoletion
    class_class_curie: ClassVar[str] = "ocl:EdgeObsoletion"
    class_name: ClassVar[str] = "edge obsoletion"
    class_model_uri: ClassVar[URIRef] = OCL.EdgeObsoletion

    subject: Optional[Union[str, NodeId]] = None
    edge_label: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    annotation_set: Optional[Union[dict, "Annotation"]] = None
    change_description: Optional[str] = None

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


@dataclass
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

    change_description: Optional[str] = None

@dataclass
class NodeDeepening(NodeMove):
    """
    A node move in which a node where the destination is a proper descendant of the original location. Note that here
    descendant applied not just to subclass, but edges of any edge label in the relational graph
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeDeepening
    class_class_curie: ClassVar[str] = "ocl:NodeDeepening"
    class_name: ClassVar[str] = "node deepening"
    class_model_uri: ClassVar[URIRef] = OCL.NodeDeepening

    change_description: Optional[str] = None

@dataclass
class EdgeLabelChange(EdgeChange):
    """
    An edge change where the edge label (relationship type) is modified.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.EdgeLabelChange
    class_class_curie: ClassVar[str] = "ocl:EdgeLabelChange"
    class_name: ClassVar[str] = "edge label change"
    class_model_uri: ClassVar[URIRef] = OCL.EdgeLabelChange

    change_description: Optional[str] = None

class EdgeLogicalInterpretationChange(EdgeChange):
    """
    An edge change where the subjet, object, and edge label are unchanged, but the logical interpretation changes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.EdgeLogicalInterpretationChange
    class_class_curie: ClassVar[str] = "ocl:EdgeLogicalInterpretationChange"
    class_name: ClassVar[str] = "edge logical interpretation change"
    class_model_uri: ClassVar[URIRef] = OCL.EdgeLogicalInterpretationChange


@dataclass
class NodeChange(SimpleChange):
    """
    A simple change where the change is about a node
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeChange
    class_class_curie: ClassVar[str] = "ocl:NodeChange"
    class_name: ClassVar[str] = "node change"
    class_model_uri: ClassVar[URIRef] = OCL.NodeChange

    about: Optional[str] = None

@dataclass
class NodeRename(NodeChange):
    """
    A node change where the name (aka rdfs:label) of the node changes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeRename
    class_class_curie: ClassVar[str] = "ocl:NodeRename"
    class_name: ClassVar[str] = "node rename"
    class_model_uri: ClassVar[URIRef] = OCL.NodeRename

    old_value: Optional[str] = None
    new_value: Optional[str] = None
    has_textual_diff: Optional[Union[dict, "TextualDiff"]] = None
    change_description: Optional[str] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.has_textual_diff is not None and not isinstance(self.has_textual_diff, TextualDiff):
            self.has_textual_diff = TextualDiff()
        super().__post_init__(**kwargs)


class NodeAnnotationChange(NodeChange):
    """
    A node change where the change alters node properties/annotations. TODO
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeAnnotationChange
    class_class_curie: ClassVar[str] = "ocl:NodeAnnotationChange"
    class_name: ClassVar[str] = "node annotation change"
    class_model_uri: ClassVar[URIRef] = OCL.NodeAnnotationChange


class NodeAnnotationReplacement(NodeAnnotationChange):
    """
    A node annotation change where the change replaces a particular property value. TODO
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeAnnotationReplacement
    class_class_curie: ClassVar[str] = "ocl:NodeAnnotationReplacement"
    class_name: ClassVar[str] = "node annotation replacement"
    class_model_uri: ClassVar[URIRef] = OCL.NodeAnnotationReplacement


class NodeSynonymChange(NodeChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeSynonymChange
    class_class_curie: ClassVar[str] = "ocl:NodeSynonymChange"
    class_name: ClassVar[str] = "node synonym change"
    class_model_uri: ClassVar[URIRef] = OCL.NodeSynonymChange


@dataclass
class NewSynonym(NodeSynonymChange):
    """
    A node change where a de-novo synonym is created
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NewSynonym
    class_class_curie: ClassVar[str] = "ocl:NewSynonym"
    class_name: ClassVar[str] = "new synonym"
    class_model_uri: ClassVar[URIRef] = OCL.NewSynonym

    new_value: Optional[str] = None

@dataclass
class RemoveSynonym(NodeSynonymChange):
    """
    A node change where a synonym is deleted
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.RemoveSynonym
    class_class_curie: ClassVar[str] = "ocl:RemoveSynonym"
    class_name: ClassVar[str] = "remove synonym"
    class_model_uri: ClassVar[URIRef] = OCL.RemoveSynonym

    old_value: Optional[str] = None

@dataclass
class SynonymReplacement(NodeSynonymChange):
    """
    A node change where the text of a synonym is changed
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.SynonymReplacement
    class_class_curie: ClassVar[str] = "ocl:SynonymReplacement"
    class_name: ClassVar[str] = "synonym replacement"
    class_model_uri: ClassVar[URIRef] = OCL.SynonymReplacement

    old_value: Optional[str] = None
    new_value: Optional[str] = None
    has_textual_diff: Optional[Union[dict, "TextualDiff"]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.has_textual_diff is not None and not isinstance(self.has_textual_diff, TextualDiff):
            self.has_textual_diff = TextualDiff()
        super().__post_init__(**kwargs)


class NodeTextDefinitionChange(NodeChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeTextDefinitionChange
    class_class_curie: ClassVar[str] = "ocl:NodeTextDefinitionChange"
    class_name: ClassVar[str] = "node text definition change"
    class_model_uri: ClassVar[URIRef] = OCL.NodeTextDefinitionChange


@dataclass
class NewTextDefinition(NodeTextDefinitionChange):
    """
    A node change where a de-novo text definition is created
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NewTextDefinition
    class_class_curie: ClassVar[str] = "ocl:NewTextDefinition"
    class_name: ClassVar[str] = "new text definition"
    class_model_uri: ClassVar[URIRef] = OCL.NewTextDefinition

    new_value: Optional[str] = None

@dataclass
class RemoveTextDefinition(NodeTextDefinitionChange):
    """
    A node change where a text definition is deleted
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.RemoveTextDefinition
    class_class_curie: ClassVar[str] = "ocl:RemoveTextDefinition"
    class_name: ClassVar[str] = "remove text definition"
    class_model_uri: ClassVar[URIRef] = OCL.RemoveTextDefinition

    old_value: Optional[str] = None

@dataclass
class TextDefinitionReplacement(NodeTextDefinitionChange):
    """
    A node change where a text definition is modified
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.TextDefinitionReplacement
    class_class_curie: ClassVar[str] = "ocl:TextDefinitionReplacement"
    class_name: ClassVar[str] = "text definition replacement"
    class_model_uri: ClassVar[URIRef] = OCL.TextDefinitionReplacement

    old_value: Optional[str] = None
    new_value: Optional[str] = None
    has_textual_diff: Optional[Union[dict, "TextualDiff"]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.has_textual_diff is not None and not isinstance(self.has_textual_diff, TextualDiff):
            self.has_textual_diff = TextualDiff()
        super().__post_init__(**kwargs)


class DatatypeChange(SimpleChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.DatatypeChange
    class_class_curie: ClassVar[str] = "ocl:DatatypeChange"
    class_name: ClassVar[str] = "datatype change"
    class_model_uri: ClassVar[URIRef] = OCL.DatatypeChange


class AddNodeToSubset(NodeChange):
    """
    Places a node inside a subset, by annotating that node
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.AddNodeToSubset
    class_class_curie: ClassVar[str] = "ocl:AddNodeToSubset"
    class_name: ClassVar[str] = "add node to subset"
    class_model_uri: ClassVar[URIRef] = OCL.AddNodeToSubset


@dataclass
class RemovedNodeFromSubset(NodeChange):
    """
    Removes a node from a subset, by removing an annotation
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.RemovedNodeFromSubset
    class_class_curie: ClassVar[str] = "ocl:RemovedNodeFromSubset"
    class_name: ClassVar[str] = "removed node from subset"
    class_model_uri: ClassVar[URIRef] = OCL.RemovedNodeFromSubset

    in_subset: Optional[Union[dict, "Subset"]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.in_subset is not None and not isinstance(self.in_subset, Subset):
            self.in_subset = Subset()
        super().__post_init__(**kwargs)


@dataclass
class NodeObsoletion(NodeChange):
    """
    Obsoletion of a node deprecates usage of that node, but does not delete it.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeObsoletion
    class_class_curie: ClassVar[str] = "ocl:NodeObsoletion"
    class_name: ClassVar[str] = "node obsoletion"
    class_model_uri: ClassVar[URIRef] = OCL.NodeObsoletion

    change_description: Optional[str] = None

@dataclass
class NodeUnobsoletion(NodeChange):
    """
    unobsoletion of a node deprecates usage of that node. Rarely applied.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeUnobsoletion
    class_class_curie: ClassVar[str] = "ocl:NodeUnobsoletion"
    class_name: ClassVar[str] = "node unobsoletion"
    class_model_uri: ClassVar[URIRef] = OCL.NodeUnobsoletion

    change_description: Optional[str] = None
    replaced_by: Optional[Union[str, NodeId]] = None
    consider: Optional[Union[str, NodeId]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.replaced_by is not None and not isinstance(self.replaced_by, NodeId):
            self.replaced_by = NodeId(self.replaced_by)
        if self.consider is not None and not isinstance(self.consider, NodeId):
            self.consider = NodeId(self.consider)
        super().__post_init__(**kwargs)


@dataclass
class NodeCreation(NodeChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeCreation
    class_class_curie: ClassVar[str] = "ocl:NodeCreation"
    class_name: ClassVar[str] = "node creation"
    class_model_uri: ClassVar[URIRef] = OCL.NodeCreation

    id: Union[str, NodeCreationId] = None
    name: Optional[str] = None
    annotation_set: Optional[Union[dict, "Annotation"]] = None
    change_description: Optional[str] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.id is None:
            raise ValueError(f"id must be supplied")
        if not isinstance(self.id, NodeCreationId):
            self.id = NodeCreationId(self.id)
        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**self.annotation_set)
        super().__post_init__(**kwargs)


@dataclass
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

    change_description: Optional[str] = None

@dataclass
class NodeObsoletionWithMerge(NodeObsoletion):
    """
    An obsoletion change in which information from the obsoleted node is moved to a single target.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeObsoletionWithMerge
    class_class_curie: ClassVar[str] = "ocl:NodeObsoletionWithMerge"
    class_name: ClassVar[str] = "node obsoletion with merge"
    class_model_uri: ClassVar[URIRef] = OCL.NodeObsoletionWithMerge

    target: Optional[str] = None
    about: Optional[str] = None
    change_description: Optional[str] = None

@dataclass
class NodeObsoletionWithSplit(NodeObsoletion):
    """
    An obsoletion change in which information from the obsoleted node is moved selectively to multiple targets
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.NodeObsoletionWithSplit
    class_class_curie: ClassVar[str] = "ocl:NodeObsoletionWithSplit"
    class_name: ClassVar[str] = "node obsoletion with split"
    class_model_uri: ClassVar[URIRef] = OCL.NodeObsoletionWithSplit

    target: List[str] = empty_list()
    change_description: Optional[str] = None

class TextualDiff(YAMLRoot):
    """
    A summarizing of a change on a piece of text. This could be rendered in a number of different ways
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OCL.TextualDiff
    class_class_curie: ClassVar[str] = "ocl:TextualDiff"
    class_name: ClassVar[str] = "textual diff"
    class_model_uri: ClassVar[URIRef] = OCL.TextualDiff


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
class PropertyValue(OntologyElement):
    """
    a property-value pair
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.PropertyValue
    class_class_curie: ClassVar[str] = "om:PropertyValue"
    class_name: ClassVar[str] = "property value"
    class_model_uri: ClassVar[URIRef] = OCL.PropertyValue

    property: Optional[Union[str, NodeId]] = None
    filler: Optional[str] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.property is not None and not isinstance(self.property, NodeId):
            self.property = NodeId(self.property)
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
    class_model_uri: ClassVar[URIRef] = OCL.Annotation

    property: Optional[Union[str, NodeId]] = None
    filler: Optional[str] = None
    annotation_set: Optional[Union[dict, "Annotation"]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.property is not None and not isinstance(self.property, NodeId):
            self.property = NodeId(self.property)
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
    class_model_uri: ClassVar[URIRef] = OCL.Node

    id: Union[str, NodeId] = None
    name: Optional[str] = None
    annotation_set: Optional[Union[dict, Annotation]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.id is None:
            raise ValueError(f"id must be supplied")
        if not isinstance(self.id, NodeId):
            self.id = NodeId(self.id)
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
    """
    A node that is an individual
    """
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
    """
    A relationship between two nodes. We assume owlstar or similar for existential restrictions
    """
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


class LogicalDefinition(OntologyElement):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.LogicalDefinition
    class_class_curie: ClassVar[str] = "om:LogicalDefinition"
    class_name: ClassVar[str] = "logical definition"
    class_model_uri: ClassVar[URIRef] = OCL.LogicalDefinition


class Subset(OntologyElement):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OM.Subset
    class_class_curie: ClassVar[str] = "om:Subset"
    class_name: ClassVar[str] = "subset"
    class_model_uri: ClassVar[URIRef] = OCL.Subset


@dataclass
class Activity(YAMLRoot):
    """
    a provence-generating activity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV.Activity
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "activity"
    class_model_uri: ClassVar[URIRef] = OCL.Activity

    activity_id: Union[str, ActivityActivityId]
    started_at_time: Optional[str] = None
    ended_at_time: Optional[str] = None
    was_informed_by: Optional[Union[str, ActivityActivityId]] = None
    was_associated_with: Optional[Union[dict, "Agent"]] = None
    used: Optional[str] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.activity_id is None:
            raise ValueError(f"activity_id must be supplied")
        if not isinstance(self.activity_id, ActivityActivityId):
            self.activity_id = ActivityActivityId(self.activity_id)
        if self.was_informed_by is not None and not isinstance(self.was_informed_by, ActivityActivityId):
            self.was_informed_by = ActivityActivityId(self.was_informed_by)
        if self.was_associated_with is not None and not isinstance(self.was_associated_with, Agent):
            self.was_associated_with = Agent(**self.was_associated_with)
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
    class_model_uri: ClassVar[URIRef] = OCL.Agent

    acted_on_behalf_of: Optional[Union[dict, "Agent"]] = None
    was_informed_by: Optional[Union[str, ActivityActivityId]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.acted_on_behalf_of is not None and not isinstance(self.acted_on_behalf_of, Agent):
            self.acted_on_behalf_of = Agent(**self.acted_on_behalf_of)
        if self.was_informed_by is not None and not isinstance(self.was_informed_by, ActivityActivityId):
            self.was_informed_by = ActivityActivityId(self.was_informed_by)
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

slots.has_textual_diff = Slot(uri=OCL.has_textual_diff, name="has textual diff", curie=OCL.curie('has_textual_diff'),
                      model_uri=OCL.has_textual_diff, domain=Change, range=Optional[Union[dict, "TextualDiff"]])

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

slots.property_value_set = Slot(uri=OM.property_value_set, name="property value set", curie=OM.curie('property_value_set'),
                      model_uri=OCL.property_value_set, domain=None, range=List[Union[dict, PropertyValue]])

slots.activity_id = Slot(uri=PROV.activity_id, name="activity id", curie=PROV.curie('activity_id'),
                      model_uri=OCL.activity_id, domain=None, range=URIRef)

slots.started_at_time = Slot(uri=PROV.started_at_time, name="started at time", curie=PROV.curie('started_at_time'),
                      model_uri=OCL.started_at_time, domain=None, range=Optional[str], mappings = [PROV.startedAtTime])

slots.ended_at_time = Slot(uri=PROV.ended_at_time, name="ended at time", curie=PROV.curie('ended_at_time'),
                      model_uri=OCL.ended_at_time, domain=None, range=Optional[str], mappings = [PROV.endedAtTime])

slots.was_informed_by = Slot(uri=PROV.was_informed_by, name="was informed by", curie=PROV.curie('was_informed_by'),
                      model_uri=OCL.was_informed_by, domain=None, range=Optional[Union[str, ActivityActivityId]], mappings = [PROV.wasInformedBy])

slots.was_associated_with = Slot(uri=PROV.was_associated_with, name="was associated with", curie=PROV.curie('was_associated_with'),
                      model_uri=OCL.was_associated_with, domain=None, range=Optional[Union[dict, Agent]], mappings = [PROV.wasAssociatedWith])

slots.acted_on_behalf_of = Slot(uri=PROV.acted_on_behalf_of, name="acted on behalf of", curie=PROV.curie('acted_on_behalf_of'),
                      model_uri=OCL.acted_on_behalf_of, domain=None, range=Optional[Union[dict, Agent]], mappings = [PROV.actedOnBehalfOf])

slots.was_generated_by = Slot(uri=PROV.was_generated_by, name="was generated by", curie=PROV.curie('was_generated_by'),
                      model_uri=OCL.was_generated_by, domain=None, range=Optional[Union[str, ActivityActivityId]], mappings = [PROV.wasGeneratedBy])

slots.used = Slot(uri=PROV.used, name="used", curie=PROV.curie('used'),
                      model_uri=OCL.used, domain=Activity, range=Optional[str])

slots.change_type = Slot(uri=OCL.change_type, name="change type", curie=OCL.curie('change_type'),
                      model_uri=OCL.change_type, domain=ChangeSetSummaryStatistic, range=Optional[Union[str, ChangeClassType]])

slots.count = Slot(uri=OCL.count, name="count", curie=OCL.curie('count'),
                      model_uri=OCL.count, domain=ChangeSetSummaryStatistic, range=Optional[int])

slots.change_set_summary_statistic_property_value_set = Slot(uri=OCL.property_value_set, name="change set summary statistic_property value set", curie=OCL.curie('property_value_set'),
                      model_uri=OCL.change_set_summary_statistic_property_value_set, domain=ChangeSetSummaryStatistic, range=List[Union[dict, "PropertyValue"]])

slots.in_subset = Slot(uri=OCL.in_subset, name="in subset", curie=OCL.curie('in_subset'),
                      model_uri=OCL.in_subset, domain=None, range=Optional[Union[dict, "Subset"]])

slots.remove_from_subset_in_subset = Slot(uri=OCL.in_subset, name="remove from subset_in subset", curie=OCL.curie('in_subset'),
                      model_uri=OCL.remove_from_subset_in_subset, domain=None, range=Optional[Union[dict, "Subset"]])

slots.edge_change_about = Slot(uri=OCL.about, name="edge change_about", curie=OCL.curie('about'),
                      model_uri=OCL.edge_change_about, domain=EdgeChange, range=Optional[str])

slots.edge_creation_change_description = Slot(uri=OCL.change_description, name="edge creation_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.edge_creation_change_description, domain=EdgeCreation, range=Optional[str])

slots.edge_deletion_change_description = Slot(uri=OCL.change_description, name="edge deletion_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.edge_deletion_change_description, domain=EdgeDeletion, range=Optional[str])

slots.edge_obsoletion_change_description = Slot(uri=OCL.change_description, name="edge obsoletion_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.edge_obsoletion_change_description, domain=EdgeObsoletion, range=Optional[str])

slots.node_move_change_description = Slot(uri=OCL.change_description, name="node move_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.node_move_change_description, domain=NodeMove, range=Optional[str])

slots.node_deepening_change_description = Slot(uri=OCL.change_description, name="node deepening_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.node_deepening_change_description, domain=NodeDeepening, range=Optional[str])

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

slots.replaced_by = Slot(uri=OCL.replaced_by, name="replaced by", curie=OCL.curie('replaced_by'),
                      model_uri=OCL.replaced_by, domain=NodeObsoletion, range=Optional[Union[str, NodeId]])

slots.consider = Slot(uri=OCL.consider, name="consider", curie=OCL.curie('consider'),
                      model_uri=OCL.consider, domain=NodeObsoletion, range=Optional[Union[str, NodeId]])

slots.node_unobsoletion_change_description = Slot(uri=OCL.change_description, name="node unobsoletion_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.node_unobsoletion_change_description, domain=NodeUnobsoletion, range=Optional[str])

slots.node_unobsoletion_replaced_by = Slot(uri=OCL.replaced_by, name="node unobsoletion_replaced by", curie=OCL.curie('replaced_by'),
                      model_uri=OCL.node_unobsoletion_replaced_by, domain=NodeUnobsoletion, range=Optional[Union[str, NodeId]])

slots.node_unobsoletion_consider = Slot(uri=OCL.consider, name="node unobsoletion_consider", curie=OCL.curie('consider'),
                      model_uri=OCL.node_unobsoletion_consider, domain=NodeUnobsoletion, range=Optional[Union[str, NodeId]])

slots.node_creation_change_description = Slot(uri=OCL.change_description, name="node creation_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.node_creation_change_description, domain=NodeCreation, range=Optional[str])

slots.node_deletion_change_description = Slot(uri=OCL.change_description, name="node deletion_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.node_deletion_change_description, domain=NodeDeletion, range=Optional[str])

slots.node_obsoletion_with_merge_target = Slot(uri=OCL.target, name="node obsoletion with merge_target", curie=OCL.curie('target'),
                      model_uri=OCL.node_obsoletion_with_merge_target, domain=NodeObsoletionWithMerge, range=Optional[str])

slots.node_obsoletion_with_merge_about = Slot(uri=OCL.about, name="node obsoletion with merge_about", curie=OCL.curie('about'),
                      model_uri=OCL.node_obsoletion_with_merge_about, domain=NodeObsoletionWithMerge, range=Optional[str])

slots.node_obsoletion_with_merge_change_description = Slot(uri=OCL.change_description, name="node obsoletion with merge_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.node_obsoletion_with_merge_change_description, domain=NodeObsoletionWithMerge, range=Optional[str])

slots.node_obsoletion_with_split_target = Slot(uri=OCL.target, name="node obsoletion with split_target", curie=OCL.curie('target'),
                      model_uri=OCL.node_obsoletion_with_split_target, domain=NodeObsoletionWithSplit, range=List[str])

slots.node_obsoletion_with_split_change_description = Slot(uri=OCL.change_description, name="node obsoletion with split_change description", curie=OCL.curie('change_description'),
                      model_uri=OCL.node_obsoletion_with_split_change_description, domain=NodeObsoletionWithSplit, range=Optional[str])
