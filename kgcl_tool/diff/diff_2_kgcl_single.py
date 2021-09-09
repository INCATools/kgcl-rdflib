import rdflib
from rdflib.namespace import (
    RDFS,
    RDF,
    OWL,
)
from rdflib import BNode, URIRef, Literal
from model.kgcl import (
    NodeRename,
    NodeMove,
    NodeDeepening,
    NodeShallowing,
    EdgeCreation,
    EdgeDeletion,
    PredicateChange,
    NodeCreation,
    ClassCreation,
    PlaceUnder,
    RemoveUnder,
    NewSynonym,
    RemovedNodeFromSubset,
)

from diff.change_detection import (
    detect_renamings,
    detect_node_moves,
    detect_predicate_changes,
)

from diff.render_operations import render


def id_generator():
    id = 0
    while True:
        yield id
        id += 1


id_gen = id_generator()

# TODO refactor deletions/additions to files


class SingleTripleChangeSummary:
    def __init__(self):
        self.edge_creations = []
        self.edge_deletions = []
        self.renamings = []
        self.class_creations = []
        self.subsumption_creations = []
        self.subsumption_deletions = []

    def get_commands(self):
        kgcl_commands = []
        for k in self.edge_creations:
            kgcl_commands.append(k)
        for k in self.edge_deletions:
            kgcl_commands.append(k)
        for k in self.renamings:
            kgcl_commands.append(k)
        for k in self.class_creations:
            kgcl_commands.append(k)
        for k in self.subsumption_creations:
            kgcl_commands.append(k)
        for k in self.subsumption_deletions:
            kgcl_commands.append(k)

        return kgcl_commands

    def add_edge_creations(self, ls):
        for i in ls:
            self.edge_creations.append(i)

    def add_edge_deletions(self, ls):
        for i in ls:
            self.edge_deletions.append(i)

    def add_renamings(self, ls):
        for i in ls:
            self.renamings.append(i)

    def add_class_creations(self, ls):
        for i in ls:
            self.class_creations.append(i)

    def add_subsumption_creations(self, ls):
        for i in ls:
            self.subsumption_creations.append(i)

    def add_subsumption_deletions(self, ls):
        for i in ls:
            self.subsumption_deletions.append(i)

    def add_edge_creation(self, i):
        self.edge_creations.append(i)

    def add_edge_deletion(self, i):
        self.edge_deletions.append(i)

    def add_renaming(self, i):
        self.renamings.append(i)

    def add_class_creation(self, i):
        self.class_creations.append(i)

    def add_subsumption_creation(self, i):
        self.subsumption_creations.append(i)

    def add_subsumption_deletion(self, i):
        self.subsumption_deletions.append(i)


def generate_thin_triple_commands(added, deleted):

    # synonyms
    # synonym_additions, covered = generate_synonym_creations(added)
    # added = added - covered
    # TODO: extend data model for deleted synonyms
    # synonym_deletions, covered = generate_synonym_deletions(added)

    # deepen [TODO: need some kind of reasoning/querying for this]
    # shallow [TODO: need some kind of reasoning/querying for this]

    # move
    # node_moves, covered, nonDeterministic = detect_node_moves(added, deleted)
    # added = added - covered
    # deleted = deleted - covered

    # change relationship
    relationship_change, covered, nonDeterministic = detect_predicate_changes(
        added, deleted
    )
    added = added - covered
    deleted = deleted - covered

    # renamings
    renamings, covered, nonDeterministic = detect_renamings(added, deleted)
    added = added - covered
    deleted = deleted - covered

    # subsumptions
    subsumption_creations, covered = generate_subsumption_creations(added)
    added = added - covered
    subsumption_deletions, covered = generate_subsumption_deletions(deleted)
    deleted = deleted - covered

    # create node
    node_creations, covered = generate_class_creations(added)
    added = added - covered

    # everything else
    edge_creations, covered = generate_edge_creations(added)
    edge_deletions, covered = generate_edge_deletions(deleted)

    summary = SingleTripleChangeSummary()
    for c in node_creations:
        summary.add_class_creation(render(c))
    # for m in node_moves:
    #     kgcl_commands.append(render(m))
    for r in relationship_change:
        summary.add_subsumption_creation(render(r))
    for s in subsumption_creations:
        summary.add_subsumption_creation(render(s))
    for s in subsumption_deletions:
        summary.add_subsumption_deletion(render(s))
    for r in renamings:
        summary.add_renaming(render(r))
    for e in edge_creations:
        summary.add_edge_creation(render(e))
    for e in edge_deletions:
        summary.add_edge_deletion(render(e))

    return summary


def get_type(rdf_entity):
    if isinstance(rdf_entity, URIRef):
        return "IRI"
    elif isinstance(rdf_entity, Literal):
        return "Literal"
    else:
        return "Error"


def get_language_tag(rdf_entity):
    if isinstance(rdf_entity, Literal):
        return rdf_entity.language
    else:
        return None


def get_datatype(rdf_entity):
    if isinstance(rdf_entity, Literal) and rdf_entity.datatype is not None:
        return str(rdf_entity.datatype)
    else:
        return None


