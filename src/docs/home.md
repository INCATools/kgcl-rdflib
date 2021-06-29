# Introduction

## About

* [Browse Schema](https://cmungall.github.io/knowledge-graph-change-language/)
* [GitHub](https://github.com/cmungall/knowledge-graph-change-language)

The goal of this project is to define a high level language and data
model that can be used to describe changes in ontologies and more
generally, "knowledge graphs".

The language should be a higher level of abstraction than a low-level
owl or rdf diff. For example, conceptually, changing the parent of a
class in ontology is a single event, which can be broken down into a
delete and add operation (see [NodeMove](https://cmungall.github.io/knowledge-graph-change-language/NodeMove/)).

An example of a NodeMove instance, correcting an incorrect placement from being part-of leg to part-of arm:

```turtle
[ a kgcl:NodeMove ;
  kgcl:about UBERON:0002398 ## manus
  kgcl:old_value UBERON:0002103 ## hindlimb
  kgcl:old_predicate BFO:0000050 ## part_of
  kgcl:new_value UBERON:0002102 ## forelimb
  kgcl:new_predicate BFO:0000050 ## part_of
]
```

## Examples

See the [examples/](https://github.com/cmungall/knowledge-graph-change-language/tree/master/examples) folder

## Apply and Diff operations

Change objects can be used in two directions:

 * Diff: given two ontologies O1 and O2, generate a list of changes C
 * Apply: Given a list of changes C, apply to ontology O1 to generate O2

The Diff operation is intended to be used to provide KG/Ontology authors a high level view of changes.

The Apply operation can take diffs as inputs. The diffs can have different serializations:

 * A direct instantiation of the classes design in the model, in one of:
   * JSON
   * YAML
   * RDF
 * A string serialization
 * A tsv serialization, for use in spreadsheets

For example an instance of a rename class on Uberon to change the
primary label of an entity may be:

```turtle
[ a kgcl:NodeRename ;
  kgcl:about UBERON:0002398 ;
  kgcl:old_value "manus" ;
  kgcl:new_value "hand" ]
```

This can be serialized as

 * `rename UBERON:0002398 from 'manus' to 'hand'`

TBD: we also want an even more compact form:

 * `rename 'manus' to 'hand'`

There are a few user stories for the Apply operation:

 * As an ontology contributor, I want to quickly describe and apply a change to an ontology, so that I do not have to clone a github repo, open protege, make a PR
 * As an ontology tool creator, I want to generate "suggestions" for changes to an ontology, so that a human user can spot-check them and apply all valid ones
    * Example: a tool that makes suggested lexical [changes to text defs to conform to standards](https://douroucouli.wordpress.com/2019/07/08/ontotip-write-simple-concise-clear-operational-textual-definitions/)
    * An OWL logic tool may suggest redundant axioms that can safely be removed. The curator feels safest vetting these via the intermediate form


## Intended use in GitHub

One intended killer app for this language is the ability for a human or agent to specify a set of changes in a GitHub ticket in a human-readable transparent way, and for a bot to create a PR from the computable description in the ticket.

This would be ideal for "drive-by" edits and Term Brokers.

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


