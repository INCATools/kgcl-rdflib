import yaml
import click
import logging
import os
import kgcl.model as model
from rdflib import Graph
from typing import List
from uuid import uuid1

from kgcl.model.kgcl import Change, Session
from kgcl.model.prov import Activity
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.dumpers.json_dumper import JSONDumper
from linkml_runtime.dumpers.rdf_dumper import RDFDumper


THIS_DIR = os.path.abspath(os.path.dirname(__file__))
LD = os.path.join(THIS_DIR, '../ldcontext/kgcl.context.jsonld')

def to_json(session: Session) -> Graph:
    dumper = JSONDumper()
    json = dumper.dumps(session)
    return json

def to_rdf(session: Session) -> Graph:
    dumper = RDFDumper()
    g = dumper.as_rdf_graph(session, LD)
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
            c['id'] = f'{uuid1()}'
            tc = c['type']
            del c['type']
            print(f'Converting type {tc} // {c}')
            chg = loader.load(source=c, target_class=getattr(model.kgcl, tc))
            session.change_set.append(chg)
    return session

@click.command()
@click.argument('files', nargs=-1)
def cli(files: List[str]):
    for f in files:
        session = from_yaml(f)

if __name__ == "__main__":
    cli()