# TODO: identify node creations + labels
def generate_class_creations(added):
    covered = rdflib.Graph()
    kgcl = []

    for s, p, o in added.triples((None, RDF.type, OWL.Class)):
        id = "test_id_" + str(next(id_gen))
        covered.add((s, p, o))
        node = ClassCreation(id=id, about_node=str(s), node_id=str(s))
        kgcl.append(node)

    return kgcl, covered


def generate_synonym_creations(added):
    covered = rdflib.Graph()
    kgcl = []

    # synonym = URIRef("http://www.geneontology.org/formats/oboInOwl#hasSynonym")
    exact_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasExactSynonym"
    )
    narrow_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym"
    )
    broad_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym"
    )
    related_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym"
    )

    # synonyms
    for s, p, o in added:
        id = "test_id_" + str(next(id_gen))
        covered.add((s, p, o))

        language = get_language_tag(o)
        # datatype = get_datatype(o)

        qualifier = ""  # case for hasSynonym
        if p == exact_synonym:
            qualifier = "exact"
        elif p == narrow_synonym:
            qualifier = "narrow"
        elif p == broad_synonym:
            qualifier = "broad"
        elif p == related_synonym:
            qualifier = "related"

        node = NewSynonym(
            id=id,
            about_node=str(s),
            new_value=str(o),
            qualifier=qualifier,
            language=language,
        )

        kgcl.append(node)

    return kgcl, covered


# TODO: extend data model for deleted synonyms
def generate_synonym_deletions(deleted):
    covered = rdflib.Graph()
    kgcl = []

    # synonym = URIRef("http://www.geneontology.org/formats/oboInOwl#hasSynonym")
    exact_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasExactSynonym"
    )
    narrow_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym"
    )
    broad_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym"
    )
    related_synonym = URIRef(
        "http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym"
    )

    # synonyms
    for s, p, o in deleted:
        id = "test_id_" + str(next(id_gen))
        covered.add((s, p, o))

        language = get_language_tag(o)
        # datatype = get_datatype(o)

        qualifier = ""  # case for hasSynonym
        if p == exact_synonym:
            qualifier = "exact"
        elif p == narrow_synonym:
            qualifier = "narrow"
        elif p == broad_synonym:
            qualifier = "broad"
        elif p == related_synonym:
            qualifier = "related"

        # TODO: extend data model for deleted synonyms
        node = NewSynonym(
            id=id,
            about_node=str(s),
            new_value=str(o),
            qualifier=qualifier,
            language=language,
        )

        kgcl.append(node)

    return kgcl, covered


def generate_subsumption_creations(added):
    covered = rdflib.Graph()
    kgcl = []

    for s, p, o in added.triples((None, RDFS.subClassOf, None)):
        id = "test_id_" + str(next(id_gen))
        subclass = str(s)
        superclass = str(o)

        # TODO the hardcoded owl:subClassOf should be part of the data model
        node = PlaceUnder(
            id=id,
            subject=subclass,
            predicate="<http://www.w3.org/2000/01/rdf-schema#subClassOf>",
            object=superclass,
        )

        kgcl.append(node)
        covered.add((s, p, o))

    return kgcl, covered


def generate_subsumption_deletions(deleted):
    covered = rdflib.Graph()
    kgcl = []

    for s, p, o in deleted.triples((None, RDFS.subClassOf, None)):
        id = "test_id_" + str(next(id_gen))
        subclass = str(s)
        superclass = str(o)

        # TODO the hardcoded owl:subClassOf should be part of the data model
        node = RemoveUnder(
            id=id,
            subject=subclass,
            predicate="<http://www.w3.org/2000/01/rdf-schema#subClassOf>",
            object=superclass,
        )

        kgcl.append(node)
        covered.add((s, p, o))

    return kgcl, covered


def generate_edge_creations(added):
    covered = rdflib.Graph()

    kgcl = []
    for s, p, o in added:

        id = "test_id_" + str(next(id_gen))
        object_type = get_type(o)
        language_tag = get_language_tag(o)
        datatype = get_datatype(o)
        if datatype is not None:
            datatype = "<" + datatype + ">"  # expect data types without curies

        node = EdgeCreation(
            id=id,
            subject=str(s),
            predicate=str(p),
            object=str(o),
            object_type=str(object_type),
            language=language_tag,
            datatype=datatype,
        )

        kgcl.append(node)
        covered.add((s, p, o))

    return kgcl, covered


def generate_edge_deletions(deleted):
    covered = rdflib.Graph()
    kgcl = []
    for s, p, o in deleted:

        id = "test_id_" + str(next(id_gen))
        object_type = get_type(o)
        language_tag = get_language_tag(o)
        datatype = get_datatype(o)
        if datatype is not None:
            datatype = "<" + datatype + ">"

        node = EdgeDeletion(
            id=id,
            subject=str(s),
            predicate=str(p),
            object=str(o),
            object_type=object_type,
            language=language_tag,
            datatype=datatype,
        )

        kgcl.append(node)
        covered.add((s, p, o))

    return kgcl, covered
