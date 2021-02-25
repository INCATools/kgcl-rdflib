# Auto generated from kgcl.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-02-25 09:50
# Schema: kgcl
#
# id: https://w3id.org/kgcl
# description: A data model for describing change operations at a high level on an ontology or ontology-like
#              artefact, e.g Knowledge Graph. See
#              [https://github.com/cmungall/knowledge-graph-change-language](https://github.com/cmungall/knowledge-graph-change-language)
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from biolinkml.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from biolinkml.utils.slot import Slot
from biolinkml.utils.metamodelcore import empty_list, empty_dict, bnode
from biolinkml.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
if sys.version_info < (3, 7, 6):
    from biolinkml.utils.dataclass_extensions_375 import dataclasses_init_fn_with_kwargs
else:
    from biolinkml.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from biolinkml.utils.formatutils import camelcase, underscore, sfx
from biolinkml.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from biolinkml.utils.curienamespace import CurieNamespace
from . ontology_model import Annotation, NodeId, PropertyValue, Subset
from . prov import ActivityActivityId
from biolinkml.utils.metamodelcore import URIorCURIE
from includes.types import Integer, String, Uriorcurie

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
IAO = CurieNamespace('IAO', 'http://purl.obolibrary.org/obo/IAO_')
BIOLINKML = CurieNamespace('biolinkml', 'https://w3id.org/biolink/biolinkml/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
KGCL = CurieNamespace('kgcl', 'http://w3id.org/kgcl')
OIO = CurieNamespace('oio', 'http://www.geneontology.org/formats/oboInOwl#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = KGCL


# Types
class ChangeClassType(Uriorcurie):
    """ CURIE for a class within this datamodel. E.g. kgcl:NodeObsoletion """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "change class type"
    type_model_uri = KGCL.ChangeClassType


# Class references
class NodeCreationId(extended_str):
    pass


@dataclass
class Change(YAMLRoot):
    """
    Any change perform on an ontology or knowledge graph
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.Change
    class_class_curie: ClassVar[str] = "kgcl:Change"
    class_name: ClassVar[str] = "change"
    class_model_uri: ClassVar[URIRef] = KGCL.Change

    was_generated_by: Optional[Union[str, ActivityActivityId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.was_generated_by is not None and not isinstance(self.was_generated_by, ActivityActivityId):
            self.was_generated_by = ActivityActivityId(self.was_generated_by)

        super().__post_init__(**kwargs)


@dataclass
class SimpleChange(Change):
    """
    A change that is about a single ontology element
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.SimpleChange
    class_class_curie: ClassVar[str] = "kgcl:SimpleChange"
    class_name: ClassVar[str] = "simple change"
    class_model_uri: ClassVar[URIRef] = KGCL.SimpleChange

    about: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.about is not None and not isinstance(self.about, str):
            self.about = str(self.about)

        if self.old_value is not None and not isinstance(self.old_value, str):
            self.old_value = str(self.old_value)

        if self.new_value is not None and not isinstance(self.new_value, str):
            self.new_value = str(self.new_value)

        super().__post_init__(**kwargs)


@dataclass
class ComplexChange(Change):
    """
    A change that is is a composition of other changes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.ComplexChange
    class_class_curie: ClassVar[str] = "kgcl:ComplexChange"
    class_name: ClassVar[str] = "complex change"
    class_model_uri: ClassVar[URIRef] = KGCL.ComplexChange

    change_set: Optional[Union[Union[dict, Change], List[Union[dict, Change]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.change_set is None:
            self.change_set = []
        if not isinstance(self.change_set, list):
            self.change_set = [self.change_set]
        self.change_set = [v if isinstance(v, Change) else Change(**v) for v in self.change_set]

        super().__post_init__(**kwargs)


@dataclass
class MultiNodeObsoletion(ComplexChange):
    """
    A complex change consisting of multiple obsoletions.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.MultiNodeObsoletion
    class_class_curie: ClassVar[str] = "kgcl:MultiNodeObsoletion"
    class_name: ClassVar[str] = "multi node obsoletion"
    class_model_uri: ClassVar[URIRef] = KGCL.MultiNodeObsoletion

    change_set: Optional[Union[Union[dict, "NodeObsoletion"], List[Union[dict, "NodeObsoletion"]]]] = empty_list()
    change_description: Optional[str] = None
    associated_change_set: Optional[Union[Union[dict, Change], List[Union[dict, Change]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.change_set is None:
            self.change_set = []
        if not isinstance(self.change_set, list):
            self.change_set = [self.change_set]
        self.change_set = [v if isinstance(v, NodeObsoletion) else NodeObsoletion(**v) for v in self.change_set]

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        if self.associated_change_set is None:
            self.associated_change_set = []
        if not isinstance(self.associated_change_set, list):
            self.associated_change_set = [self.associated_change_set]
        self.associated_change_set = [v if isinstance(v, Change) else Change(**v) for v in self.associated_change_set]

        super().__post_init__(**kwargs)


@dataclass
class Transaction(YAMLRoot):
    """
    A unified set of changes. Could be a single change, or the results of an ontology diff
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.Transaction
    class_class_curie: ClassVar[str] = "kgcl:Transaction"
    class_name: ClassVar[str] = "transaction"
    class_model_uri: ClassVar[URIRef] = KGCL.Transaction

    change_set: Optional[Union[Union[dict, Change], List[Union[dict, Change]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.change_set is None:
            self.change_set = []
        if not isinstance(self.change_set, list):
            self.change_set = [self.change_set]
        self.change_set = [v if isinstance(v, Change) else Change(**v) for v in self.change_set]

        super().__post_init__(**kwargs)


@dataclass
class ChangeSetSummaryStatistic(YAMLRoot):
    """
    A summary statistic for a set of changes of the same type, grouped by zero or more node properties
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.ChangeSetSummaryStatistic
    class_class_curie: ClassVar[str] = "kgcl:ChangeSetSummaryStatistic"
    class_name: ClassVar[str] = "change set summary statistic"
    class_model_uri: ClassVar[URIRef] = KGCL.ChangeSetSummaryStatistic

    change_type: Optional[Union[str, ChangeClassType]] = None
    count: Optional[int] = None
    property_value_set: Optional[Union[Union[dict, PropertyValue], List[Union[dict, PropertyValue]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.change_type is not None and not isinstance(self.change_type, ChangeClassType):
            self.change_type = ChangeClassType(self.change_type)

        if self.count is not None and not isinstance(self.count, int):
            self.count = int(self.count)

        if self.property_value_set is None:
            self.property_value_set = []
        if not isinstance(self.property_value_set, list):
            self.property_value_set = [self.property_value_set]
        self.property_value_set = [v if isinstance(v, PropertyValue) else PropertyValue(**v) for v in self.property_value_set]

        super().__post_init__(**kwargs)


class ChangeMixin(YAMLRoot):
    """
    root class for all change mixins
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.ChangeMixin
    class_class_curie: ClassVar[str] = "kgcl:ChangeMixin"
    class_name: ClassVar[str] = "change mixin"
    class_model_uri: ClassVar[URIRef] = KGCL.ChangeMixin


class Obsoletion(ChangeMixin):
    """
    Obsoletion of an element deprecates usage of that element, but does not delete that element.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.Obsoletion
    class_class_curie: ClassVar[str] = "kgcl:Obsoletion"
    class_name: ClassVar[str] = "obsoletion"
    class_model_uri: ClassVar[URIRef] = KGCL.Obsoletion


class Unobsoletion(ChangeMixin):
    """
    Opposite operation of obsoletion. Rarely performed.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.Unobsoletion
    class_class_curie: ClassVar[str] = "kgcl:Unobsoletion"
    class_name: ClassVar[str] = "unobsoletion"
    class_model_uri: ClassVar[URIRef] = KGCL.Unobsoletion


class Deletion(ChangeMixin):
    """
    Removal of an element.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.Deletion
    class_class_curie: ClassVar[str] = "kgcl:Deletion"
    class_name: ClassVar[str] = "deletion"
    class_model_uri: ClassVar[URIRef] = KGCL.Deletion


class Creation(ChangeMixin):
    """
    Creation of an element.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.Creation
    class_class_curie: ClassVar[str] = "kgcl:Creation"
    class_name: ClassVar[str] = "creation"
    class_model_uri: ClassVar[URIRef] = KGCL.Creation


@dataclass
class AddToSubset(ChangeMixin):
    """
    placing an element inside a subset
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.AddToSubset
    class_class_curie: ClassVar[str] = "kgcl:AddToSubset"
    class_name: ClassVar[str] = "add to subset"
    class_model_uri: ClassVar[URIRef] = KGCL.AddToSubset

    in_subset: Optional[Union[dict, Subset]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_subset is not None and not isinstance(self.in_subset, Subset):
            self.in_subset = Subset()

        super().__post_init__(**kwargs)


@dataclass
class RemoveFromSubset(ChangeMixin):
    """
    removing an element from a subset
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.RemoveFromSubset
    class_class_curie: ClassVar[str] = "kgcl:RemoveFromSubset"
    class_name: ClassVar[str] = "remove from subset"
    class_model_uri: ClassVar[URIRef] = KGCL.RemoveFromSubset

    in_subset: Optional[Union[dict, Subset]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_subset is not None and not isinstance(self.in_subset, Subset):
            self.in_subset = Subset()

        super().__post_init__(**kwargs)


@dataclass
class EdgeChange(SimpleChange):
    """
    A change in which the entity changes is an edge
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.EdgeChange
    class_class_curie: ClassVar[str] = "kgcl:EdgeChange"
    class_name: ClassVar[str] = "edge change"
    class_model_uri: ClassVar[URIRef] = KGCL.EdgeChange

    about: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.about is not None and not isinstance(self.about, str):
            self.about = str(self.about)

        super().__post_init__(**kwargs)


@dataclass
class EdgeCreation(EdgeChange):
    """
    An edge change in which a de-novo edge is created. The edge is potentially annotated in the same action.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.EdgeCreation
    class_class_curie: ClassVar[str] = "kgcl:EdgeCreation"
    class_name: ClassVar[str] = "edge creation"
    class_model_uri: ClassVar[URIRef] = KGCL.EdgeCreation

    subject: Optional[Union[str, NodeId]] = None
    edge_label: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    annotation_set: Optional[Union[dict, Annotation]] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.subject is not None and not isinstance(self.subject, NodeId):
            self.subject = NodeId(self.subject)

        if self.edge_label is not None and not isinstance(self.edge_label, NodeId):
            self.edge_label = NodeId(self.edge_label)

        if self.object is not None and not isinstance(self.object, NodeId):
            self.object = NodeId(self.object)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**self.annotation_set)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class EdgeDeletion(EdgeChange):
    """
    An edge change in which an edge is removed. All edge annotations/properies are removed in the same action.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.EdgeDeletion
    class_class_curie: ClassVar[str] = "kgcl:EdgeDeletion"
    class_name: ClassVar[str] = "edge deletion"
    class_model_uri: ClassVar[URIRef] = KGCL.EdgeDeletion

    subject: Optional[Union[str, NodeId]] = None
    edge_label: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    annotation_set: Optional[Union[dict, Annotation]] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.subject is not None and not isinstance(self.subject, NodeId):
            self.subject = NodeId(self.subject)

        if self.edge_label is not None and not isinstance(self.edge_label, NodeId):
            self.edge_label = NodeId(self.edge_label)

        if self.object is not None and not isinstance(self.object, NodeId):
            self.object = NodeId(self.object)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**self.annotation_set)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class EdgeObsoletion(EdgeChange):
    """
    An edge change in which an edge is obsoleted.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.EdgeObsoletion
    class_class_curie: ClassVar[str] = "kgcl:EdgeObsoletion"
    class_name: ClassVar[str] = "edge obsoletion"
    class_model_uri: ClassVar[URIRef] = KGCL.EdgeObsoletion

    subject: Optional[Union[str, NodeId]] = None
    edge_label: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    annotation_set: Optional[Union[dict, Annotation]] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.subject is not None and not isinstance(self.subject, NodeId):
            self.subject = NodeId(self.subject)

        if self.edge_label is not None and not isinstance(self.edge_label, NodeId):
            self.edge_label = NodeId(self.edge_label)

        if self.object is not None and not isinstance(self.object, NodeId):
            self.object = NodeId(self.object)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**self.annotation_set)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class NodeMove(EdgeChange):
    """
    A node move is a combination of deleting a parent edge and adding a parent edge, where the edge label is preserved
    and the object/parent node changes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeMove
    class_class_curie: ClassVar[str] = "kgcl:NodeMove"
    class_name: ClassVar[str] = "node move"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeMove

    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class NodeDeepening(NodeMove):
    """
    A node move in which a node where the destination is a proper descendant of the original location. Note that here
    descendant applied not just to subclass, but edges of any edge label in the relational graph
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeDeepening
    class_class_curie: ClassVar[str] = "kgcl:NodeDeepening"
    class_name: ClassVar[str] = "node deepening"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeDeepening

    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class NodeShallowing(NodeMove):
    """
    The opposite of node deepening
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeShallowing
    class_class_curie: ClassVar[str] = "kgcl:NodeShallowing"
    class_name: ClassVar[str] = "node shallowing"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeShallowing

    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class EdgeLabelChange(EdgeChange):
    """
    An edge change where the edge label (relationship type) is modified.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.EdgeLabelChange
    class_class_curie: ClassVar[str] = "kgcl:EdgeLabelChange"
    class_name: ClassVar[str] = "edge label change"
    class_model_uri: ClassVar[URIRef] = KGCL.EdgeLabelChange

    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


class EdgeLogicalInterpretationChange(EdgeChange):
    """
    An edge change where the subjet, object, and edge label are unchanged, but the logical interpretation changes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.EdgeLogicalInterpretationChange
    class_class_curie: ClassVar[str] = "kgcl:EdgeLogicalInterpretationChange"
    class_name: ClassVar[str] = "edge logical interpretation change"
    class_model_uri: ClassVar[URIRef] = KGCL.EdgeLogicalInterpretationChange


@dataclass
class NodeChange(SimpleChange):
    """
    A simple change where the change is about a node
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeChange
    class_class_curie: ClassVar[str] = "kgcl:NodeChange"
    class_name: ClassVar[str] = "node change"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeChange

    about: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.about is not None and not isinstance(self.about, str):
            self.about = str(self.about)

        super().__post_init__(**kwargs)


@dataclass
class NodeRename(NodeChange):
    """
    A node change where the name (aka rdfs:label) of the node changes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeRename
    class_class_curie: ClassVar[str] = "kgcl:NodeRename"
    class_name: ClassVar[str] = "node rename"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeRename

    old_value: Optional[str] = None
    new_value: Optional[str] = None
    has_textual_diff: Optional[Union[dict, "TextualDiff"]] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.old_value is not None and not isinstance(self.old_value, str):
            self.old_value = str(self.old_value)

        if self.new_value is not None and not isinstance(self.new_value, str):
            self.new_value = str(self.new_value)

        if self.has_textual_diff is not None and not isinstance(self.has_textual_diff, TextualDiff):
            self.has_textual_diff = TextualDiff()

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


class NodeAnnotationChange(NodeChange):
    """
    A node change where the change alters node properties/annotations. TODO
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeAnnotationChange
    class_class_curie: ClassVar[str] = "kgcl:NodeAnnotationChange"
    class_name: ClassVar[str] = "node annotation change"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeAnnotationChange


class NodeAnnotationReplacement(NodeAnnotationChange):
    """
    A node annotation change where the change replaces a particular property value. TODO
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeAnnotationReplacement
    class_class_curie: ClassVar[str] = "kgcl:NodeAnnotationReplacement"
    class_name: ClassVar[str] = "node annotation replacement"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeAnnotationReplacement


class NodeSynonymChange(NodeChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeSynonymChange
    class_class_curie: ClassVar[str] = "kgcl:NodeSynonymChange"
    class_name: ClassVar[str] = "node synonym change"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeSynonymChange


@dataclass
class NewSynonym(NodeSynonymChange):
    """
    A node change where a de-novo synonym is created
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NewSynonym
    class_class_curie: ClassVar[str] = "kgcl:NewSynonym"
    class_name: ClassVar[str] = "new synonym"
    class_model_uri: ClassVar[URIRef] = KGCL.NewSynonym

    new_value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.new_value is not None and not isinstance(self.new_value, str):
            self.new_value = str(self.new_value)

        super().__post_init__(**kwargs)


@dataclass
class RemoveSynonym(NodeSynonymChange):
    """
    A node change where a synonym is deleted
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.RemoveSynonym
    class_class_curie: ClassVar[str] = "kgcl:RemoveSynonym"
    class_name: ClassVar[str] = "remove synonym"
    class_model_uri: ClassVar[URIRef] = KGCL.RemoveSynonym

    old_value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.old_value is not None and not isinstance(self.old_value, str):
            self.old_value = str(self.old_value)

        super().__post_init__(**kwargs)


@dataclass
class SynonymReplacement(NodeSynonymChange):
    """
    A node change where the text of a synonym is changed
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.SynonymReplacement
    class_class_curie: ClassVar[str] = "kgcl:SynonymReplacement"
    class_name: ClassVar[str] = "synonym replacement"
    class_model_uri: ClassVar[URIRef] = KGCL.SynonymReplacement

    old_value: Optional[str] = None
    new_value: Optional[str] = None
    has_textual_diff: Optional[Union[dict, "TextualDiff"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.old_value is not None and not isinstance(self.old_value, str):
            self.old_value = str(self.old_value)

        if self.new_value is not None and not isinstance(self.new_value, str):
            self.new_value = str(self.new_value)

        if self.has_textual_diff is not None and not isinstance(self.has_textual_diff, TextualDiff):
            self.has_textual_diff = TextualDiff()

        super().__post_init__(**kwargs)


class NodeTextDefinitionChange(NodeChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeTextDefinitionChange
    class_class_curie: ClassVar[str] = "kgcl:NodeTextDefinitionChange"
    class_name: ClassVar[str] = "node text definition change"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeTextDefinitionChange


@dataclass
class NewTextDefinition(NodeTextDefinitionChange):
    """
    A node change where a de-novo text definition is created
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NewTextDefinition
    class_class_curie: ClassVar[str] = "kgcl:NewTextDefinition"
    class_name: ClassVar[str] = "new text definition"
    class_model_uri: ClassVar[URIRef] = KGCL.NewTextDefinition

    new_value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.new_value is not None and not isinstance(self.new_value, str):
            self.new_value = str(self.new_value)

        super().__post_init__(**kwargs)


@dataclass
class RemoveTextDefinition(NodeTextDefinitionChange):
    """
    A node change where a text definition is deleted
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.RemoveTextDefinition
    class_class_curie: ClassVar[str] = "kgcl:RemoveTextDefinition"
    class_name: ClassVar[str] = "remove text definition"
    class_model_uri: ClassVar[URIRef] = KGCL.RemoveTextDefinition

    old_value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.old_value is not None and not isinstance(self.old_value, str):
            self.old_value = str(self.old_value)

        super().__post_init__(**kwargs)


@dataclass
class TextDefinitionReplacement(NodeTextDefinitionChange):
    """
    A node change where a text definition is modified
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.TextDefinitionReplacement
    class_class_curie: ClassVar[str] = "kgcl:TextDefinitionReplacement"
    class_name: ClassVar[str] = "text definition replacement"
    class_model_uri: ClassVar[URIRef] = KGCL.TextDefinitionReplacement

    old_value: Optional[str] = None
    new_value: Optional[str] = None
    has_textual_diff: Optional[Union[dict, "TextualDiff"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.old_value is not None and not isinstance(self.old_value, str):
            self.old_value = str(self.old_value)

        if self.new_value is not None and not isinstance(self.new_value, str):
            self.new_value = str(self.new_value)

        if self.has_textual_diff is not None and not isinstance(self.has_textual_diff, TextualDiff):
            self.has_textual_diff = TextualDiff()

        super().__post_init__(**kwargs)


class DatatypeChange(SimpleChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.DatatypeChange
    class_class_curie: ClassVar[str] = "kgcl:DatatypeChange"
    class_name: ClassVar[str] = "datatype change"
    class_model_uri: ClassVar[URIRef] = KGCL.DatatypeChange


@dataclass
class AddNodeToSubset(NodeChange):
    """
    Places a node inside a subset, by annotating that node
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.AddNodeToSubset
    class_class_curie: ClassVar[str] = "kgcl:AddNodeToSubset"
    class_name: ClassVar[str] = "add node to subset"
    class_model_uri: ClassVar[URIRef] = KGCL.AddNodeToSubset

    in_subset: Optional[Union[dict, Subset]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_subset is not None and not isinstance(self.in_subset, Subset):
            self.in_subset = Subset()

        super().__post_init__(**kwargs)


@dataclass
class RemovedNodeFromSubset(NodeChange):
    """
    Removes a node from a subset, by removing an annotation
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.RemovedNodeFromSubset
    class_class_curie: ClassVar[str] = "kgcl:RemovedNodeFromSubset"
    class_name: ClassVar[str] = "removed node from subset"
    class_model_uri: ClassVar[URIRef] = KGCL.RemovedNodeFromSubset

    in_subset: Optional[Union[dict, Subset]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_subset is not None and not isinstance(self.in_subset, Subset):
            self.in_subset = Subset()

        super().__post_init__(**kwargs)


@dataclass
class NodeObsoletion(NodeChange):
    """
    Obsoletion of a node deprecates usage of that node, but does not delete it.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeObsoletion
    class_class_curie: ClassVar[str] = "kgcl:NodeObsoletion"
    class_name: ClassVar[str] = "node obsoletion"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeObsoletion

    change_description: Optional[str] = None
    replaced_by: Optional[Union[str, NodeId]] = None
    consider: Optional[Union[str, NodeId]] = None
    associated_change_set: Optional[Union[Union[dict, Change], List[Union[dict, Change]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        if self.replaced_by is not None and not isinstance(self.replaced_by, NodeId):
            self.replaced_by = NodeId(self.replaced_by)

        if self.consider is not None and not isinstance(self.consider, NodeId):
            self.consider = NodeId(self.consider)

        if self.associated_change_set is None:
            self.associated_change_set = []
        if not isinstance(self.associated_change_set, list):
            self.associated_change_set = [self.associated_change_set]
        self.associated_change_set = [v if isinstance(v, Change) else Change(**v) for v in self.associated_change_set]

        super().__post_init__(**kwargs)


@dataclass
class NodeUnobsoletion(NodeChange):
    """
    unobsoletion of a node deprecates usage of that node. Rarely applied.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeUnobsoletion
    class_class_curie: ClassVar[str] = "kgcl:NodeUnobsoletion"
    class_name: ClassVar[str] = "node unobsoletion"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeUnobsoletion

    change_description: Optional[str] = None
    replaced_by: Optional[Union[str, NodeId]] = None
    consider: Optional[Union[str, NodeId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        if self.replaced_by is not None and not isinstance(self.replaced_by, NodeId):
            self.replaced_by = NodeId(self.replaced_by)

        if self.consider is not None and not isinstance(self.consider, NodeId):
            self.consider = NodeId(self.consider)

        super().__post_init__(**kwargs)


@dataclass
class NodeCreation(NodeChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeCreation
    class_class_curie: ClassVar[str] = "kgcl:NodeCreation"
    class_name: ClassVar[str] = "node creation"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeCreation

    id: Union[str, NodeCreationId] = None
    name: Optional[str] = None
    annotation_set: Optional[Union[dict, Annotation]] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is None:
            raise ValueError("id must be supplied")
        if not isinstance(self.id, NodeCreationId):
            self.id = NodeCreationId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**self.annotation_set)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class NodeDeletion(NodeChange):
    """
    Deletion of a node from the graph. Note it is recommended nodes are obsoleted and never merged, but this operation
    exists to represent deletions in ontologies, accidental or otherwise
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeDeletion
    class_class_curie: ClassVar[str] = "kgcl:NodeDeletion"
    class_name: ClassVar[str] = "node deletion"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeDeletion

    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class NodeObsoletionWithMerge(NodeObsoletion):
    """
    An obsoletion change in which information from the obsoleted node is moved to a single target.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeObsoletionWithMerge
    class_class_curie: ClassVar[str] = "kgcl:NodeObsoletionWithMerge"
    class_name: ClassVar[str] = "node obsoletion with merge"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeObsoletionWithMerge

    target: Optional[str] = None
    about: Optional[str] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.target is not None and not isinstance(self.target, str):
            self.target = str(self.target)

        if self.about is not None and not isinstance(self.about, str):
            self.about = str(self.about)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class NodeObsoletionWithSplit(NodeObsoletion):
    """
    An obsoletion change in which information from the obsoleted node is moved selectively to multiple targets
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeObsoletionWithSplit
    class_class_curie: ClassVar[str] = "kgcl:NodeObsoletionWithSplit"
    class_name: ClassVar[str] = "node obsoletion with split"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeObsoletionWithSplit

    target: Optional[Union[str, List[str]]] = empty_list()
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.target is None:
            self.target = []
        if not isinstance(self.target, list):
            self.target = [self.target]
        self.target = [v if isinstance(v, str) else str(v) for v in self.target]

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


class TextualDiff(YAMLRoot):
    """
    A summarizing of a change on a piece of text. This could be rendered in a number of different ways
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.TextualDiff
    class_class_curie: ClassVar[str] = "kgcl:TextualDiff"
    class_name: ClassVar[str] = "textual diff"
    class_model_uri: ClassVar[URIRef] = KGCL.TextualDiff


# Enumerations


# Slots
class slots:
    pass

slots.about = Slot(uri=KGCL.about, name="about", curie=KGCL.curie('about'),
                   model_uri=KGCL.about, domain=None, range=Optional[str])

slots.target = Slot(uri=KGCL.target, name="target", curie=KGCL.curie('target'),
                   model_uri=KGCL.target, domain=None, range=Optional[str])

slots.old_value = Slot(uri=KGCL.old_value, name="old value", curie=KGCL.curie('old_value'),
                   model_uri=KGCL.old_value, domain=None, range=Optional[str])

slots.new_value = Slot(uri=KGCL.new_value, name="new value", curie=KGCL.curie('new_value'),
                   model_uri=KGCL.new_value, domain=None, range=Optional[str])

slots.change_description = Slot(uri=KGCL.change_description, name="change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.change_description, domain=None, range=Optional[str])

slots.has_textual_diff = Slot(uri=KGCL.has_textual_diff, name="has textual diff", curie=KGCL.curie('has_textual_diff'),
                   model_uri=KGCL.has_textual_diff, domain=Change, range=Optional[Union[dict, "TextualDiff"]])

slots.change_set = Slot(uri=KGCL.change_set, name="change set", curie=KGCL.curie('change_set'),
                   model_uri=KGCL.change_set, domain=None, range=Optional[Union[Union[dict, Change], List[Union[dict, Change]]]])

slots.associated_change_set = Slot(uri=KGCL.associated_change_set, name="associated change set", curie=KGCL.curie('associated_change_set'),
                   model_uri=KGCL.associated_change_set, domain=None, range=Optional[Union[Union[dict, Change], List[Union[dict, Change]]]])

slots.change_type = Slot(uri=KGCL.change_type, name="change type", curie=KGCL.curie('change_type'),
                   model_uri=KGCL.change_type, domain=None, range=Optional[Union[str, ChangeClassType]])

slots.count = Slot(uri=KGCL.count, name="count", curie=KGCL.curie('count'),
                   model_uri=KGCL.count, domain=None, range=Optional[int])

slots.in_subset = Slot(uri=KGCL.in_subset, name="in subset", curie=KGCL.curie('in_subset'),
                   model_uri=KGCL.in_subset, domain=None, range=Optional[Union[dict, Subset]])

slots.replaced_by = Slot(uri=KGCL.replaced_by, name="replaced by", curie=KGCL.curie('replaced_by'),
                   model_uri=KGCL.replaced_by, domain=None, range=Optional[Union[str, NodeId]])

slots.consider = Slot(uri=KGCL.consider, name="consider", curie=KGCL.curie('consider'),
                   model_uri=KGCL.consider, domain=None, range=Optional[Union[str, NodeId]])

slots.multi_node_obsoletion_change_set = Slot(uri=KGCL.change_set, name="multi node obsoletion_change set", curie=KGCL.curie('change_set'),
                   model_uri=KGCL.multi_node_obsoletion_change_set, domain=MultiNodeObsoletion, range=Optional[Union[Union[dict, "NodeObsoletion"], List[Union[dict, "NodeObsoletion"]]]])

slots.multi_node_obsoletion_change_description = Slot(uri=KGCL.change_description, name="multi node obsoletion_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.multi_node_obsoletion_change_description, domain=MultiNodeObsoletion, range=Optional[str])

slots.multi_node_obsoletion_associated_change_set = Slot(uri=KGCL.associated_change_set, name="multi node obsoletion_associated change set", curie=KGCL.curie('associated_change_set'),
                   model_uri=KGCL.multi_node_obsoletion_associated_change_set, domain=MultiNodeObsoletion, range=Optional[Union[Union[dict, Change], List[Union[dict, Change]]]])

slots.change_set_summary_statistic_change_type = Slot(uri=KGCL.change_type, name="change set summary statistic_change type", curie=KGCL.curie('change_type'),
                   model_uri=KGCL.change_set_summary_statistic_change_type, domain=ChangeSetSummaryStatistic, range=Optional[Union[str, ChangeClassType]])

slots.change_set_summary_statistic_count = Slot(uri=KGCL.count, name="change set summary statistic_count", curie=KGCL.curie('count'),
                   model_uri=KGCL.change_set_summary_statistic_count, domain=ChangeSetSummaryStatistic, range=Optional[int])

slots.change_set_summary_statistic_property_value_set = Slot(uri=KGCL.property_value_set, name="change set summary statistic_property value set", curie=KGCL.curie('property_value_set'),
                   model_uri=KGCL.change_set_summary_statistic_property_value_set, domain=ChangeSetSummaryStatistic, range=Optional[Union[Union[dict, PropertyValue], List[Union[dict, PropertyValue]]]])

slots.add_to_subset_in_subset = Slot(uri=KGCL.in_subset, name="add to subset_in subset", curie=KGCL.curie('in_subset'),
                   model_uri=KGCL.add_to_subset_in_subset, domain=None, range=Optional[Union[dict, Subset]])

slots.remove_from_subset_in_subset = Slot(uri=KGCL.in_subset, name="remove from subset_in subset", curie=KGCL.curie('in_subset'),
                   model_uri=KGCL.remove_from_subset_in_subset, domain=None, range=Optional[Union[dict, Subset]])

slots.edge_change_about = Slot(uri=KGCL.about, name="edge change_about", curie=KGCL.curie('about'),
                   model_uri=KGCL.edge_change_about, domain=EdgeChange, range=Optional[str])

slots.edge_creation_change_description = Slot(uri=KGCL.change_description, name="edge creation_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.edge_creation_change_description, domain=EdgeCreation, range=Optional[str])

slots.edge_deletion_change_description = Slot(uri=KGCL.change_description, name="edge deletion_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.edge_deletion_change_description, domain=EdgeDeletion, range=Optional[str])

slots.edge_obsoletion_change_description = Slot(uri=KGCL.change_description, name="edge obsoletion_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.edge_obsoletion_change_description, domain=EdgeObsoletion, range=Optional[str])

slots.node_move_change_description = Slot(uri=KGCL.change_description, name="node move_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_move_change_description, domain=NodeMove, range=Optional[str])

slots.node_deepening_change_description = Slot(uri=KGCL.change_description, name="node deepening_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_deepening_change_description, domain=NodeDeepening, range=Optional[str])

slots.node_shallowing_change_description = Slot(uri=KGCL.change_description, name="node shallowing_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_shallowing_change_description, domain=NodeShallowing, range=Optional[str])

slots.edge_label_change_change_description = Slot(uri=KGCL.change_description, name="edge label change_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.edge_label_change_change_description, domain=EdgeLabelChange, range=Optional[str])

slots.node_change_about = Slot(uri=KGCL.about, name="node change_about", curie=KGCL.curie('about'),
                   model_uri=KGCL.node_change_about, domain=NodeChange, range=Optional[str])

slots.node_rename_old_value = Slot(uri=KGCL.old_value, name="node rename_old value", curie=KGCL.curie('old_value'),
                   model_uri=KGCL.node_rename_old_value, domain=NodeRename, range=Optional[str])

slots.node_rename_new_value = Slot(uri=KGCL.new_value, name="node rename_new value", curie=KGCL.curie('new_value'),
                   model_uri=KGCL.node_rename_new_value, domain=NodeRename, range=Optional[str])

slots.node_rename_change_description = Slot(uri=KGCL.change_description, name="node rename_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_rename_change_description, domain=NodeRename, range=Optional[str])

slots.node_obsoletion_change_description = Slot(uri=KGCL.change_description, name="node obsoletion_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_obsoletion_change_description, domain=NodeObsoletion, range=Optional[str])

slots.node_obsoletion_replaced_by = Slot(uri=KGCL.replaced_by, name="node obsoletion_replaced by", curie=KGCL.curie('replaced_by'),
                   model_uri=KGCL.node_obsoletion_replaced_by, domain=NodeObsoletion, range=Optional[Union[str, NodeId]])

slots.node_obsoletion_consider = Slot(uri=KGCL.consider, name="node obsoletion_consider", curie=KGCL.curie('consider'),
                   model_uri=KGCL.node_obsoletion_consider, domain=NodeObsoletion, range=Optional[Union[str, NodeId]])

slots.node_obsoletion_associated_change_set = Slot(uri=KGCL.associated_change_set, name="node obsoletion_associated change set", curie=KGCL.curie('associated_change_set'),
                   model_uri=KGCL.node_obsoletion_associated_change_set, domain=NodeObsoletion, range=Optional[Union[Union[dict, Change], List[Union[dict, Change]]]])

slots.node_unobsoletion_change_description = Slot(uri=KGCL.change_description, name="node unobsoletion_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_unobsoletion_change_description, domain=NodeUnobsoletion, range=Optional[str])

slots.node_unobsoletion_replaced_by = Slot(uri=KGCL.replaced_by, name="node unobsoletion_replaced by", curie=KGCL.curie('replaced_by'),
                   model_uri=KGCL.node_unobsoletion_replaced_by, domain=NodeUnobsoletion, range=Optional[Union[str, NodeId]])

slots.node_unobsoletion_consider = Slot(uri=KGCL.consider, name="node unobsoletion_consider", curie=KGCL.curie('consider'),
                   model_uri=KGCL.node_unobsoletion_consider, domain=NodeUnobsoletion, range=Optional[Union[str, NodeId]])

slots.node_creation_change_description = Slot(uri=KGCL.change_description, name="node creation_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_creation_change_description, domain=NodeCreation, range=Optional[str])

slots.node_deletion_change_description = Slot(uri=KGCL.change_description, name="node deletion_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_deletion_change_description, domain=NodeDeletion, range=Optional[str])

slots.node_obsoletion_with_merge_target = Slot(uri=KGCL.target, name="node obsoletion with merge_target", curie=KGCL.curie('target'),
                   model_uri=KGCL.node_obsoletion_with_merge_target, domain=NodeObsoletionWithMerge, range=Optional[str])

slots.node_obsoletion_with_merge_about = Slot(uri=KGCL.about, name="node obsoletion with merge_about", curie=KGCL.curie('about'),
                   model_uri=KGCL.node_obsoletion_with_merge_about, domain=NodeObsoletionWithMerge, range=Optional[str])

slots.node_obsoletion_with_merge_change_description = Slot(uri=KGCL.change_description, name="node obsoletion with merge_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_obsoletion_with_merge_change_description, domain=NodeObsoletionWithMerge, range=Optional[str])

slots.node_obsoletion_with_split_target = Slot(uri=KGCL.target, name="node obsoletion with split_target", curie=KGCL.curie('target'),
                   model_uri=KGCL.node_obsoletion_with_split_target, domain=NodeObsoletionWithSplit, range=Optional[Union[str, List[str]]])

slots.node_obsoletion_with_split_change_description = Slot(uri=KGCL.change_description, name="node obsoletion with split_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_obsoletion_with_split_change_description, domain=NodeObsoletionWithSplit, range=Optional[str])
