
# Type: node rename


A node change where the name (aka rdfs:label) of the node changes

URI: [ocl:NodeRename](http://w3id.org/oclNodeRename)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[NodeChange]^-[NodeRename&#124;old_value:string%20%3F;new_value:string%20%3F;about(i):string%20%3F])

## Parents

 *  is_a: [NodeChange](NodeChange.md) - A simple change where the change is about a node

## Referenced by class


## Attributes


### Own

 * [node rename➞new value](node_rename_new_value.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
 * [node rename➞old value](node_rename_old_value.md)  <sub>OPT</sub>
    * range: [String](types/String.md)

### Inherited from node change:

 * [node change➞about](node_change_about.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: [NodeChange](NodeChange.md)

### Domain for slot:

 * [node rename➞new value](node_rename_new_value.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
 * [node rename➞old value](node_rename_old_value.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
