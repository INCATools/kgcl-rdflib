SHELL=/bin/bash -o pipefail

EXTS = _datamodel.py .graphql .schema.json .owl -docs .shex

all: $(patsubst %,src/schema/ocl%, $(EXTS))

test: all

OUT = > $@.tmp && mv $@.tmp $@

src/schema/%_datamodel.py: src/schema/%.yaml
	gen-py-classes $< $(OUT)
src/schema/%.graphql: src/schema/%.yaml
	gen-graphql $< $(OUT)
src/schema/%.schema.json: src/schema/%.yaml
	gen-json-schema -t transaction $< $(OUT)
src/schema/%.shex: src/schema/%.yaml
	gen-shex $< $(OUT)
src/schema/%.csv: src/schema/%.yaml
	gen-csv $< $(OUT)
src/schema/%.owl: src/schema/%.yaml
	gen-owl $< $(OUT)
src/schema/%.ttl: src/schema/%.owl
	cp $< $@
src/schema/%-docs: src/schema/%.yaml
	pipenv run gen-markdown --dir $@ $<

deploy-docs:
	cp src/schema/ocl-docs/*md docs/
