# Auto generated from kgcl.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-09-25 20:26
# Schema: kgcl
#
# id: https://w3id.org/kgcl
# description: A data model for describing change operations at a high level on an ontology or ontology-like
#              artefact, such as a Knowledge Graph. * [Browse
#              Schema](https://cmungall.github.io/knowledge-graph-change-language/) *
#              [GitHub](https://github.com/cmungall/knowledge-graph-change-language)
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
from . ontology_model import Annotation, Edge, NodeId, OntologyElement, OntologySubset, OwlTypeEnum, PropertyValue
from . prov import Activity, ActivityId
from linkml_runtime.linkml_model.types import Integer, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
IAO = CurieNamespace('IAO', 'http://purl.obolibrary.org/obo/IAO_')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
KGCL = CurieNamespace('kgcl', 'http://w3id.org/kgcl/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OIO = CurieNamespace('oio', 'http://www.geneontology.org/formats/oboInOwl#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
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
class ChangeId(extended_str):
    pass


class SimpleChangeId(ChangeId):
    pass


class ComplexChangeId(ChangeId):
    pass


class MultiNodeObsoletionId(ComplexChangeId):
    pass


class TransactionId(ChangeId):
    pass


class EdgeChangeId(SimpleChangeId):
    pass


class EdgeCreationId(EdgeChangeId):
    pass


class PlaceUnderId(EdgeCreationId):
    pass


class EdgeDeletionId(EdgeChangeId):
    pass


class RemoveUnderId(EdgeDeletionId):
    pass


class EdgeObsoletionId(EdgeChangeId):
    pass


class EdgeRewiringId(EdgeChangeId):
    pass


class MappingCreationId(EdgeCreationId):
    pass


class NodeMoveId(EdgeChangeId):
    pass


class NodeDeepeningId(NodeMoveId):
    pass


class NodeShallowingId(NodeMoveId):
    pass


class PredicateChangeId(EdgeChangeId):
    pass


class EdgeLogicalInterpretationChangeId(EdgeChangeId):
    pass


class ComplexExistentialRestrictionChangeId(ComplexChangeId):
    pass


class LogicalAxiomChangeId(SimpleChangeId):
    pass


class ExistentialRestrictionChangeId(LogicalAxiomChangeId):
    pass


class ExistentialRestrictionCreationId(ExistentialRestrictionChangeId):
    pass


class ExistentialRestrictionDeletionId(ExistentialRestrictionChangeId):
    pass


class ExistentialRestrictionSubclassChangeId(ExistentialRestrictionChangeId):
    pass


class ExistentialRestrictionPropertyChangeId(ExistentialRestrictionChangeId):
    pass


class ExistentialRestrictionFillerChangeId(ExistentialRestrictionChangeId):
    pass


class NodeChangeId(SimpleChangeId):
    pass


class NodeRenameId(NodeChangeId):
    pass


class NodeAnnotationChangeId(NodeChangeId):
    pass


class NodeAnnotationReplacementId(NodeAnnotationChangeId):
    pass


class NodeSynonymChangeId(NodeChangeId):
    pass


class NewSynonymId(NodeSynonymChangeId):
    pass


class NameBecomesSynonymId(NodeSynonymChangeId):
    pass


class RemoveSynonymId(NodeSynonymChangeId):
    pass


class SynonymReplacementId(NodeSynonymChangeId):
    pass


class SynonymPredicateChangeId(NodeSynonymChangeId):
    pass


class NodeTextDefinitionChangeId(NodeChangeId):
    pass


class NewTextDefinitionId(NodeTextDefinitionChangeId):
    pass


class RemoveTextDefinitionId(NodeTextDefinitionChangeId):
    pass


class TextDefinitionReplacementId(NodeTextDefinitionChangeId):
    pass


class DatatypeChangeId(SimpleChangeId):
    pass


class AddNodeToSubsetId(NodeChangeId):
    pass


class RemovedNodeFromSubsetId(NodeChangeId):
    pass


class NodeObsoletionId(NodeChangeId):
    pass


class NodeUnobsoletionId(NodeChangeId):
    pass


class NodeCreationId(NodeChangeId):
    pass


class ClassCreationId(NodeCreationId):
    pass


class NodeDeletionId(NodeChangeId):
    pass


class NodeDirectMergeId(NodeObsoletionId):
    pass


class NodeObsoletionWithDirectReplacementId(NodeObsoletionId):
    pass


class NodeObsoletionWithNoDirectReplacementId(NodeObsoletionId):
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

    id: Union[str, ChangeId] = None
    was_generated_by: Optional[Union[str, ActivityId]] = None
    see_also: Optional[str] = None
    pull_request: Optional[str] = None
    creator: Optional[str] = None
    change_date: Optional[str] = None
    contributor: Optional[str] = None
    has_undo: Optional[Union[str, ChangeId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ChangeId):
            self.id = ChangeId(self.id)

        if self.was_generated_by is not None and not isinstance(self.was_generated_by, ActivityId):
            self.was_generated_by = ActivityId(self.was_generated_by)

        if self.see_also is not None and not isinstance(self.see_also, str):
            self.see_also = str(self.see_also)

        if self.pull_request is not None and not isinstance(self.pull_request, str):
            self.pull_request = str(self.pull_request)

        if self.creator is not None and not isinstance(self.creator, str):
            self.creator = str(self.creator)

        if self.change_date is not None and not isinstance(self.change_date, str):
            self.change_date = str(self.change_date)

        if self.contributor is not None and not isinstance(self.contributor, str):
            self.contributor = str(self.contributor)

        if self.has_undo is not None and not isinstance(self.has_undo, ChangeId):
            self.has_undo = ChangeId(self.has_undo)

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

    id: Union[str, SimpleChangeId] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    old_value_type: Optional[str] = None
    new_value_type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.old_value is not None and not isinstance(self.old_value, str):
            self.old_value = str(self.old_value)

        if self.new_value is not None and not isinstance(self.new_value, str):
            self.new_value = str(self.new_value)

        if self.old_value_type is not None and not isinstance(self.old_value_type, str):
            self.old_value_type = str(self.old_value_type)

        if self.new_value_type is not None and not isinstance(self.new_value_type, str):
            self.new_value_type = str(self.new_value_type)

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

    id: Union[str, ComplexChangeId] = None
    change_set: Optional[Union[Dict[Union[str, ChangeId], Union[dict, Change]], List[Union[dict, Change]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="change_set", slot_type=Change, key_name="id", keyed=True)

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

    id: Union[str, MultiNodeObsoletionId] = None
    change_set: Optional[Union[Dict[Union[str, NodeObsoletionId], Union[dict, "NodeObsoletion"]], List[Union[dict, "NodeObsoletion"]]]] = empty_dict()
    change_description: Optional[str] = None
    associated_change_set: Optional[Union[Dict[Union[str, ChangeId], Union[dict, Change]], List[Union[dict, Change]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MultiNodeObsoletionId):
            self.id = MultiNodeObsoletionId(self.id)

        self._normalize_inlined_as_list(slot_name="change_set", slot_type=NodeObsoletion, key_name="id", keyed=True)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        self._normalize_inlined_as_list(slot_name="associated_change_set", slot_type=Change, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class Transaction(Change):
    """
    A change that is a composition of a set of changes, where those changes are treated as a single unit. Could be a
    single change, or the results of an ontology diff
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.Transaction
    class_class_curie: ClassVar[str] = "kgcl:Transaction"
    class_name: ClassVar[str] = "transaction"
    class_model_uri: ClassVar[URIRef] = KGCL.Transaction

    id: Union[str, TransactionId] = None
    change_set: Optional[Union[Dict[Union[str, ChangeId], Union[dict, Change]], List[Union[dict, Change]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TransactionId):
            self.id = TransactionId(self.id)

        self._normalize_inlined_as_list(slot_name="change_set", slot_type=Change, key_name="id", keyed=True)

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

        if not isinstance(self.property_value_set, list):
            self.property_value_set = [self.property_value_set] if self.property_value_set is not None else []
        self.property_value_set = [v if isinstance(v, PropertyValue) else PropertyValue(**as_dict(v)) for v in self.property_value_set]

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


@dataclass
class Obsoletion(ChangeMixin):
    """
    Obsoletion of an element deprecates usage of that element, but does not delete that element.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.Obsoletion
    class_class_curie: ClassVar[str] = "kgcl:Obsoletion"
    class_name: ClassVar[str] = "obsoletion"
    class_model_uri: ClassVar[URIRef] = KGCL.Obsoletion

    about: Optional[Union[dict, OntologyElement]] = None
    has_undo: Optional[Union[dict, "Obsoletion"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.about is not None and not isinstance(self.about, OntologyElement):
            self.about = OntologyElement()

        if self.has_undo is not None and not isinstance(self.has_undo, Obsoletion):
            self.has_undo = Obsoletion(**as_dict(self.has_undo))

        super().__post_init__(**kwargs)


class AllowsAutomaticReplacementOfEdges(Obsoletion):
    """
    Applies to an obsoletion in which annotations or edges pointing at the obsoleted node can be automatically rewired
    to point to a target
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.AllowsAutomaticReplacementOfEdges
    class_class_curie: ClassVar[str] = "kgcl:AllowsAutomaticReplacementOfEdges"
    class_name: ClassVar[str] = "allows automatic replacement of edges"
    class_model_uri: ClassVar[URIRef] = KGCL.AllowsAutomaticReplacementOfEdges


@dataclass
class Unobsoletion(ChangeMixin):
    """
    Opposite operation of obsoletion. Rarely performed.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.Unobsoletion
    class_class_curie: ClassVar[str] = "kgcl:Unobsoletion"
    class_name: ClassVar[str] = "unobsoletion"
    class_model_uri: ClassVar[URIRef] = KGCL.Unobsoletion

    has_undo: Optional[Union[dict, Obsoletion]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.has_undo is not None and not isinstance(self.has_undo, Obsoletion):
            self.has_undo = Obsoletion(**as_dict(self.has_undo))

        super().__post_init__(**kwargs)


class Deletion(ChangeMixin):
    """
    Removal of an element.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.Deletion
    class_class_curie: ClassVar[str] = "kgcl:Deletion"
    class_name: ClassVar[str] = "deletion"
    class_model_uri: ClassVar[URIRef] = KGCL.Deletion


@dataclass
class Creation(ChangeMixin):
    """
    Creation of an element.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.Creation
    class_class_curie: ClassVar[str] = "kgcl:Creation"
    class_name: ClassVar[str] = "creation"
    class_model_uri: ClassVar[URIRef] = KGCL.Creation

    has_undo: Optional[Union[dict, Deletion]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.has_undo is not None and not isinstance(self.has_undo, Deletion):
            self.has_undo = Deletion()

        super().__post_init__(**kwargs)


@dataclass
class SubsetMembershipChange(ChangeMixin):
    """
    A change in the membership status of a node with respect to a subset (view)
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.SubsetMembershipChange
    class_class_curie: ClassVar[str] = "kgcl:SubsetMembershipChange"
    class_name: ClassVar[str] = "subset membership change"
    class_model_uri: ClassVar[URIRef] = KGCL.SubsetMembershipChange

    in_subset: Optional[Union[dict, OntologySubset]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_subset is not None and not isinstance(self.in_subset, OntologySubset):
            self.in_subset = OntologySubset()

        super().__post_init__(**kwargs)


@dataclass
class AddToSubset(SubsetMembershipChange):
    """
    placing an element inside a subset
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.AddToSubset
    class_class_curie: ClassVar[str] = "kgcl:AddToSubset"
    class_name: ClassVar[str] = "add to subset"
    class_model_uri: ClassVar[URIRef] = KGCL.AddToSubset

    in_subset: Optional[Union[dict, OntologySubset]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_subset is not None and not isinstance(self.in_subset, OntologySubset):
            self.in_subset = OntologySubset()

        super().__post_init__(**kwargs)


@dataclass
class RemoveFromSubset(SubsetMembershipChange):
    """
    removing an element from a subset
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.RemoveFromSubset
    class_class_curie: ClassVar[str] = "kgcl:RemoveFromSubset"
    class_name: ClassVar[str] = "remove from subset"
    class_model_uri: ClassVar[URIRef] = KGCL.RemoveFromSubset

    in_subset: Optional[Union[dict, OntologySubset]] = None
    has_undo: Optional[Union[dict, AddToSubset]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_subset is not None and not isinstance(self.in_subset, OntologySubset):
            self.in_subset = OntologySubset()

        if self.has_undo is not None and not isinstance(self.has_undo, AddToSubset):
            self.has_undo = AddToSubset(**as_dict(self.has_undo))

        super().__post_init__(**kwargs)


@dataclass
class EdgeChange(SimpleChange):
    """
    A change in which the element that is the focus of the change is an edge.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.EdgeChange
    class_class_curie: ClassVar[str] = "kgcl:EdgeChange"
    class_name: ClassVar[str] = "edge change"
    class_model_uri: ClassVar[URIRef] = KGCL.EdgeChange

    id: Union[str, EdgeChangeId] = None
    about_edge: Optional[Union[dict, Edge]] = None
    object_type: Optional[str] = None
    language: Optional[str] = None
    datatype: Optional[str] = None
    subject: Optional[Union[str, NodeId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.about_edge is not None and not isinstance(self.about_edge, Edge):
            self.about_edge = Edge(**as_dict(self.about_edge))

        if self.object_type is not None and not isinstance(self.object_type, str):
            self.object_type = str(self.object_type)

        if self.language is not None and not isinstance(self.language, str):
            self.language = str(self.language)

        if self.datatype is not None and not isinstance(self.datatype, str):
            self.datatype = str(self.datatype)

        if self.subject is not None and not isinstance(self.subject, NodeId):
            self.subject = NodeId(self.subject)

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

    id: Union[str, EdgeCreationId] = None
    subject: Optional[Union[str, NodeId]] = None
    predicate: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    subject_type: Optional[str] = None
    predicate_type: Optional[str] = None
    object_type: Optional[str] = None
    annotation_set: Optional[Union[dict, Annotation]] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EdgeCreationId):
            self.id = EdgeCreationId(self.id)

        if self.subject is not None and not isinstance(self.subject, NodeId):
            self.subject = NodeId(self.subject)

        if self.predicate is not None and not isinstance(self.predicate, NodeId):
            self.predicate = NodeId(self.predicate)

        if self.object is not None and not isinstance(self.object, NodeId):
            self.object = NodeId(self.object)

        if self.subject_type is not None and not isinstance(self.subject_type, str):
            self.subject_type = str(self.subject_type)

        if self.predicate_type is not None and not isinstance(self.predicate_type, str):
            self.predicate_type = str(self.predicate_type)

        if self.object_type is not None and not isinstance(self.object_type, str):
            self.object_type = str(self.object_type)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**as_dict(self.annotation_set))

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class PlaceUnder(EdgeCreation):
    """
    An edge creation where the predicate is owl:subClassOf
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.PlaceUnder
    class_class_curie: ClassVar[str] = "kgcl:PlaceUnder"
    class_name: ClassVar[str] = "place under"
    class_model_uri: ClassVar[URIRef] = KGCL.PlaceUnder

    id: Union[str, PlaceUnderId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PlaceUnderId):
            self.id = PlaceUnderId(self.id)

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

    id: Union[str, EdgeDeletionId] = None
    subject: Optional[Union[str, NodeId]] = None
    predicate: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    subject_type: Optional[str] = None
    predicate_type: Optional[str] = None
    object_type: Optional[str] = None
    annotation_set: Optional[Union[dict, Annotation]] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EdgeDeletionId):
            self.id = EdgeDeletionId(self.id)

        if self.subject is not None and not isinstance(self.subject, NodeId):
            self.subject = NodeId(self.subject)

        if self.predicate is not None and not isinstance(self.predicate, NodeId):
            self.predicate = NodeId(self.predicate)

        if self.object is not None and not isinstance(self.object, NodeId):
            self.object = NodeId(self.object)

        if self.subject_type is not None and not isinstance(self.subject_type, str):
            self.subject_type = str(self.subject_type)

        if self.predicate_type is not None and not isinstance(self.predicate_type, str):
            self.predicate_type = str(self.predicate_type)

        if self.object_type is not None and not isinstance(self.object_type, str):
            self.object_type = str(self.object_type)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**as_dict(self.annotation_set))

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class RemoveUnder(EdgeDeletion):
    """
    An edge deletion where the predicate is owl:subClassOf
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.RemoveUnder
    class_class_curie: ClassVar[str] = "kgcl:RemoveUnder"
    class_name: ClassVar[str] = "remove under"
    class_model_uri: ClassVar[URIRef] = KGCL.RemoveUnder

    id: Union[str, RemoveUnderId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RemoveUnderId):
            self.id = RemoveUnderId(self.id)

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

    id: Union[str, EdgeObsoletionId] = None
    subject: Optional[Union[str, NodeId]] = None
    predicate: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    annotation_set: Optional[Union[dict, Annotation]] = None
    change_description: Optional[str] = None
    about: Optional[Union[dict, OntologyElement]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EdgeObsoletionId):
            self.id = EdgeObsoletionId(self.id)

        if self.subject is not None and not isinstance(self.subject, NodeId):
            self.subject = NodeId(self.subject)

        if self.predicate is not None and not isinstance(self.predicate, NodeId):
            self.predicate = NodeId(self.predicate)

        if self.object is not None and not isinstance(self.object, NodeId):
            self.object = NodeId(self.object)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**as_dict(self.annotation_set))

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        if self.about is not None and not isinstance(self.about, OntologyElement):
            self.about = OntologyElement()

        super().__post_init__(**kwargs)


@dataclass
class EdgeRewiring(EdgeChange):
    """
    An edge change where one node is replaced with another, as in the case of obsoletion with replacement
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.EdgeRewiring
    class_class_curie: ClassVar[str] = "kgcl:EdgeRewiring"
    class_name: ClassVar[str] = "edge rewiring"
    class_model_uri: ClassVar[URIRef] = KGCL.EdgeRewiring

    id: Union[str, EdgeRewiringId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EdgeRewiringId):
            self.id = EdgeRewiringId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class MappingCreation(EdgeCreation):
    """
    A specific kind of edge creation in which the created edge is a mapping.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.MappingCreation
    class_class_curie: ClassVar[str] = "kgcl:MappingCreation"
    class_name: ClassVar[str] = "mapping creation"
    class_model_uri: ClassVar[URIRef] = KGCL.MappingCreation

    id: Union[str, MappingCreationId] = None
    subject: Optional[Union[str, NodeId]] = None
    predicate: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    annotation_set: Optional[Union[dict, Annotation]] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MappingCreationId):
            self.id = MappingCreationId(self.id)

        if self.subject is not None and not isinstance(self.subject, NodeId):
            self.subject = NodeId(self.subject)

        if self.predicate is not None and not isinstance(self.predicate, NodeId):
            self.predicate = NodeId(self.predicate)

        if self.object is not None and not isinstance(self.object, NodeId):
            self.object = NodeId(self.object)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**as_dict(self.annotation_set))

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class NodeMove(EdgeChange):
    """
    A node move is a combination of deleting a parent edge and adding a parent edge, where the predicate is preserved
    and the object/parent node changes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeMove
    class_class_curie: ClassVar[str] = "kgcl:NodeMove"
    class_name: ClassVar[str] = "node move"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeMove

    id: Union[str, NodeMoveId] = None
    old_object_type: Optional[str] = None
    new_object_type: Optional[str] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeMoveId):
            self.id = NodeMoveId(self.id)

        if self.old_object_type is not None and not isinstance(self.old_object_type, str):
            self.old_object_type = str(self.old_object_type)

        if self.new_object_type is not None and not isinstance(self.new_object_type, str):
            self.new_object_type = str(self.new_object_type)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class NodeDeepening(NodeMove):
    """
    A node move in which a node where the destination is a proper descendant of the original location. Note that here
    descendant applied not just to subclass, but edges of any predicate in the relational graph
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeDeepening
    class_class_curie: ClassVar[str] = "kgcl:NodeDeepening"
    class_name: ClassVar[str] = "node deepening"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeDeepening

    id: Union[str, NodeDeepeningId] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeDeepeningId):
            self.id = NodeDeepeningId(self.id)

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

    id: Union[str, NodeShallowingId] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeShallowingId):
            self.id = NodeShallowingId(self.id)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class PredicateChange(EdgeChange):
    """
    An edge change where the predicate (relationship type) is modified.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.PredicateChange
    class_class_curie: ClassVar[str] = "kgcl:PredicateChange"
    class_name: ClassVar[str] = "predicate change"
    class_model_uri: ClassVar[URIRef] = KGCL.PredicateChange

    id: Union[str, PredicateChangeId] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PredicateChangeId):
            self.id = PredicateChangeId(self.id)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class EdgeLogicalInterpretationChange(EdgeChange):
    """
    An edge change where the subjet, object, and predicate are unchanged, but the logical interpretation changes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.EdgeLogicalInterpretationChange
    class_class_curie: ClassVar[str] = "kgcl:EdgeLogicalInterpretationChange"
    class_name: ClassVar[str] = "edge logical interpretation change"
    class_model_uri: ClassVar[URIRef] = KGCL.EdgeLogicalInterpretationChange

    id: Union[str, EdgeLogicalInterpretationChangeId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EdgeLogicalInterpretationChangeId):
            self.id = EdgeLogicalInterpretationChangeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ComplexExistentialRestrictionChange(ComplexChange):
    """
    A complex change where an existential restriction axiom is changed
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.ComplexExistentialRestrictionChange
    class_class_curie: ClassVar[str] = "kgcl:ComplexExistentialRestrictionChange"
    class_name: ClassVar[str] = "complex existential restriction change"
    class_model_uri: ClassVar[URIRef] = KGCL.ComplexExistentialRestrictionChange

    id: Union[str, ComplexExistentialRestrictionChangeId] = None
    subclass: Optional[str] = None
    property: Optional[Union[str, NodeId]] = None
    filler: Optional[str] = None
    new_subclass: Optional[str] = None
    new_property: Optional[str] = None
    new_filler: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ComplexExistentialRestrictionChangeId):
            self.id = ComplexExistentialRestrictionChangeId(self.id)

        if self.subclass is not None and not isinstance(self.subclass, str):
            self.subclass = str(self.subclass)

        if self.property is not None and not isinstance(self.property, NodeId):
            self.property = NodeId(self.property)

        if self.filler is not None and not isinstance(self.filler, str):
            self.filler = str(self.filler)

        if self.new_subclass is not None and not isinstance(self.new_subclass, str):
            self.new_subclass = str(self.new_subclass)

        if self.new_property is not None and not isinstance(self.new_property, str):
            self.new_property = str(self.new_property)

        if self.new_filler is not None and not isinstance(self.new_filler, str):
            self.new_filler = str(self.new_filler)

        super().__post_init__(**kwargs)


@dataclass
class LogicalAxiomChange(SimpleChange):
    """
    A simple change where a logical axiom is changed, where the logical axiom cannot be represented as an edge
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.LogicalAxiomChange
    class_class_curie: ClassVar[str] = "kgcl:LogicalAxiomChange"
    class_name: ClassVar[str] = "logical axiom change"
    class_model_uri: ClassVar[URIRef] = KGCL.LogicalAxiomChange

    id: Union[str, LogicalAxiomChangeId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LogicalAxiomChangeId):
            self.id = LogicalAxiomChangeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ExistentialRestrictionChange(LogicalAxiomChange):
    """
    A simple change where an existential restriction axiom is changed
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.ExistentialRestrictionChange
    class_class_curie: ClassVar[str] = "kgcl:ExistentialRestrictionChange"
    class_name: ClassVar[str] = "existential restriction change"
    class_model_uri: ClassVar[URIRef] = KGCL.ExistentialRestrictionChange

    id: Union[str, ExistentialRestrictionChangeId] = None
    subclass: Optional[str] = None
    property: Optional[Union[str, NodeId]] = None
    filler: Optional[str] = None
    subclass_type: Optional[str] = None
    property_type: Optional[str] = None
    filler_type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExistentialRestrictionChangeId):
            self.id = ExistentialRestrictionChangeId(self.id)

        if self.subclass is not None and not isinstance(self.subclass, str):
            self.subclass = str(self.subclass)

        if self.property is not None and not isinstance(self.property, NodeId):
            self.property = NodeId(self.property)

        if self.filler is not None and not isinstance(self.filler, str):
            self.filler = str(self.filler)

        if self.subclass_type is not None and not isinstance(self.subclass_type, str):
            self.subclass_type = str(self.subclass_type)

        if self.property_type is not None and not isinstance(self.property_type, str):
            self.property_type = str(self.property_type)

        if self.filler_type is not None and not isinstance(self.filler_type, str):
            self.filler_type = str(self.filler_type)

        super().__post_init__(**kwargs)


@dataclass
class ExistentialRestrictionCreation(ExistentialRestrictionChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.ExistentialRestrictionCreation
    class_class_curie: ClassVar[str] = "kgcl:ExistentialRestrictionCreation"
    class_name: ClassVar[str] = "existential restriction creation"
    class_model_uri: ClassVar[URIRef] = KGCL.ExistentialRestrictionCreation

    id: Union[str, ExistentialRestrictionCreationId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExistentialRestrictionCreationId):
            self.id = ExistentialRestrictionCreationId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ExistentialRestrictionDeletion(ExistentialRestrictionChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.ExistentialRestrictionDeletion
    class_class_curie: ClassVar[str] = "kgcl:ExistentialRestrictionDeletion"
    class_name: ClassVar[str] = "existential restriction deletion"
    class_model_uri: ClassVar[URIRef] = KGCL.ExistentialRestrictionDeletion

    id: Union[str, ExistentialRestrictionDeletionId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExistentialRestrictionDeletionId):
            self.id = ExistentialRestrictionDeletionId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ExistentialRestrictionSubclassChange(ExistentialRestrictionChange):
    """
    A simple change where an existential restriction axiom is changed
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.ExistentialRestrictionSubclassChange
    class_class_curie: ClassVar[str] = "kgcl:ExistentialRestrictionSubclassChange"
    class_name: ClassVar[str] = "existential restriction subclass change"
    class_model_uri: ClassVar[URIRef] = KGCL.ExistentialRestrictionSubclassChange

    id: Union[str, ExistentialRestrictionSubclassChangeId] = None
    new_subclass: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExistentialRestrictionSubclassChangeId):
            self.id = ExistentialRestrictionSubclassChangeId(self.id)

        if self.new_subclass is not None and not isinstance(self.new_subclass, str):
            self.new_subclass = str(self.new_subclass)

        super().__post_init__(**kwargs)


@dataclass
class ExistentialRestrictionPropertyChange(ExistentialRestrictionChange):
    """
    A simple change where an existential restriction axiom is changed
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.ExistentialRestrictionPropertyChange
    class_class_curie: ClassVar[str] = "kgcl:ExistentialRestrictionPropertyChange"
    class_name: ClassVar[str] = "existential restriction property change"
    class_model_uri: ClassVar[URIRef] = KGCL.ExistentialRestrictionPropertyChange

    id: Union[str, ExistentialRestrictionPropertyChangeId] = None
    new_property: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExistentialRestrictionPropertyChangeId):
            self.id = ExistentialRestrictionPropertyChangeId(self.id)

        if self.new_property is not None and not isinstance(self.new_property, str):
            self.new_property = str(self.new_property)

        super().__post_init__(**kwargs)


@dataclass
class ExistentialRestrictionFillerChange(ExistentialRestrictionChange):
    """
    A simple change where an existential restriction axiom is changed
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.ExistentialRestrictionFillerChange
    class_class_curie: ClassVar[str] = "kgcl:ExistentialRestrictionFillerChange"
    class_name: ClassVar[str] = "existential restriction filler change"
    class_model_uri: ClassVar[URIRef] = KGCL.ExistentialRestrictionFillerChange

    id: Union[str, ExistentialRestrictionFillerChangeId] = None
    new_filler: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExistentialRestrictionFillerChangeId):
            self.id = ExistentialRestrictionFillerChangeId(self.id)

        if self.new_filler is not None and not isinstance(self.new_filler, str):
            self.new_filler = str(self.new_filler)

        super().__post_init__(**kwargs)


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

    id: Union[str, NodeChangeId] = None
    about_node: Optional[Union[str, NodeId]] = None
    about_node_representation: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.about_node is not None and not isinstance(self.about_node, NodeId):
            self.about_node = NodeId(self.about_node)

        if self.about_node_representation is not None and not isinstance(self.about_node_representation, str):
            self.about_node_representation = str(self.about_node_representation)

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

    id: Union[str, NodeRenameId] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    has_textual_diff: Optional[Union[dict, "TextualDiff"]] = None
    new_language: Optional[str] = None
    old_language: Optional[str] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeRenameId):
            self.id = NodeRenameId(self.id)

        if self.old_value is not None and not isinstance(self.old_value, str):
            self.old_value = str(self.old_value)

        if self.new_value is not None and not isinstance(self.new_value, str):
            self.new_value = str(self.new_value)

        if self.has_textual_diff is not None and not isinstance(self.has_textual_diff, TextualDiff):
            self.has_textual_diff = TextualDiff()

        if self.new_language is not None and not isinstance(self.new_language, str):
            self.new_language = str(self.new_language)

        if self.old_language is not None and not isinstance(self.old_language, str):
            self.old_language = str(self.old_language)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class NodeAnnotationChange(NodeChange):
    """
    A node change where the change alters node properties/annotations. TODO
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeAnnotationChange
    class_class_curie: ClassVar[str] = "kgcl:NodeAnnotationChange"
    class_name: ClassVar[str] = "node annotation change"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeAnnotationChange

    id: Union[str, NodeAnnotationChangeId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeAnnotationChangeId):
            self.id = NodeAnnotationChangeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class NodeAnnotationReplacement(NodeAnnotationChange):
    """
    A node annotation change where the change replaces a particular property value. TODO
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeAnnotationReplacement
    class_class_curie: ClassVar[str] = "kgcl:NodeAnnotationReplacement"
    class_name: ClassVar[str] = "node annotation replacement"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeAnnotationReplacement

    id: Union[str, NodeAnnotationReplacementId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeAnnotationReplacementId):
            self.id = NodeAnnotationReplacementId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class NodeSynonymChange(NodeChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeSynonymChange
    class_class_curie: ClassVar[str] = "kgcl:NodeSynonymChange"
    class_name: ClassVar[str] = "node synonym change"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeSynonymChange

    id: Union[str, NodeSynonymChangeId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeSynonymChangeId):
            self.id = NodeSynonymChangeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class NewSynonym(NodeSynonymChange):
    """
    A node synonym change where a de-novo synonym is created
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NewSynonym
    class_class_curie: ClassVar[str] = "kgcl:NewSynonym"
    class_name: ClassVar[str] = "new synonym"
    class_model_uri: ClassVar[URIRef] = KGCL.NewSynonym

    id: Union[str, NewSynonymId] = None
    new_value: Optional[str] = None
    language: Optional[str] = None
    qualifier: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NewSynonymId):
            self.id = NewSynonymId(self.id)

        if self.new_value is not None and not isinstance(self.new_value, str):
            self.new_value = str(self.new_value)

        if self.language is not None and not isinstance(self.language, str):
            self.language = str(self.language)

        if self.qualifier is not None and not isinstance(self.qualifier, str):
            self.qualifier = str(self.qualifier)

        super().__post_init__(**kwargs)


@dataclass
class NameBecomesSynonym(NodeSynonymChange):
    """
    A node synonym where the name NAME of an node NODE moves to a synonym, and NODE receives a new name. This change
    consists of compose of (1) a node rename where NAME is replaced by a different name (2) a new synonym
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NameBecomesSynonym
    class_class_curie: ClassVar[str] = "kgcl:NameBecomesSynonym"
    class_name: ClassVar[str] = "name becomes synonym"
    class_model_uri: ClassVar[URIRef] = KGCL.NameBecomesSynonym

    id: Union[str, NameBecomesSynonymId] = None
    change_1: Optional[Union[str, NodeRenameId]] = None
    change_2: Optional[Union[str, NewSynonymId]] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NameBecomesSynonymId):
            self.id = NameBecomesSynonymId(self.id)

        if self.change_1 is not None and not isinstance(self.change_1, NodeRenameId):
            self.change_1 = NodeRenameId(self.change_1)

        if self.change_2 is not None and not isinstance(self.change_2, NewSynonymId):
            self.change_2 = NewSynonymId(self.change_2)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class RemoveSynonym(NodeSynonymChange):
    """
    A node synonym change where a synonym is deleted
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.RemoveSynonym
    class_class_curie: ClassVar[str] = "kgcl:RemoveSynonym"
    class_name: ClassVar[str] = "remove synonym"
    class_model_uri: ClassVar[URIRef] = KGCL.RemoveSynonym

    id: Union[str, RemoveSynonymId] = None
    old_value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RemoveSynonymId):
            self.id = RemoveSynonymId(self.id)

        if self.old_value is not None and not isinstance(self.old_value, str):
            self.old_value = str(self.old_value)

        super().__post_init__(**kwargs)


@dataclass
class SynonymReplacement(NodeSynonymChange):
    """
    A node synonym change where the text of a synonym is changed
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.SynonymReplacement
    class_class_curie: ClassVar[str] = "kgcl:SynonymReplacement"
    class_name: ClassVar[str] = "synonym replacement"
    class_model_uri: ClassVar[URIRef] = KGCL.SynonymReplacement

    id: Union[str, SynonymReplacementId] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    has_textual_diff: Optional[Union[dict, "TextualDiff"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SynonymReplacementId):
            self.id = SynonymReplacementId(self.id)

        if self.old_value is not None and not isinstance(self.old_value, str):
            self.old_value = str(self.old_value)

        if self.new_value is not None and not isinstance(self.new_value, str):
            self.new_value = str(self.new_value)

        if self.has_textual_diff is not None and not isinstance(self.has_textual_diff, TextualDiff):
            self.has_textual_diff = TextualDiff()

        super().__post_init__(**kwargs)


@dataclass
class SynonymPredicateChange(NodeSynonymChange):
    """
    A node synonym change where the predicate of a synonym is changed. Background: synonyms can be represented by a
    variety of predicates. For example, many OBO ontologies make use of predicates such as oio:hasExactSynonym,
    oio:hasRelatedSynonym, etc
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.SynonymPredicateChange
    class_class_curie: ClassVar[str] = "kgcl:SynonymPredicateChange"
    class_name: ClassVar[str] = "synonym predicate change"
    class_model_uri: ClassVar[URIRef] = KGCL.SynonymPredicateChange

    id: Union[str, SynonymPredicateChangeId] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    has_textual_diff: Optional[Union[dict, "TextualDiff"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SynonymPredicateChangeId):
            self.id = SynonymPredicateChangeId(self.id)

        if self.old_value is not None and not isinstance(self.old_value, str):
            self.old_value = str(self.old_value)

        if self.new_value is not None and not isinstance(self.new_value, str):
            self.new_value = str(self.new_value)

        if self.has_textual_diff is not None and not isinstance(self.has_textual_diff, TextualDiff):
            self.has_textual_diff = TextualDiff()

        super().__post_init__(**kwargs)


@dataclass
class NodeTextDefinitionChange(NodeChange):
    """
    A node change where the text definition is changed
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeTextDefinitionChange
    class_class_curie: ClassVar[str] = "kgcl:NodeTextDefinitionChange"
    class_name: ClassVar[str] = "node text definition change"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeTextDefinitionChange

    id: Union[str, NodeTextDefinitionChangeId] = None

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

    id: Union[str, NewTextDefinitionId] = None
    new_value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NewTextDefinitionId):
            self.id = NewTextDefinitionId(self.id)

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

    id: Union[str, RemoveTextDefinitionId] = None
    old_value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RemoveTextDefinitionId):
            self.id = RemoveTextDefinitionId(self.id)

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

    id: Union[str, TextDefinitionReplacementId] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    has_textual_diff: Optional[Union[dict, "TextualDiff"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TextDefinitionReplacementId):
            self.id = TextDefinitionReplacementId(self.id)

        if self.old_value is not None and not isinstance(self.old_value, str):
            self.old_value = str(self.old_value)

        if self.new_value is not None and not isinstance(self.new_value, str):
            self.new_value = str(self.new_value)

        if self.has_textual_diff is not None and not isinstance(self.has_textual_diff, TextualDiff):
            self.has_textual_diff = TextualDiff()

        super().__post_init__(**kwargs)


@dataclass
class DatatypeChange(SimpleChange):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.DatatypeChange
    class_class_curie: ClassVar[str] = "kgcl:DatatypeChange"
    class_name: ClassVar[str] = "datatype change"
    class_model_uri: ClassVar[URIRef] = KGCL.DatatypeChange

    id: Union[str, DatatypeChangeId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DatatypeChangeId):
            self.id = DatatypeChangeId(self.id)

        super().__post_init__(**kwargs)


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

    id: Union[str, AddNodeToSubsetId] = None
    in_subset: Optional[Union[dict, OntologySubset]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AddNodeToSubsetId):
            self.id = AddNodeToSubsetId(self.id)

        if self.in_subset is not None and not isinstance(self.in_subset, OntologySubset):
            self.in_subset = OntologySubset()

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

    id: Union[str, RemovedNodeFromSubsetId] = None
    change_description: Optional[str] = None
    about_node: Optional[Union[str, NodeId]] = None
    subset: Optional[str] = None
    in_subset: Optional[Union[dict, OntologySubset]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RemovedNodeFromSubsetId):
            self.id = RemovedNodeFromSubsetId(self.id)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        if self.about_node is not None and not isinstance(self.about_node, NodeId):
            self.about_node = NodeId(self.about_node)

        if self.subset is not None and not isinstance(self.subset, str):
            self.subset = str(self.subset)

        if self.in_subset is not None and not isinstance(self.in_subset, OntologySubset):
            self.in_subset = OntologySubset()

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

    id: Union[str, NodeObsoletionId] = None
    has_direct_replacement: Optional[Union[str, NodeId]] = None
    has_nondirect_replacement: Optional[Union[Union[str, NodeId], List[Union[str, NodeId]]]] = empty_list()
    change_description: Optional[str] = None
    associated_change_set: Optional[Union[Dict[Union[str, ChangeId], Union[dict, Change]], List[Union[dict, Change]]]] = empty_dict()
    about: Optional[Union[dict, OntologyElement]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeObsoletionId):
            self.id = NodeObsoletionId(self.id)

        if self.has_direct_replacement is not None and not isinstance(self.has_direct_replacement, NodeId):
            self.has_direct_replacement = NodeId(self.has_direct_replacement)

        if not isinstance(self.has_nondirect_replacement, list):
            self.has_nondirect_replacement = [self.has_nondirect_replacement] if self.has_nondirect_replacement is not None else []
        self.has_nondirect_replacement = [v if isinstance(v, NodeId) else NodeId(v) for v in self.has_nondirect_replacement]

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        self._normalize_inlined_as_list(slot_name="associated_change_set", slot_type=Change, key_name="id", keyed=True)

        if self.about is not None and not isinstance(self.about, OntologyElement):
            self.about = OntologyElement()

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

    id: Union[str, NodeUnobsoletionId] = None
    change_description: Optional[str] = None
    replaced_by: Optional[Union[str, NodeId]] = None
    consider: Optional[Union[str, NodeId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeUnobsoletionId):
            self.id = NodeUnobsoletionId(self.id)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        if self.replaced_by is not None and not isinstance(self.replaced_by, NodeId):
            self.replaced_by = NodeId(self.replaced_by)

        if self.consider is not None and not isinstance(self.consider, NodeId):
            self.consider = NodeId(self.consider)

        super().__post_init__(**kwargs)


@dataclass
class NodeCreation(NodeChange):
    """
    a node change in which a new node is created
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeCreation
    class_class_curie: ClassVar[str] = "kgcl:NodeCreation"
    class_name: ClassVar[str] = "node creation"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeCreation

    id: Union[str, NodeCreationId] = None
    node_id: Optional[Union[str, NodeId]] = None
    name: Optional[str] = None
    owl_type: Optional[Union[str, "OwlTypeEnum"]] = None
    annotation_set: Optional[Union[dict, Annotation]] = None
    language: Optional[str] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeCreationId):
            self.id = NodeCreationId(self.id)

        if self.node_id is not None and not isinstance(self.node_id, NodeId):
            self.node_id = NodeId(self.node_id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.owl_type is not None and not isinstance(self.owl_type, OwlTypeEnum):
            self.owl_type = OwlTypeEnum(self.owl_type)

        if self.annotation_set is not None and not isinstance(self.annotation_set, Annotation):
            self.annotation_set = Annotation(**as_dict(self.annotation_set))

        if self.language is not None and not isinstance(self.language, str):
            self.language = str(self.language)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class ClassCreation(NodeCreation):
    """
    A node creation where the owl type is 'class'
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.ClassCreation
    class_class_curie: ClassVar[str] = "kgcl:ClassCreation"
    class_name: ClassVar[str] = "class creation"
    class_model_uri: ClassVar[URIRef] = KGCL.ClassCreation

    id: Union[str, ClassCreationId] = None
    superclass: Optional[Union[str, NodeId]] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ClassCreationId):
            self.id = ClassCreationId(self.id)

        if self.superclass is not None and not isinstance(self.superclass, NodeId):
            self.superclass = NodeId(self.superclass)

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

    id: Union[str, NodeDeletionId] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeDeletionId):
            self.id = NodeDeletionId(self.id)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class NodeDirectMerge(NodeObsoletion):
    """
    An obsoletion change in which all metadata (including name/label) from the source node is deleted and added to the
    target node, and edges can automatically be rewired to point to the target node
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeDirectMerge
    class_class_curie: ClassVar[str] = "kgcl:NodeDirectMerge"
    class_name: ClassVar[str] = "node direct merge"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeDirectMerge

    id: Union[str, NodeDirectMergeId] = None
    has_direct_replacement: Union[str, NodeId] = None
    about_node: Optional[Union[str, NodeId]] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeDirectMergeId):
            self.id = NodeDirectMergeId(self.id)

        if self._is_empty(self.has_direct_replacement):
            self.MissingRequiredField("has_direct_replacement")
        if not isinstance(self.has_direct_replacement, NodeId):
            self.has_direct_replacement = NodeId(self.has_direct_replacement)

        if self.about_node is not None and not isinstance(self.about_node, NodeId):
            self.about_node = NodeId(self.about_node)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class NodeObsoletionWithDirectReplacement(NodeObsoletion):
    """
    An obsoletion change in which information from the obsoleted node is selectively copied to a single target, and
    edges can automatically be rewired to point to the target node
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeObsoletionWithDirectReplacement
    class_class_curie: ClassVar[str] = "kgcl:NodeObsoletionWithDirectReplacement"
    class_name: ClassVar[str] = "node obsoletion with direct replacement"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeObsoletionWithDirectReplacement

    id: Union[str, NodeObsoletionWithDirectReplacementId] = None
    has_direct_replacement: Union[str, NodeId] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeObsoletionWithDirectReplacementId):
            self.id = NodeObsoletionWithDirectReplacementId(self.id)

        if self._is_empty(self.has_direct_replacement):
            self.MissingRequiredField("has_direct_replacement")
        if not isinstance(self.has_direct_replacement, NodeId):
            self.has_direct_replacement = NodeId(self.has_direct_replacement)

        if self.change_description is not None and not isinstance(self.change_description, str):
            self.change_description = str(self.change_description)

        super().__post_init__(**kwargs)


@dataclass
class NodeObsoletionWithNoDirectReplacement(NodeObsoletion):
    """
    An obsoletion change in which there is no direct replacement
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.NodeObsoletionWithNoDirectReplacement
    class_class_curie: ClassVar[str] = "kgcl:NodeObsoletionWithNoDirectReplacement"
    class_name: ClassVar[str] = "node obsoletion with no direct replacement"
    class_model_uri: ClassVar[URIRef] = KGCL.NodeObsoletionWithNoDirectReplacement

    id: Union[str, NodeObsoletionWithNoDirectReplacementId] = None
    has_nondirect_replacement: Union[Union[str, NodeId], List[Union[str, NodeId]]] = None
    change_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeObsoletionWithNoDirectReplacementId):
            self.id = NodeObsoletionWithNoDirectReplacementId(self.id)

        if self._is_empty(self.has_nondirect_replacement):
            self.MissingRequiredField("has_nondirect_replacement")
        if not isinstance(self.has_nondirect_replacement, list):
            self.has_nondirect_replacement = [self.has_nondirect_replacement] if self.has_nondirect_replacement is not None else []
        self.has_nondirect_replacement = [v if isinstance(v, NodeId) else NodeId(v) for v in self.has_nondirect_replacement]

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


@dataclass
class Configuration(YAMLRoot):
    """
    The meaning of operations can be configured
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.Configuration
    class_class_curie: ClassVar[str] = "kgcl:Configuration"
    class_name: ClassVar[str] = "configuration"
    class_model_uri: ClassVar[URIRef] = KGCL.Configuration

    name_predicate: Optional[str] = None
    definition_predicate: Optional[str] = None
    main_synonym_predicate: Optional[str] = None
    synonym_predicates: Optional[str] = None
    creator_predicate: Optional[str] = None
    contributor_predicate: Optional[str] = None
    obsoletion_workflow: Optional[str] = None
    obsoletion_policy: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name_predicate is not None and not isinstance(self.name_predicate, str):
            self.name_predicate = str(self.name_predicate)

        if self.definition_predicate is not None and not isinstance(self.definition_predicate, str):
            self.definition_predicate = str(self.definition_predicate)

        if self.main_synonym_predicate is not None and not isinstance(self.main_synonym_predicate, str):
            self.main_synonym_predicate = str(self.main_synonym_predicate)

        if self.synonym_predicates is not None and not isinstance(self.synonym_predicates, str):
            self.synonym_predicates = str(self.synonym_predicates)

        if self.creator_predicate is not None and not isinstance(self.creator_predicate, str):
            self.creator_predicate = str(self.creator_predicate)

        if self.contributor_predicate is not None and not isinstance(self.contributor_predicate, str):
            self.contributor_predicate = str(self.contributor_predicate)

        if self.obsoletion_workflow is not None and not isinstance(self.obsoletion_workflow, str):
            self.obsoletion_workflow = str(self.obsoletion_workflow)

        if self.obsoletion_policy is not None and not isinstance(self.obsoletion_policy, str):
            self.obsoletion_policy = str(self.obsoletion_policy)

        super().__post_init__(**kwargs)


@dataclass
class Session(YAMLRoot):
    """
    A session consists of a set of change sets bundled with the activities that generated those change sets
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KGCL.Session
    class_class_curie: ClassVar[str] = "kgcl:Session"
    class_name: ClassVar[str] = "session"
    class_model_uri: ClassVar[URIRef] = KGCL.Session

    change_set: Optional[Union[Dict[Union[str, ChangeId], Union[dict, Change]], List[Union[dict, Change]]]] = empty_dict()
    activity_set: Optional[Union[Dict[Union[str, ActivityId], Union[dict, Activity]], List[Union[dict, Activity]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="change_set", slot_type=Change, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="activity_set", slot_type=Activity, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.pull_request = Slot(uri=KGCL.pull_request, name="pull request", curie=KGCL.curie('pull_request'),
                   model_uri=KGCL.pull_request, domain=None, range=Optional[str])

slots.see_also = Slot(uri=RDFS.seeAlso, name="see also", curie=RDFS.curie('seeAlso'),
                   model_uri=KGCL.see_also, domain=None, range=Optional[str])

slots.creator = Slot(uri=DCTERMS.creator, name="creator", curie=DCTERMS.curie('creator'),
                   model_uri=KGCL.creator, domain=None, range=Optional[str])

slots.contributor = Slot(uri=DCTERMS.creator, name="contributor", curie=DCTERMS.curie('creator'),
                   model_uri=KGCL.contributor, domain=None, range=Optional[str])

slots.change_date = Slot(uri=DCTERMS.date, name="change date", curie=DCTERMS.curie('date'),
                   model_uri=KGCL.change_date, domain=None, range=Optional[str])

slots.has_undo = Slot(uri=KGCL.has_undo, name="has undo", curie=KGCL.curie('has_undo'),
                   model_uri=KGCL.has_undo, domain=Change, range=Optional[Union[str, ChangeId]])

slots.node_id = Slot(uri=KGCL.node_id, name="node id", curie=KGCL.curie('node_id'),
                   model_uri=KGCL.node_id, domain=None, range=Optional[Union[str, NodeId]])

slots.superclass = Slot(uri=KGCL.superclass, name="superclass", curie=KGCL.curie('superclass'),
                   model_uri=KGCL.superclass, domain=None, range=Optional[Union[str, NodeId]])

slots.about = Slot(uri=KGCL.about, name="about", curie=KGCL.curie('about'),
                   model_uri=KGCL.about, domain=None, range=Optional[Union[dict, OntologyElement]])

slots.about_node = Slot(uri=KGCL.about_node, name="about node", curie=KGCL.curie('about_node'),
                   model_uri=KGCL.about_node, domain=None, range=Optional[Union[str, NodeId]])

slots.about_edge = Slot(uri=KGCL.about_edge, name="about edge", curie=KGCL.curie('about_edge'),
                   model_uri=KGCL.about_edge, domain=None, range=Optional[Union[dict, Edge]])

slots.about_node_representation = Slot(uri=KGCL.about_node_representation, name="about node representation", curie=KGCL.curie('about_node_representation'),
                   model_uri=KGCL.about_node_representation, domain=None, range=Optional[str])

slots.target = Slot(uri=KGCL.target, name="target", curie=KGCL.curie('target'),
                   model_uri=KGCL.target, domain=None, range=Optional[str])

slots.old_value = Slot(uri=KGCL.old_value, name="old value", curie=KGCL.curie('old_value'),
                   model_uri=KGCL.old_value, domain=None, range=Optional[str])

slots.new_value = Slot(uri=KGCL.new_value, name="new value", curie=KGCL.curie('new_value'),
                   model_uri=KGCL.new_value, domain=None, range=Optional[str])

slots.language = Slot(uri=KGCL.language, name="language", curie=KGCL.curie('language'),
                   model_uri=KGCL.language, domain=None, range=Optional[str])

slots.datatype = Slot(uri=KGCL.datatype, name="datatype", curie=KGCL.curie('datatype'),
                   model_uri=KGCL.datatype, domain=None, range=Optional[str])

slots.new_language = Slot(uri=KGCL.new_language, name="new language", curie=KGCL.curie('new_language'),
                   model_uri=KGCL.new_language, domain=None, range=Optional[str])

slots.old_language = Slot(uri=KGCL.old_language, name="old language", curie=KGCL.curie('old_language'),
                   model_uri=KGCL.old_language, domain=None, range=Optional[str])

slots.qualifier = Slot(uri=KGCL.qualifier, name="qualifier", curie=KGCL.curie('qualifier'),
                   model_uri=KGCL.qualifier, domain=None, range=Optional[str])

slots.subclass = Slot(uri=KGCL.subclass, name="subclass", curie=KGCL.curie('subclass'),
                   model_uri=KGCL.subclass, domain=None, range=Optional[str])

slots.new_subclass = Slot(uri=KGCL.new_subclass, name="new subclass", curie=KGCL.curie('new_subclass'),
                   model_uri=KGCL.new_subclass, domain=None, range=Optional[str])

slots.new_property = Slot(uri=KGCL.new_property, name="new property", curie=KGCL.curie('new_property'),
                   model_uri=KGCL.new_property, domain=None, range=Optional[str])

slots.new_filler = Slot(uri=KGCL.new_filler, name="new filler", curie=KGCL.curie('new_filler'),
                   model_uri=KGCL.new_filler, domain=None, range=Optional[str])

slots.object_type = Slot(uri=KGCL.object_type, name="object type", curie=KGCL.curie('object_type'),
                   model_uri=KGCL.object_type, domain=None, range=Optional[str])

slots.new_object_type = Slot(uri=KGCL.new_object_type, name="new object type", curie=KGCL.curie('new_object_type'),
                   model_uri=KGCL.new_object_type, domain=None, range=Optional[str])

slots.old_object_type = Slot(uri=KGCL.old_object_type, name="old object type", curie=KGCL.curie('old_object_type'),
                   model_uri=KGCL.old_object_type, domain=None, range=Optional[str])

slots.new_value_type = Slot(uri=KGCL.new_value_type, name="new value type", curie=KGCL.curie('new_value_type'),
                   model_uri=KGCL.new_value_type, domain=None, range=Optional[str])

slots.old_value_type = Slot(uri=KGCL.old_value_type, name="old value type", curie=KGCL.curie('old_value_type'),
                   model_uri=KGCL.old_value_type, domain=None, range=Optional[str])

slots.subject_type = Slot(uri=KGCL.subject_type, name="subject type", curie=KGCL.curie('subject_type'),
                   model_uri=KGCL.subject_type, domain=None, range=Optional[str])

slots.subclass_type = Slot(uri=KGCL.subclass_type, name="subclass type", curie=KGCL.curie('subclass_type'),
                   model_uri=KGCL.subclass_type, domain=None, range=Optional[str])

slots.superclass_type = Slot(uri=KGCL.superclass_type, name="superclass type", curie=KGCL.curie('superclass_type'),
                   model_uri=KGCL.superclass_type, domain=None, range=Optional[str])

slots.predicate_type = Slot(uri=KGCL.predicate_type, name="predicate type", curie=KGCL.curie('predicate_type'),
                   model_uri=KGCL.predicate_type, domain=None, range=Optional[str])

slots.in_subset = Slot(uri=KGCL.in_subset, name="in subset", curie=KGCL.curie('in_subset'),
                   model_uri=KGCL.in_subset, domain=None, range=Optional[Union[dict, OntologySubset]])

slots.change_description = Slot(uri=KGCL.change_description, name="change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.change_description, domain=None, range=Optional[str])

slots.has_textual_diff = Slot(uri=KGCL.has_textual_diff, name="has textual diff", curie=KGCL.curie('has_textual_diff'),
                   model_uri=KGCL.has_textual_diff, domain=Change, range=Optional[Union[dict, "TextualDiff"]])

slots.change_set = Slot(uri=KGCL.change_set, name="change set", curie=KGCL.curie('change_set'),
                   model_uri=KGCL.change_set, domain=None, range=Optional[Union[Dict[Union[str, ChangeId], Union[dict, Change]], List[Union[dict, Change]]]])

slots.has_replacement = Slot(uri=KGCL.has_replacement, name="has replacement", curie=KGCL.curie('has_replacement'),
                   model_uri=KGCL.has_replacement, domain=NodeObsoletion, range=Optional[Union[str, NodeId]])

slots.has_direct_replacement = Slot(uri=KGCL.has_direct_replacement, name="has direct replacement", curie=KGCL.curie('has_direct_replacement'),
                   model_uri=KGCL.has_direct_replacement, domain=None, range=Optional[Union[str, NodeId]])

slots.has_nondirect_replacement = Slot(uri=KGCL.has_nondirect_replacement, name="has nondirect replacement", curie=KGCL.curie('has_nondirect_replacement'),
                   model_uri=KGCL.has_nondirect_replacement, domain=None, range=Optional[Union[Union[str, NodeId], List[Union[str, NodeId]]]])

slots.configuration__name_predicate = Slot(uri=KGCL.name_predicate, name="configuration__name_predicate", curie=KGCL.curie('name_predicate'),
                   model_uri=KGCL.configuration__name_predicate, domain=None, range=Optional[str])

slots.configuration__definition_predicate = Slot(uri=KGCL.definition_predicate, name="configuration__definition_predicate", curie=KGCL.curie('definition_predicate'),
                   model_uri=KGCL.configuration__definition_predicate, domain=None, range=Optional[str])

slots.configuration__main_synonym_predicate = Slot(uri=KGCL.main_synonym_predicate, name="configuration__main_synonym_predicate", curie=KGCL.curie('main_synonym_predicate'),
                   model_uri=KGCL.configuration__main_synonym_predicate, domain=None, range=Optional[str])

slots.configuration__synonym_predicates = Slot(uri=KGCL.synonym_predicates, name="configuration__synonym_predicates", curie=KGCL.curie('synonym_predicates'),
                   model_uri=KGCL.configuration__synonym_predicates, domain=None, range=Optional[str])

slots.configuration__creator_predicate = Slot(uri=KGCL.creator_predicate, name="configuration__creator_predicate", curie=KGCL.curie('creator_predicate'),
                   model_uri=KGCL.configuration__creator_predicate, domain=None, range=Optional[str])

slots.configuration__contributor_predicate = Slot(uri=KGCL.contributor_predicate, name="configuration__contributor_predicate", curie=KGCL.curie('contributor_predicate'),
                   model_uri=KGCL.configuration__contributor_predicate, domain=None, range=Optional[str])

slots.configuration__obsoletion_workflow = Slot(uri=KGCL.obsoletion_workflow, name="configuration__obsoletion_workflow", curie=KGCL.curie('obsoletion_workflow'),
                   model_uri=KGCL.configuration__obsoletion_workflow, domain=None, range=Optional[str])

slots.configuration__obsoletion_policy = Slot(uri=KGCL.obsoletion_policy, name="configuration__obsoletion_policy", curie=KGCL.curie('obsoletion_policy'),
                   model_uri=KGCL.configuration__obsoletion_policy, domain=None, range=Optional[str])

slots.associated_change_set = Slot(uri=KGCL.associated_change_set, name="associated change set", curie=KGCL.curie('associated_change_set'),
                   model_uri=KGCL.associated_change_set, domain=None, range=Optional[Union[Dict[Union[str, ChangeId], Union[dict, Change]], List[Union[dict, Change]]]])

slots.change_type = Slot(uri=KGCL.change_type, name="change type", curie=KGCL.curie('change_type'),
                   model_uri=KGCL.change_type, domain=None, range=Optional[Union[str, ChangeClassType]])

slots.count = Slot(uri=KGCL.count, name="count", curie=KGCL.curie('count'),
                   model_uri=KGCL.count, domain=None, range=Optional[int])

slots.change_1 = Slot(uri=KGCL.change_1, name="change 1", curie=KGCL.curie('change_1'),
                   model_uri=KGCL.change_1, domain=None, range=Optional[Union[str, NodeRenameId]])

slots.change_2 = Slot(uri=KGCL.change_2, name="change 2", curie=KGCL.curie('change_2'),
                   model_uri=KGCL.change_2, domain=None, range=Optional[Union[str, NewSynonymId]])

slots.subset = Slot(uri=KGCL.subset, name="subset", curie=KGCL.curie('subset'),
                   model_uri=KGCL.subset, domain=None, range=Optional[str])

slots.replaced_by = Slot(uri=KGCL.replaced_by, name="replaced by", curie=KGCL.curie('replaced_by'),
                   model_uri=KGCL.replaced_by, domain=None, range=Optional[Union[str, NodeId]])

slots.consider = Slot(uri=KGCL.consider, name="consider", curie=KGCL.curie('consider'),
                   model_uri=KGCL.consider, domain=None, range=Optional[Union[str, NodeId]])

slots.change_was_generated_by = Slot(uri=KGCL.was_generated_by, name="change_was generated by", curie=KGCL.curie('was_generated_by'),
                   model_uri=KGCL.change_was_generated_by, domain=Change, range=Optional[Union[str, ActivityId]])

slots.change_see_also = Slot(uri=KGCL.see_also, name="change_see also", curie=KGCL.curie('see_also'),
                   model_uri=KGCL.change_see_also, domain=Change, range=Optional[str])

slots.change_pull_request = Slot(uri=KGCL.pull_request, name="change_pull request", curie=KGCL.curie('pull_request'),
                   model_uri=KGCL.change_pull_request, domain=Change, range=Optional[str])

slots.change_creator = Slot(uri=KGCL.creator, name="change_creator", curie=KGCL.curie('creator'),
                   model_uri=KGCL.change_creator, domain=Change, range=Optional[str])

slots.change_change_date = Slot(uri=KGCL.change_date, name="change_change date", curie=KGCL.curie('change_date'),
                   model_uri=KGCL.change_change_date, domain=Change, range=Optional[str])

slots.multi_node_obsoletion_change_set = Slot(uri=KGCL.change_set, name="multi node obsoletion_change set", curie=KGCL.curie('change_set'),
                   model_uri=KGCL.multi_node_obsoletion_change_set, domain=MultiNodeObsoletion, range=Optional[Union[Dict[Union[str, NodeObsoletionId], Union[dict, "NodeObsoletion"]], List[Union[dict, "NodeObsoletion"]]]])

slots.multi_node_obsoletion_change_description = Slot(uri=KGCL.change_description, name="multi node obsoletion_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.multi_node_obsoletion_change_description, domain=MultiNodeObsoletion, range=Optional[str])

slots.multi_node_obsoletion_associated_change_set = Slot(uri=KGCL.associated_change_set, name="multi node obsoletion_associated change set", curie=KGCL.curie('associated_change_set'),
                   model_uri=KGCL.multi_node_obsoletion_associated_change_set, domain=MultiNodeObsoletion, range=Optional[Union[Dict[Union[str, ChangeId], Union[dict, Change]], List[Union[dict, Change]]]])

slots.change_set_summary_statistic_change_type = Slot(uri=KGCL.change_type, name="change set summary statistic_change type", curie=KGCL.curie('change_type'),
                   model_uri=KGCL.change_set_summary_statistic_change_type, domain=ChangeSetSummaryStatistic, range=Optional[Union[str, ChangeClassType]])

slots.change_set_summary_statistic_count = Slot(uri=KGCL.count, name="change set summary statistic_count", curie=KGCL.curie('count'),
                   model_uri=KGCL.change_set_summary_statistic_count, domain=ChangeSetSummaryStatistic, range=Optional[int])

slots.change_set_summary_statistic_property_value_set = Slot(uri=KGCL.property_value_set, name="change set summary statistic_property value set", curie=KGCL.curie('property_value_set'),
                   model_uri=KGCL.change_set_summary_statistic_property_value_set, domain=ChangeSetSummaryStatistic, range=Optional[Union[Union[dict, PropertyValue], List[Union[dict, PropertyValue]]]])

slots.obsoletion_about = Slot(uri=KGCL.about, name="obsoletion_about", curie=KGCL.curie('about'),
                   model_uri=KGCL.obsoletion_about, domain=None, range=Optional[Union[dict, OntologyElement]])

slots.obsoletion_has_undo = Slot(uri=KGCL.has_undo, name="obsoletion_has undo", curie=KGCL.curie('has_undo'),
                   model_uri=KGCL.obsoletion_has_undo, domain=None, range=Optional[Union[dict, "Obsoletion"]])

slots.unobsoletion_has_undo = Slot(uri=KGCL.has_undo, name="unobsoletion_has undo", curie=KGCL.curie('has_undo'),
                   model_uri=KGCL.unobsoletion_has_undo, domain=None, range=Optional[Union[dict, Obsoletion]])

slots.creation_has_undo = Slot(uri=KGCL.has_undo, name="creation_has undo", curie=KGCL.curie('has_undo'),
                   model_uri=KGCL.creation_has_undo, domain=None, range=Optional[Union[dict, Deletion]])

slots.add_to_subset_in_subset = Slot(uri=KGCL.in_subset, name="add to subset_in subset", curie=KGCL.curie('in_subset'),
                   model_uri=KGCL.add_to_subset_in_subset, domain=None, range=Optional[Union[dict, OntologySubset]])

slots.remove_from_subset_in_subset = Slot(uri=KGCL.in_subset, name="remove from subset_in subset", curie=KGCL.curie('in_subset'),
                   model_uri=KGCL.remove_from_subset_in_subset, domain=None, range=Optional[Union[dict, OntologySubset]])

slots.remove_from_subset_has_undo = Slot(uri=KGCL.has_undo, name="remove from subset_has undo", curie=KGCL.curie('has_undo'),
                   model_uri=KGCL.remove_from_subset_has_undo, domain=None, range=Optional[Union[dict, AddToSubset]])

slots.edge_change_subject = Slot(uri=KGCL.subject, name="edge change_subject", curie=KGCL.curie('subject'),
                   model_uri=KGCL.edge_change_subject, domain=EdgeChange, range=Optional[Union[str, NodeId]])

slots.edge_creation_change_description = Slot(uri=KGCL.change_description, name="edge creation_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.edge_creation_change_description, domain=EdgeCreation, range=Optional[str])

slots.edge_deletion_change_description = Slot(uri=KGCL.change_description, name="edge deletion_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.edge_deletion_change_description, domain=EdgeDeletion, range=Optional[str])

slots.edge_obsoletion_change_description = Slot(uri=KGCL.change_description, name="edge obsoletion_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.edge_obsoletion_change_description, domain=EdgeObsoletion, range=Optional[str])

slots.mapping_creation_change_description = Slot(uri=KGCL.change_description, name="mapping creation_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.mapping_creation_change_description, domain=MappingCreation, range=Optional[str])

slots.mapping_creation_subject = Slot(uri=KGCL.subject, name="mapping creation_subject", curie=KGCL.curie('subject'),
                   model_uri=KGCL.mapping_creation_subject, domain=MappingCreation, range=Optional[Union[str, NodeId]])

slots.mapping_creation_predicate = Slot(uri=KGCL.predicate, name="mapping creation_predicate", curie=KGCL.curie('predicate'),
                   model_uri=KGCL.mapping_creation_predicate, domain=MappingCreation, range=Optional[Union[str, NodeId]])

slots.mapping_creation_object = Slot(uri=KGCL.object, name="mapping creation_object", curie=KGCL.curie('object'),
                   model_uri=KGCL.mapping_creation_object, domain=MappingCreation, range=Optional[Union[str, NodeId]])

slots.node_move_change_description = Slot(uri=KGCL.change_description, name="node move_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_move_change_description, domain=NodeMove, range=Optional[str])

slots.node_deepening_change_description = Slot(uri=KGCL.change_description, name="node deepening_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_deepening_change_description, domain=NodeDeepening, range=Optional[str])

slots.node_shallowing_change_description = Slot(uri=KGCL.change_description, name="node shallowing_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_shallowing_change_description, domain=NodeShallowing, range=Optional[str])

slots.predicate_change_change_description = Slot(uri=KGCL.change_description, name="predicate change_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.predicate_change_change_description, domain=PredicateChange, range=Optional[str])

slots.node_rename_old_value = Slot(uri=KGCL.old_value, name="node rename_old value", curie=KGCL.curie('old_value'),
                   model_uri=KGCL.node_rename_old_value, domain=NodeRename, range=Optional[str])

slots.node_rename_new_value = Slot(uri=KGCL.new_value, name="node rename_new value", curie=KGCL.curie('new_value'),
                   model_uri=KGCL.node_rename_new_value, domain=NodeRename, range=Optional[str])

slots.node_rename_change_description = Slot(uri=KGCL.change_description, name="node rename_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_rename_change_description, domain=NodeRename, range=Optional[str])

slots.name_becomes_synonym_change_1 = Slot(uri=KGCL.change_1, name="name becomes synonym_change 1", curie=KGCL.curie('change_1'),
                   model_uri=KGCL.name_becomes_synonym_change_1, domain=NameBecomesSynonym, range=Optional[Union[str, NodeRenameId]])

slots.name_becomes_synonym_change_2 = Slot(uri=KGCL.change_2, name="name becomes synonym_change 2", curie=KGCL.curie('change_2'),
                   model_uri=KGCL.name_becomes_synonym_change_2, domain=NameBecomesSynonym, range=Optional[Union[str, NewSynonymId]])

slots.name_becomes_synonym_change_description = Slot(uri=KGCL.change_description, name="name becomes synonym_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.name_becomes_synonym_change_description, domain=NameBecomesSynonym, range=Optional[str])

slots.removed_node_from_subset_change_description = Slot(uri=KGCL.change_description, name="removed node from subset_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.removed_node_from_subset_change_description, domain=RemovedNodeFromSubset, range=Optional[str])

slots.removed_node_from_subset_about_node = Slot(uri=KGCL.about_node, name="removed node from subset_about node", curie=KGCL.curie('about_node'),
                   model_uri=KGCL.removed_node_from_subset_about_node, domain=RemovedNodeFromSubset, range=Optional[Union[str, NodeId]])

slots.removed_node_from_subset_subset = Slot(uri=KGCL.subset, name="removed node from subset_subset", curie=KGCL.curie('subset'),
                   model_uri=KGCL.removed_node_from_subset_subset, domain=RemovedNodeFromSubset, range=Optional[str])

slots.node_obsoletion_change_description = Slot(uri=KGCL.change_description, name="node obsoletion_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_obsoletion_change_description, domain=NodeObsoletion, range=Optional[str])

slots.node_obsoletion_associated_change_set = Slot(uri=KGCL.associated_change_set, name="node obsoletion_associated change set", curie=KGCL.curie('associated_change_set'),
                   model_uri=KGCL.node_obsoletion_associated_change_set, domain=NodeObsoletion, range=Optional[Union[Dict[Union[str, ChangeId], Union[dict, Change]], List[Union[dict, Change]]]])

slots.node_unobsoletion_change_description = Slot(uri=KGCL.change_description, name="node unobsoletion_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_unobsoletion_change_description, domain=NodeUnobsoletion, range=Optional[str])

slots.node_unobsoletion_replaced_by = Slot(uri=KGCL.replaced_by, name="node unobsoletion_replaced by", curie=KGCL.curie('replaced_by'),
                   model_uri=KGCL.node_unobsoletion_replaced_by, domain=NodeUnobsoletion, range=Optional[Union[str, NodeId]])

slots.node_unobsoletion_consider = Slot(uri=KGCL.consider, name="node unobsoletion_consider", curie=KGCL.curie('consider'),
                   model_uri=KGCL.node_unobsoletion_consider, domain=NodeUnobsoletion, range=Optional[Union[str, NodeId]])

slots.node_creation_change_description = Slot(uri=KGCL.change_description, name="node creation_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_creation_change_description, domain=NodeCreation, range=Optional[str])

slots.class_creation_change_description = Slot(uri=KGCL.change_description, name="class creation_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.class_creation_change_description, domain=ClassCreation, range=Optional[str])

slots.node_deletion_change_description = Slot(uri=KGCL.change_description, name="node deletion_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_deletion_change_description, domain=NodeDeletion, range=Optional[str])

slots.node_direct_merge_has_direct_replacement = Slot(uri=KGCL.has_direct_replacement, name="node direct merge_has direct replacement", curie=KGCL.curie('has_direct_replacement'),
                   model_uri=KGCL.node_direct_merge_has_direct_replacement, domain=NodeDirectMerge, range=Union[str, NodeId])

slots.node_direct_merge_about_node = Slot(uri=KGCL.about_node, name="node direct merge_about node", curie=KGCL.curie('about_node'),
                   model_uri=KGCL.node_direct_merge_about_node, domain=NodeDirectMerge, range=Optional[Union[str, NodeId]])

slots.node_direct_merge_change_description = Slot(uri=KGCL.change_description, name="node direct merge_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_direct_merge_change_description, domain=NodeDirectMerge, range=Optional[str])

slots.node_obsoletion_with_direct_replacement_has_direct_replacement = Slot(uri=KGCL.has_direct_replacement, name="node obsoletion with direct replacement_has direct replacement", curie=KGCL.curie('has_direct_replacement'),
                   model_uri=KGCL.node_obsoletion_with_direct_replacement_has_direct_replacement, domain=NodeObsoletionWithDirectReplacement, range=Union[str, NodeId])

slots.node_obsoletion_with_direct_replacement_change_description = Slot(uri=KGCL.change_description, name="node obsoletion with direct replacement_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_obsoletion_with_direct_replacement_change_description, domain=NodeObsoletionWithDirectReplacement, range=Optional[str])

slots.node_obsoletion_with_no_direct_replacement_has_nondirect_replacement = Slot(uri=KGCL.has_nondirect_replacement, name="node obsoletion with no direct replacement_has nondirect replacement", curie=KGCL.curie('has_nondirect_replacement'),
                   model_uri=KGCL.node_obsoletion_with_no_direct_replacement_has_nondirect_replacement, domain=NodeObsoletionWithNoDirectReplacement, range=Union[Union[str, NodeId], List[Union[str, NodeId]]])

slots.node_obsoletion_with_no_direct_replacement_change_description = Slot(uri=KGCL.change_description, name="node obsoletion with no direct replacement_change description", curie=KGCL.curie('change_description'),
                   model_uri=KGCL.node_obsoletion_with_no_direct_replacement_change_description, domain=NodeObsoletionWithNoDirectReplacement, range=Optional[str])
