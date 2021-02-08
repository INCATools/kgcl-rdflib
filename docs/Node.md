
# Type: node


Any named entity in an ontology. May be a class, individual, property

URI: [kgcl:Node](http://w3id.org/kgclNode)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[OntologyElement],[NodeUnobsoletion],[NodeObsoletion],[Annotation]<annotation%20set%200..1-++[Node&#124;id:string;name:string%20%3F],[EdgeCreation]-%20edge%20label%200..1>[Node],[EdgeDeletion]-%20edge%20label%200..1>[Node],[EdgeObsoletion]-%20edge%20label%200..1>[Node],[Edge]-%20edge%20label%200..1>[Node],[NodeObsoletion]-%20consider%200..1>[Node],[NodeObsoletion]-%20replaced%20by%200..1>[Node],[NodeUnobsoletion]-%20consider%200..1>[Node],[NodeUnobsoletion]-%20replaced%20by%200..1>[Node],[EdgeCreation]-%20object%200..1>[Node],[EdgeDeletion]-%20object%200..1>[Node],[EdgeObsoletion]-%20object%200..1>[Node],[Edge]-%20object%200..1>[Node],[PropertyValue]-%20property%200..1>[Node],[Annotation]-%20property(i)%200..1>[Node],[EdgeCreation]-%20subject%200..1>[Node],[EdgeDeletion]-%20subject%200..1>[Node],[EdgeObsoletion]-%20subject%200..1>[Node],[Edge]-%20subject%200..1>[Node],[Node]^-[InstanceNode],[Node]^-[ClassNode],[OntologyElement]^-[Node],[PropertyValue],[InstanceNode],[EdgeObsoletion],[EdgeDeletion],[EdgeCreation],[Edge],[ClassNode],[Annotation])

## Parents

 *  is_a: [OntologyElement](OntologyElement.md) - Any component of an ontology or knowledge graph

## Children

 * [ClassNode](ClassNode.md) - A node that is a class
 * [InstanceNode](InstanceNode.md) - A node that is an individual

## Referenced by class

 *  **None** *[consider](consider.md)*  <sub>OPT</sub>  **[Node](Node.md)**
 *  **None** *[edge label](edge_label.md)*  <sub>OPT</sub>  **[Node](Node.md)**
 *  **[NodeObsoletion](NodeObsoletion.md)** *[node obsoletion➞consider](node_obsoletion_consider.md)*  <sub>OPT</sub>  **[Node](Node.md)**
 *  **[NodeObsoletion](NodeObsoletion.md)** *[node obsoletion➞replaced by](node_obsoletion_replaced_by.md)*  <sub>OPT</sub>  **[Node](Node.md)**
 *  **[NodeUnobsoletion](NodeUnobsoletion.md)** *[node unobsoletion➞consider](node_unobsoletion_consider.md)*  <sub>OPT</sub>  **[Node](Node.md)**
 *  **[NodeUnobsoletion](NodeUnobsoletion.md)** *[node unobsoletion➞replaced by](node_unobsoletion_replaced_by.md)*  <sub>OPT</sub>  **[Node](Node.md)**
 *  **None** *[object](object.md)*  <sub>OPT</sub>  **[Node](Node.md)**
 *  **None** *[property](property.md)*  <sub>OPT</sub>  **[Node](Node.md)**
 *  **None** *[replaced by](replaced_by.md)*  <sub>OPT</sub>  **[Node](Node.md)**
 *  **None** *[subject](subject.md)*  <sub>OPT</sub>  **[Node](Node.md)**

## Attributes


### Own

 * [annotation set](annotation_set.md)  <sub>OPT</sub>
    * range: [Annotation](Annotation.md)
 * [id](id.md)  <sub>REQ</sub>
    * Description: CURIE or URI
    * range: [String](types/String.md)
 * [name](name.md)  <sub>OPT</sub>
    * range: [String](types/String.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | entity |

