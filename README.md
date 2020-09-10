# Ontology Change Language

This repo includes schema and code for an Ontology Change Language

The overall idea is laid out in:

https://docs.google.com/document/d/1__7p64FOI5ZhiZ6F2TXtUc8JN1XXGwglOiVRrlg9G_c/edit#heading=h.xadk0a3ee8g

The goal is to provide a high level abstracted graph-oriented change
language that is intended for describing changes in ontologies and
ontology-like artefacts. The level of abstraction is intentionally at
a higher level than either RDF or OWL. It currently does not attempt
to encapsulate all of OWL. Instead it focuses on the majority of
operations performed on ontologies.

## Schema

Browse the schema here: [http://cmungall.github.io/ontology-change-language](http://cmungall.github.io/ontology-change-language)

See the [schema/](https://github.com/cmungall/ontology-change-language/tree/master/src/schema/) folder

The source is in YAML (biolinkml)

Currently the main derived artefacts of interest are:

 - [JSON Schema](src/schema/ocl.schema.json)
 - [Python dataclasses](src/schema/ocl_datamodel.py)
 - [GraphQL](src/schema/ocl.graphql)

Note there is also an OWL vocabulary rendering, and a schema in ShEx (TODO: fix issues with namespaces)

 - [JSON Schema](src/schema/ocl.schema.json)
 - [Python dataclasses](src/schema/ocl_datamodel.py)


It is likely we will bind this into [owl-diff](https://github.com/balhoff/owl-diff) so compilation to scala traits likely in future.

Note that transactions can themselves be represented in RDF. This can
be either JSON-LD following the schema above or native. The [ShEx
Schema](src/schema/ocl.shex) constrains the shape of the RDF graph.
