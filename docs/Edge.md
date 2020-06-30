
# Type: edge


A relationship between two nodes. We assume owlstar or similar for existential restrictions

URI: [ocl:Edge](http://w3id.org/oclEdge)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Annotation]<annotation%20set%200..1-++[Edge],%20[Node]<object%200..1-%20[Edge],%20[Node]<edge%20label%200..1-%20[Edge],%20[Node]<subject%200..1-%20[Edge],%20[OntologyElement]^-[Edge])

## Parents

 *  is_a: [OntologyElement](OntologyElement.md) - Any component of an ontology or knowledge graph

## Attributes


### Own

 * [annotation set](annotation_set.md)  <sub>OPT</sub>
    * range: [Annotation](Annotation.md)
 * [edge label](edge_label.md)  <sub>OPT</sub>
    * range: [Node](Node.md)
 * [object](object.md)  <sub>OPT</sub>
    * range: [Node](Node.md)
 * [subject](subject.md)  <sub>OPT</sub>
    * range: [Node](Node.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | triple |
|  | | axiom |
| **Mappings:** | | owl:Axiom |
|  | | rdf:Statement |

