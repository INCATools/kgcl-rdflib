
# Type: node


Any named entity in an ontology. May be a class, individual, property

URI: [ocl:Node](http://w3id.org/oclNode)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Annotation]<annotation%20set%200..1-++[Node&#124;id:string;name:string%20%3F],%20[Node]^-[InstanceNode],%20[Node]^-[ClassNode],%20[OntologyElement]^-[Node])

## Parents

 *  is_a: [OntologyElement](OntologyElement.md) - Any component of an ontology or knowledge graph

## Children

 * [ClassNode](ClassNode.md) - A node that is a class
 * [InstanceNode](InstanceNode.md) - A node that is an individual

## Referenced by class

 *  **None** *[edge label](edge_label.md)*  <sub>OPT</sub>  **[Node](Node.md)**
 *  **None** *[object](object.md)*  <sub>OPT</sub>  **[Node](Node.md)**
 *  **None** *[property](property.md)*  <sub>OPT</sub>  **[Node](Node.md)**
 *  **None** *[subject](subject.md)*  <sub>OPT</sub>  **[Node](Node.md)**

## Attributes


### Own

 * [id](id.md)  <sub>REQ</sub>
    * Description: CURIE or URI
    * range: [String](types/String.md)
 * [name](name.md)  <sub>OPT</sub>
    * range: [String](types/String.md)

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

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | entity |

