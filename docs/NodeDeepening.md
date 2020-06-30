
# Type: node deepening


A node move in which a node where the destination is a proper descendant of the original location

URI: [ocl:NodeDeepening](http://w3id.org/oclNodeDeepening)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[NodeMove]^-[NodeDeepening&#124;about(i):string%20%3F;old_value(i):string%20%3F;new_value(i):string%20%3F])

## Parents

 *  is_a: [NodeMove](NodeMove.md) - A node move is a combination of deleting a parent edge and adding a parent edge, where the edge label is preserved and the object/parent node changes

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
| **Examples:** | | Example(value='changing a is-a b to a is-a c, where c is a subclass of b', description=None) |

