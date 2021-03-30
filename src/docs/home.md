# Introduction

* [Browse Schema](https://cmungall.github.io/knowledge-graph-change-language/)

The goal of this project is to define a high level language and data
model that can be used to describe changes in ontologies and more
generally, "knowledge graphs".

The language should be a higher level of abstraction than a low-level
owl or rdf diff. For example, conceptually, changing the parent of a
class in ontology is a single event, which can be broken down into a
delete and add operation.

The goal is to provide both a data model and a syntax for describing
changes. This can be used in two directions:

 * Generate: given two ontologies O1 and O2, generate a list of changes C
 * Parse: Given a list of changes C, apply to ontology O1 to generate O2

The Parse operation is anticipated to be useful in a number of ways
Authoring operations in a file then calling a proposed new command robot apply
Killer app: A user authoring drive-by edits into a github ticket (“create a term X, place X under Y”; “obsolete Z”), with an agent/bot taking care of creating a Pull Request
Standard protocol for Term Brokers
The Generate operation may be non-deterministic as there may be multiple solutions to reducing a list of primitive diff operations to higher level operations

The overall idea is laid out in: [this google doc](https://docs.google.com/document/d/1__7p64FOI5ZhiZ6F2TXtUc8JN1XXGwglOiVRrlg9G_c/edit#heading=h.xadk0a3ee8g)


## Schema Source

The linkml source yaml can be found here:

 * [src/schema](https://github.com/cmungall/knowledge-graph-change-language/tree/master/src/schema)

The source is in LinkML. The best way to browse this is via the [generated markdown](https://cmungall.github.io/knowledge-graph-change-language/)

An example class is [kgcl:NodeRename](https://cmungall.github.io/knowledge-graph-change-language/NodeRename/)

``` yaml
classes:
  node rename:
    is_a: node change
    description: >-
      A node change where the name (aka rdfs:label) of the node changes
    slots:
      - old value
      - new value
      - has textual diff      
    slot_usage:
      old value:
        multivalued: false
      new value:
        multivalued: false
      change description:
        string_serialization: "renaming {about} from {old value} to {new value}"
```

## Derived Artefacts

 * [jsonschema](https://github.com/cmungall/knowledge-graph-change-language/tree/master/jsonschema)
 * [python dataclasses](https://github.com/cmungall/knowledge-graph-change-language/tree/master/python)
 * [shex](https://github.com/cmungall/knowledge-graph-change-language/tree/master/shex)
 * [graphql](https://github.com/cmungall/knowledge-graph-change-language/tree/master/graphql)
 * [owl](https://github.com/cmungall/knowledge-graph-change-language/tree/master/owl)


## Python Classes

 * [python dataclasses](https://github.com/cmungall/knowledge-graph-change-language/tree/master/python)

Example code:

``` python
from kgcl import NodeRename

change = NodeRename(about="UBERON:1234567", old_value="limb skin", new_value="skin of limb")
```

## JSON Schema

 * [jsonschema](https://github.com/cmungall/knowledge-graph-change-language/tree/master/jsonschema)

Example snippet:

```json
      "NodeRename": {
         "additionalProperties": false,
         "description": "A node change where the name (aka rdfs:label) of the node changes",
         "properties": {
            "about": {
               "type": "string"
            },
            "change_description": {
               "type": "string"
            },
            "has_textual_diff": {
               "$ref": "#/definitions/TextualDiff"
            },
            "new_value": {
               "type": "string"
            },
            "old_value": {
               "type": "string"
            },
            "was_generated_by": {
               "type": "string"
            }
         },
         "required": [],
         "title": "NodeRename",
         "type": "object"
      },
```

## Implementation

Currently this is just a schema, no implementation.

It is likely we will bind this into [owl-diff](https://github.com/balhoff/owl-diff) so compilation to scala traits likely in future.

Note that transactions can themselves be represented in RDF. This can
be either JSON-LD following the schema above or native. The ShEx
Schema constrains the shape of the RDF graph.


