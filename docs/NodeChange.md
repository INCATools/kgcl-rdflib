
# Type: node change




URI: [ocl:NodeChange](http://w3id.org/oclNodeChange)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[NodeChange&#124;about:string%20%3F;old_value(i):string%20%3F;new_value(i):string%20%3F]^-[NodeRename],%20[NodeChange]^-[NodeObsoletion],%20[NodeChange]^-[NodeDeletion],%20[NodeChange]^-[NodeCreation],%20[SimpleChange]^-[NodeChange])

## Parents

 *  is_a: [SimpleChange](SimpleChange.md) - A change that is about a single ontology element

## Children

 * [NodeCreation](NodeCreation.md)
 * [NodeDeletion](NodeDeletion.md) - Deletion of a node from the graph. Note it is recommended nodes are obsoleted and never merged, but this operation exists to represent deletions in ontologies, accidental or otherwise
 * [NodeObsoletion](NodeObsoletion.md)
 * [NodeRename](NodeRename.md)

## Referenced by class


## Attributes


### Own

 * [node change➞about](node_change_about.md)  <sub>OPT</sub>
    * range: [String](types/String.md)

### Inherited from node rename:

 * [node rename➞old value](node_rename_old_value.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: [NodeRename](NodeRename.md)
 * [node rename➞new value](node_rename_new_value.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: [NodeRename](NodeRename.md)

### Domain for slot:

 * [node change➞about](node_change_about.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
