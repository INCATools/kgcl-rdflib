"""
convenience wrappers around linkml runtime, for doing basic conversion between objects
and serialization formats.

The top level class is a Session object

Some of this will become unnecessary in the future
"""
import yaml
import click
import logging
import os
import kgcl.model as model
from rdflib import Graph
from typing import List
from uuid import uuid1
import json

from kgcl.model.kgcl import Change, Session
from kgcl.model.prov import Activity
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.dumpers.json_dumper import JSONDumper
from linkml_runtime.dumpers.rdf_dumper import RDFDumper


THIS_DIR = os.path.abspath(os.path.dirname(__file__))
LD = os.path.join(THIS_DIR, '../ldcontext/kgcl.context.jsonld')

def get_context() -> str:
    """
    gets the JSON-LD context
    """
    with open(LD) as stream:
        context = json.load(stream)
        context['@context']['ANAT'] = {'@id': 'https://example.org/anatomy/', '@prefix': True}
        context['@context']['uuid'] = {'@id': 'https://example.org/uuid/', '@prefix': True}
        context['@context']['type'] = {'@type': '@id'}
        return json.dumps(context)

def to_json(session: Session) -> Graph:
    """
    converts a session object to plain json
    """
    dumper = JSONDumper()
    jsons = dumper.dumps(session)
    return jsons

def to_jsonld(session: Session) -> str:
    """
    converts a session object to JSON-LD
    """
    dumper = JSONDumper()
    jsons = dumper.dumps(session, get_context())
    return jsons

def to_rdf(session: Session) -> Graph:
    """
    converts a session object to an rdflib Graph
    """
    dumper = RDFDumper()
    g = dumper.as_rdf_graph(element=session, contexts=get_context())
    return g

def from_yaml(filename: str) -> Session:
    """
    This parses a slight variant of the standard serialization of the model into YAML

    See de-novo.yaml as an example

    In particular, until linkml supports a polymorphic discriminator we need ad-hoc
    code for instantiating to the correct class
    """
    logging.info(f'Converting {filename}')
    session = Session()
    loader = YAMLLoader()
    with open(filename, 'r') as stream:
        obj = yaml.load(stream)
        for a in obj['activity_set']:
            activity = loader.load(source=a, target_class=Activity)
            session.activity_set.append(activity)
        for c in obj['change_set']:
            # auto-create an ID
            c['id'] = f'uuid:{uuid1()}'
            tc = c['type']
            del c['type']
            print(f'Converting type {tc} // {c}')
            chg = loader.load(source=c, target_class=getattr(model.kgcl, tc))
            chg.type = f'kgcl:{tc}'
            session.change_set.append(chg)
    return session

@click.command()
@click.argument('files', nargs=-1)
def cli(files: List[str]):
    for f in files:
        session = from_yaml(f)

if __name__ == "__main__":
    cli()


