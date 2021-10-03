import click
import grammar.parser
import apply.graph_transformer
import rdflib

import sys

sys.path.append("../")
import python.kgcl


class Config(object):
    def __init__(self):
        self.verbose = False


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.command()
@click.argument("graph", type=click.Path(), required=True)
@click.argument("kgcl", type=click.File("r"), required=True)
@click.argument("output", type=click.Path(), required=True)
# @click.option("--verbose", "-v", is_flag=True, help="Print more output.")
@pass_config
def cli(config, graph, kgcl, output):

    # read kgcl commands from file
    kgcl_patch = kgcl.read()

    # parser kgcl commands
    parsed_patch = grammar.parser.parse(kgcl_patch)

    # apply kgcl commands as SPARQL UPDATE queries to graph
    g = rdflib.Graph()
    # TODO: change this to 'parse' in order to support all formats
    # g.load(graph, format="nt")
    g.parse(graph)  # , format="nt") #TODO: this doesn't always work
    apply.graph_transformer.apply_patch(parsed_patch, g)

    # save updated graph
    g.serialize(destination=output, format="nt")


if __name__ == "__main__":
    cli()
