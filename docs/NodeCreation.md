
# Type: node creation




URI: [ocl:NodeCreation](http://w3id.org/oclNodeCreation)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Annotation]<annotation%20set%200..1-++[NodeCreation&#124;id:string;name:string%20%3F;about(i):string%20%3F;old_value(i):string%20%3F;new_value(i):string%20%3F],%20[NodeCreation]uses%20-.->[Obsoletion],%20[NodeChange]^-[NodeCreation])

## Parents

 *  is_a: [NodeChange](NodeChange.md) - A simple change where the change is about a node

## Uses Mixins

 *  mixin: [Obsoletion](Obsoletion.md)

## Referenced by class


## Attributes


### Inherited from edge:

 * [subject](subject.md)  <sub>OPT</sub>
    * range: [Node](Node.md)
    * inherited from: None
 * [edge label](edge_label.md)  <sub>OPT</sub>
    * range: [Node](Node.md)
    * inherited from: None
 * [object](object.md)  <sub>OPT</sub>
    * range: [Node](Node.md)
    * inherited from: None
 * [annotation set](annotation_set.md)  <sub>OPT</sub>
    * range: [Annotation](Annotation.md)

### Inherited from node:

 * [id](id.md)  <sub>REQ</sub>
    * Description: CURIE or URI
    * range: [String](types/String.md)
 * [name](name.md)  <sub>OPT</sub>
    * range: [String](types/String.md)

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
