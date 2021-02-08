# Introduction

The overall idea is laid out in: [this google doc](https://docs.google.com/document/d/1__7p64FOI5ZhiZ6F2TXtUc8JN1XXGwglOiVRrlg9G_c/edit#heading=h.xadk0a3ee8g)

The goal is to provide a high level abstracted graph-oriented change
language that is intended for describing changes in ontologies and
ontology-like artefacts. The level of abstraction is intentionally at
a higher level than either RDF or OWL. It currently does not attempt
to encapsulate all of OWL. Instead it focuses on the majority of
operations performed on ontologies.

## Source

The linkml source yaml can be found here:

 * [src/schema](https://github.com/cmungall/knowledge-graph-change-language/tree/master/src/schema)

## Derived Artefacts

 * [jsonschema](https://github.com/cmungall/knowledge-graph-change-language/tree/master/jsonschema)
 * [python dataclasses](https://github.com/cmungall/knowledge-graph-change-language/tree/master/python)
 * [shex](https://github.com/cmungall/knowledge-graph-change-language/tree/master/shex)
 * [graphql](https://github.com/cmungall/knowledge-graph-change-language/tree/master/graphql)
 * [owl](https://github.com/cmungall/knowledge-graph-change-language/tree/master/owl)

## Implementation

Currently this is just a schema, no implemehtation.

It is likely we will bind this into [owl-diff](https://github.com/balhoff/owl-diff) so compilation to scala traits likely in future.

Note that transactions can themselves be represented in RDF. This can
be either JSON-LD following the schema above or native. The ShEx
Schema constrains the shape of the RDF graph.


