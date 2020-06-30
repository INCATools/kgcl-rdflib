
# Type: class node


A node that is a class

URI: [ocl:ClassNode](http://w3id.org/oclClassNode)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Annotation]<annotation%20set(i)%200..1-++[ClassNode&#124;id(i):string;name(i):string%20%3F],%20[Node]^-[ClassNode])

## Parents

 *  is_a: [Node](Node.md) - Any named entity in an ontology. May be a class, individual, property

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
    * inherited from: None

### Inherited from node:

 * [id](id.md)  <sub>REQ</sub>
    * Description: CURIE or URI
    * range: [String](types/String.md)
    * inherited from: None
 * [name](name.md)  <sub>OPT</sub>
    * range: [String](types/String.md)
    * inherited from: None

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | concept |
| **Mappings:** | | owl:Class |

