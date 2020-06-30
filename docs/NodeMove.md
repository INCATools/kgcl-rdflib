
# Type: node move


A node move is a combination of deleting a parent edge and adding a parent edge, where the edge label is preserved and the object/parent node changes

URI: [ocl:NodeMove](http://w3id.org/oclNodeMove)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[NodeMove&#124;about(i):string%20%3F;old_value(i):string%20%3F;new_value(i):string%20%3F]^-[NodeDeepening],%20[EdgeChange]^-[NodeMove])

## Parents

 *  is_a: [EdgeChange](EdgeChange.md) - A change in which the entity changes is an edge

## Children

 * [NodeDeepening](NodeDeepening.md) - A node move in which a node where the destination is a proper descendant of the original location

## Referenced by class


## Attributes


### Inherited from edge change:

 * [edge change➞about](edge_change_about.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: [EdgeChange](EdgeChange.md)

### Inherited from node rename:

 * [node rename➞old value](node_rename_old_value.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: [NodeRename](NodeRename.md)
 * [node rename➞new value](node_rename_new_value.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: [NodeRename](NodeRename.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Examples:** | | Example(value='changing a is-a b to a is-a c', description=None) |

