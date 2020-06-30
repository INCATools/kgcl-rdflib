
# Type: node deletion


Deletion of a node from the graph. Note it is recommended nodes are obsoleted and never merged, but this operation exists to represent deletions in ontologies, accidental or otherwise

URI: [ocl:NodeDeletion](http://w3id.org/oclNodeDeletion)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[NodeDeletion&#124;about(i):string%20%3F;old_value(i):string%20%3F;new_value(i):string%20%3F]uses%20-.->[Deletion],%20[NodeChange]^-[NodeDeletion])

## Parents

 *  is_a: [NodeChange](NodeChange.md)

## Uses Mixins

 *  mixin: [Deletion](Deletion.md)

## Referenced by class


## Attributes


### Inherited from node change:

 * [node change➞about](node_change_about.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: [NodeChange](NodeChange.md)

### Inherited from node rename:

 * [node rename➞old value](node_rename_old_value.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: [NodeRename](NodeRename.md)
 * [node rename➞new value](node_rename_new_value.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: [NodeRename](NodeRename.md)
