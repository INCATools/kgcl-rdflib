
# Type: edge


A relationship between two nodes. We assume owlstar or similar for existential restrictions

URI: [ocl:Edge](http://w3id.org/oclEdge)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[OntologyElement],[Node],[Annotation]<annotation%20set%200..1-++[Edge],[Node]<object%200..1-%20[Edge],[Node]<edge%20label%200..1-%20[Edge],[Node]<subject%200..1-%20[Edge],[OntologyElement]^-[Edge],[Annotation])

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
|  | | relationship |
| **Mappings:** | | owl:Axiom |
|  | | rdf:Statement |

