
# Ocl schema


A data model for describing change operations at a high level on an ontology or ontology-like artefact


### Classes

 * [Change](Change.md) - Any change perform on an ontology or knowledge graph
    * [DatatypeChange](DatatypeChange.md)
 * [ComplexChange](ComplexChange.md) - A change that is is a composition of other changes
 * [OntologyElement](OntologyElement.md) - Any component of an ontology or knowledge graph
    * [Annotation](Annotation.md)
    * [Edge](Edge.md)
    * [Node](Node.md)
       * [ClassNode](ClassNode.md)
       * [InstanceNode](InstanceNode.md)
 * [SimpleChange](SimpleChange.md) - A change that is about a single ontology element
    * [EdgeChange](EdgeChange.md)
       * [EdgeLabelChange](EdgeLabelChange.md)
       * [NodeMove](NodeMove.md) - A node move is a combination of deleting a parent edge and adding a parent edge, where the edge label is preserved and the object/parent node changes
    * [NodeChange](NodeChange.md)
       * [NodeCreation](NodeCreation.md)
       * [NodeDeletion](NodeDeletion.md) - Deletion of a node from the graph. Note it is recommended nodes are obsoleted and never merged, but this operation exists to represent deletions in ontologies, accidental or otherwise
       * [NodeObsoletion](NodeObsoletion.md)
          * [NodeObsoletionWithMerge](NodeObsoletionWithMerge.md) - An obsoletion change in which information from the obsoleted node is moved to a single target
          * [NodeObsoletionWithSplit](NodeObsoletionWithSplit.md) - An obsoletion change in which information from the obsoleted node is moved selectively to multiple targets
       * [NodeRename](NodeRename.md)
 * [Transaction](Transaction.md) - A unified set of changes. Could be a single change, or the results of an ontology diff

### Mixins

 * [ChangeMixin](ChangeMixin.md) - root class for all change mixins
    * [Creation](Creation.md)
    * [Deletion](Deletion.md)
    * [Obsoletion](Obsoletion.md)
 * [Creation](Creation.md)
 * [Deletion](Deletion.md)
 * [Obsoletion](Obsoletion.md)

### Slots

 * [about](about.md) - The 'focus' entity on which the change operates
    * [edge change➞about](edge_change_about.md)
    * [node change➞about](node_change_about.md)
 * [annotation set](annotation_set.md)
 * [change description](change_description.md) - A string serialization of the change
    * [edge label change➞change description](edge_label_change_change_description.md)
    * [node creation➞change description](node_creation_change_description.md)
    * [node deletion➞change description](node_deletion_change_description.md)
    * [node move➞change description](node_move_change_description.md)
    * [node obsoletion with merge➞change description](node_obsoletion_with_merge_change_description.md)
    * [node obsoletion with split➞change description](node_obsoletion_with_split_change_description.md)
    * [node obsoletion➞change description](node_obsoletion_change_description.md)
    * [node rename➞change description](node_rename_change_description.md)
 * [change set](change_set.md)
 * [edge label](edge_label.md)
 * [filler](filler.md)
 * [id](id.md) - CURIE or URI
 * [name](name.md)
 * [new value](new_value.md) - The value of a property held in the old instance of the ontology
    * [node rename➞new value](node_rename_new_value.md)
 * [object](object.md)
 * [old value](old_value.md) - The value of a property held in the old instance of the ontology
    * [node rename➞old value](node_rename_old_value.md)
 * [property](property.md)
 * [subject](subject.md)
 * [target](target.md) - The secondary entity on which the change operates
    * [node obsoletion with merge➞target](node_obsoletion_with_merge_target.md)
    * [node obsoletion with split➞target](node_obsoletion_with_split_target.md)

### Types


#### Built in

 * **Bool**
 * **ElementIdentifier**
 * **NCName**
 * **NodeIdentifier**
 * **URI**
 * **URIorCURIE**
 * **XSDDate**
 * **XSDDateTime**
 * **XSDTime**
 * **float**
 * **int**
 * **str**

#### Defined

 * [Boolean](types/Boolean.md)  (**Bool**)  - A binary (true or false) value
 * [Date](types/Date.md)  (**XSDDate**)  - a date (year, month and day) in an idealized calendar
 * [Datetime](types/Datetime.md)  (**XSDDateTime**)  - The combination of a date and time
 * [Double](types/Double.md)  (**float**)  - A real number that conforms to the xsd:double specification
 * [Float](types/Float.md)  (**float**)  - A real number that conforms to the xsd:float specification
 * [Integer](types/Integer.md)  (**int**)  - An integer
 * [Ncname](types/Ncname.md)  (**NCName**)  - Prefix part of CURIE
 * [Nodeidentifier](types/Nodeidentifier.md)  (**NodeIdentifier**)  - A URI, CURIE or BNODE that represents a node in a model.
 * [Objectidentifier](types/Objectidentifier.md)  (**ElementIdentifier**)  - A URI or CURIE that represents an object in the model.
 * [String](types/String.md)  (**str**)  - A character string
 * [Time](types/Time.md)  (**XSDTime**)  - A time object represents a (local) time of day, independent of any particular day
 * [Uri](types/Uri.md)  (**URI**)  - a complete URI
 * [Uriorcurie](types/Uriorcurie.md)  (**URIorCURIE**)  - a URI or a CURIE
