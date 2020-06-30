
# Type: edge change


A change in which the entity changes is an edge

URI: [ocl:EdgeChange](http://w3id.org/oclEdgeChange)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[EdgeChange&#124;about:string%20%3F;old_value(i):string%20%3F;new_value(i):string%20%3F]^-[NodeMove],%20[EdgeChange]^-[EdgeLabelChange],%20[SimpleChange]^-[EdgeChange])

## Parents

 *  is_a: [SimpleChange](SimpleChange.md) - A change that is about a single ontology element

## Children

 * [EdgeLabelChange](EdgeLabelChange.md) - An edge change where the edge label (relationship type) is modified.
 * [NodeMove](NodeMove.md) - A node move is a combination of deleting a parent edge and adding a parent edge, where the edge label is preserved and the object/parent node changes

## Referenced by class


## Attributes


### Own

 * [edge change➞about](edge_change_about.md)  <sub>OPT</sub>
    * range: [String](types/String.md)

### Inherited from node rename:

 * [node rename➞old value](node_rename_old_value.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: [NodeRename](NodeRename.md)
 * [node rename➞new value](node_rename_new_value.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: [NodeRename](NodeRename.md)

### Domain for slot:

 * [edge change➞about](edge_change_about.md)  <sub>OPT</sub>
    * range: [String](types/String.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | axiom change |
|  | | triple change |

