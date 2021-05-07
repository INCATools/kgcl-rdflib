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
from linkml.loaders.yaml_loader import load
import linkml.dumpers.json_dumper as json_dumper
from linkml.dumpers.rdf_dumper import as_rdf_graph


THIS_DIR = os.path.abspath(os.path.dirname(__file__))
LD = os.path.join(THIS_DIR, '../ldcontext/kgcl.context.jsonld')

def to_json(session: Session) -> Graph:
    json = json_dumper.dumps(session)
    return json

def to_rdf(session: Session) -> Graph:
    g = as_rdf_graph(session, LD)
    return g

def from_yaml(filename: str) -> Session:
    logging.info(f'Converting {filename}')
    session = Session()
    with open(filename, 'r') as stream:
        obj = yaml.load(stream)
        for a in obj['activity_set']:
            activity = load(a, None, Activity, None)
            session.activity_set.append(activity)
        for c in obj['change_set']:
            c['id'] = f'{uuid1()}'
            tc = c['type']
            del c['type']
            print(f'Converting type {tc} // {c}')
            chg = load(c, None, getattr(model.kgcl, tc), None)
            session.change_set.append(chg)
    return session

@click.command()
@click.argument('files', nargs=-1)
def cli(files: List[str]):
    for f in files:
        session = from_yaml(f)

if __name__ == "__main__":
    cli()


