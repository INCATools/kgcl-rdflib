
# Type: instance node


A node that is an individual

URI: [kgcl:InstanceNode](http://w3id.org/kgclInstanceNode)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Node],[Node]^-[InstanceNode&#124;id(i):string;name(i):string%20%3F],[Annotation])

## Parents

 *  is_a: [Node](Node.md) - Any named entity in an ontology. May be a class, individual, property

## Attributes


### Inherited from node:

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
| **Aliases:** | | named individual |
| **Mappings:** | | owl:NamedIndividual |

