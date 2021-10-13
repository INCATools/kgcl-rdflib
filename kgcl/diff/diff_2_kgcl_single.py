import rdflib
from rdflib.namespace import (
    RDFS,
    RDF,
    OWL,
)
from rdflib import URIRef, Literal
from kgcl.model.kgcl import (
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

from kgcl.diff.change_detection import (
    detect_renamings,
    detect_node_moves,
    detect_predicate_changes,
    detect_annotation_changes,
)

from kgcl.diff.render_operations import render

from kgcl.diff.graph_diff import (
    get_added_thin_triples,
    get_deleted_thin_triples,
)


def id_generator():
    id = 0
    while True:
        yield id
        id += 1


id_gen = id_generator()


class SingleTripleChangeSummary:
    """
    Dataclass holding information about (atomic) existential restriction changes.
    """

    def __init__(self):

        # KGCL data
        self.renamings = []
        self.class_creations = []
        self.subsumption_creations = []
        self.subsumption_deletions = []
        self.predicate_changes = []
        self.node_moves = []
        self.synonym_creations = []
        self.annotation_changes = []

        # RDF data
        self.covered_triples_renamings = []
        self.covered_triples_class_creations = []
        self.covered_triples_subsumption_creations = []
        self.covered_triples_subsumption_deletions = []
        self.covered_triples_predicate_changes = []
        self.covered_triples_node_moves = []
        self.covered_triples_synonym_creations = []
        self.covered_triples_edge_creations = []
        self.covered_triples_edge_deletions = []
        self.covered_triples_annotation_changes = []

        # non-deterministic data
        self.non_deterministic_node_moves = []
        self.non_deterministic_predicate_changes = []
        self.non_deterministic_renamings = []
        self.non_deterministic_annotation_changes = []

    def get_commands(self):
        kgcl_commands = []
        for k in self.synonym_creations:
            kgcl_commands.append(k)
        for k in self.node_moves:
            kgcl_commands.append(k)
        for k in self.predicate_changes:
            kgcl_commands.append(k)
        for k in self.renamings:
            kgcl_commands.append(k)
        for k in self.class_creations:
            kgcl_commands.append(k)
        for k in self.subsumption_creations:
            kgcl_commands.append(k)
        for k in self.subsumption_deletions:
            kgcl_commands.append(k)
        for k in self.annotation_changes:
            kgcl_commands.append(k)

        return kgcl_commands

    def get_renamings(self):
        return self.renamings

    def get_class_creations(self):
        return self.class_creations

    def get_subsumption_creations(self):
        return self.subsumption_creations

    def get_subsumption_deletions(self):
        return self.subsumption_deletions

    def get_predicate_changes(self):
        return self.predicate_changes

    def get_node_moves(self):
        return self.node_moves

    def get_synonym_creations(self):
        return self.synonym_creations

    def get_annotation_changes(self):
        return self.annotation_changes

    def get_summary_KGCL_commands(self):
        out = (
            "Renamings: "
            + str(len(self.renamings))
            + "\n"
            + "ClassCreations: "
            + str(len(self.class_creations))
            + "\n"
            # + "Subsumption Creations: "
            + "PlaceUnder: "
            + str(len(self.subsumption_creations))
            + "\n"
            # + "Subsumption Deletions: "
            + "RemoveUnder: "
            + str(len(self.subsumption_deletions))
            + "\n"
            + "PredicateChanges: "
            + str(len(self.predicate_changes))
            + "\n"
            + "NodeMoves: "
            + str(len(self.node_moves))
            + "\n"
            + "SynonymCreations: "
            + str(len(self.synonym_creations))
            + "\n"
            + "NodeAnnotationChanges: "
            + str(len(self.annotation_changes))
            + "\n"
        )
        return out

    def get_summary_RDF_triples(self):
        out = (
            "Renamings:"
            + str(len(self.covered_triples_renamings))
            + "\n"
            + "ClassCreations: "
            + str(len(self.covered_triples_class_creations))
            + "\n"
            # + "Subsumption Creations: "
            + "PlaceUnder: "
            + str(len(self.covered_triples_subsumption_creations))
            + "\n"
            # + "Subsumption Deletions: "
            + "RemoveUnder: "
            + str(len(self.covered_triples_subsumption_deletions))
            + "\n"
            + "PredicateChanges: "
            + str(len(self.covered_triples_predicate_changes))
            + "\n"
            + "NodeMoves: "
            + str(len(self.covered_triples_node_moves))
            + "\n"
            + "SynonymCreations: "
            + str(len(self.covered_triples_synonym_creations))
            + "\n"
            + "NodeAnnotationChanges: "
            + str(len(self.covered_triples_annotation_changes))
            + "\n"
        )
        return out

    # RDF data

    def get_covered_triples_renamings(self):
        return self.covered_triples_renamings

    def add_covered_triples_renamings(self, triples):
        for t in triples:
            self.covered_triples_renamings.append(t)

    def get_covered_triples_class_creations(self):
        return self.covered_triples_class_creations

    def add_covered_triples_class_creations(self, triples):
        for t in triples:
            self.covered_triples_class_creations.append(t)

    def get_covered_triples_subsumption_creations(self):
        return self.covered_triples_subsumption_creations

    def add_covered_triples_subsumption_creations(self, triples):
        for t in triples:
            self.covered_triples_subsumption_creations.append(t)

    def get_covered_triples_subsumption_deletions(self):
        return self.covered_triples_subsumption_deletions

    def add_covered_triples_subsumption_deletions(self, triples):
        for t in triples:
            self.covered_triples_subsumption_deletions.append(t)

    def get_covered_triples_predicate_changes(self):
        return self.covered_triples_predicate_changes

    def add_covered_triples_predicate_changes(self, triples):
        for t in triples:
            self.covered_triples_predicate_changes.append(t)

    def get_covered_triples_node_moves(self):
        return self.covered_triples_node_moves

    def add_covered_triples_node_moves(self, triples):
        for t in triples:
            self.covered_triples_node_moves.append(t)

    def get_covered_triples_synonym_creations(self):
        return self.covered_triples_synonym_creations

    def add_covered_triples_synonym_creations(self, triples):
        for t in triples:
            self.covered_triples_synonym_creations.append(t)

    def get_covered_triples_annotation_changes(self):
        return self.covered_triples_annotation_changes

    def add_covered_triples_annotation_changes(self, triples):
        for t in triples:
            self.covered_triples_annotation_changes.append(t)

    # KGCL data

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

    def add_predicate_change(self, i):
        self.predicate_changes.append(i)

    def add_node_move(self, i):
        self.node_moves.append(i)

    def add_synonym_creation(self, i):
        self.synonym_creations.append(i)

    def add_annotation_change(self, i):
        self.annotation_changes.append(i)

    # non-deterministic data
    def add_non_deterministic_node_moves(self, ls):
        self.non_deterministic_node_moves += ls

    def add_non_deterministic_predicate_changes(self, ls):
        self.non_deterministic_predicate_changes += ls

    def add_non_deterministic_renamings(self, ls):
        self.non_deterministic_renamings += ls

    def add_non_deterministic_annotation_changes(self, ls):
        self.non_deterministic_annotation_changes += ls

    def get_non_deterministic_node_moves(self):
        return self.non_deterministic_node_moves

    def get_non_deterministic_predicate_changes(self):
        return self.non_deterministic_predicate_changes

    def get_non_deterministic_renamings(self):
        return self.non_deterministic_renamings

    def get_non_deterministic_annotation_changes(self):
        return self.non_deterministic_annotation_changes


def generate_thin_triple_commands(g1, g2):
    """
    Given two graphs g1 and g2,
    return all KGCL data model instances to account for their diff.
    """
    # summary object for single triple changes
    summary = SingleTripleChangeSummary()

    added = get_added_thin_triples(g1, g2)
    deleted = get_deleted_thin_triples(g1, g2)

    # synonyms
    synonym_additions, covered = generate_synonym_creations(added)
    summary.add_covered_triples_synonym_creations(covered)
    added = added - covered
    # TODO: extend data model for deleted synonyms
    # synonym_deletions, covered = generate_synonym_deletions(added)

    # deepen [TODO: need some kind of reasoning/querying for this]
    # shallow [TODO: need some kind of reasoning/querying for this]

    # move
    node_moves, covered, non_deterministic = detect_node_moves(added, deleted)
    summary.add_covered_triples_node_moves(covered)
    summary.add_non_deterministic_node_moves(non_deterministic)
    added = added - covered
    deleted = deleted - covered

    # change relationship
    relationship_change, covered, non_deterministic = detect_predicate_changes(
        added, deleted
    )
    summary.add_covered_triples_predicate_changes(covered)
    summary.add_non_deterministic_predicate_changes(non_deterministic)
    added = added - covered
    deleted = deleted - covered

    # renamings
    renamings, covered, non_deterministic = detect_renamings(added, deleted)
    summary.add_covered_triples_renamings(covered)
    summary.add_non_deterministic_renamings(non_deterministic)
    added = added - covered
    deleted = deleted - covered

    # subsumptions
    subsumption_creations, covered = generate_subsumption_creations(added)
    summary.add_covered_triples_subsumption_creations(covered)
    added = added - covered

    subsumption_deletions, covered = generate_subsumption_deletions(deleted)
    summary.add_covered_triples_subsumption_deletions(covered)
    deleted = deleted - covered

    # create node
    node_creations, covered = generate_class_creations(added)
    summary.add_covered_triples_class_creations(covered)
    added = added - covered

    # create annotation changes
    old_annotation_properties = get_annotation_properties(g1)
    new_annotation_properties = get_annotation_properties(g2)
    annotation_changes, covered, non_deterministic = detect_annotation_changes(
        added, deleted, new_annotation_properties, old_annotation_properties
    )
    summary.add_covered_triples_annotation_changes(covered)
    summary.add_non_deterministic_annotation_changes(non_deterministic)
    added = added - covered
    deleted = deleted - covered

    for s in synonym_additions:
        summary.add_synonym_creation(render(s))
    for c in node_creations:
        summary.add_class_creation(render(c))
    for m in node_moves:
        summary.add_node_move(render(m))
    for r in relationship_change:
        summary.add_predicate_change(render(r))
    for s in subsumption_creations:
        summary.add_subsumption_creation(render(s))
    for s in subsumption_deletions:
        summary.add_subsumption_deletion(render(s))
    for r in renamings:
        summary.add_renaming(render(r))
    for c in annotation_changes:
        summary.add_annotation_change(render(c))

    return summary


def get_annotation_properties(graph):
    properties = set()
    for s, p, o in graph.triples((None, RDF.type, OWL.AnnotationProperty)):
        properties.add(s)
    return properties


def get_type(rdf_entity):
    if isinstance(rdf_entity, URIRef):
        return "uri"
    elif isinstance(rdf_entity, Literal):
        return "literal"
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

    synonym = URIRef("http://www.geneontology.org/formats/oboInOwl#hasSynonym")
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

    include = {synonym, exact_synonym, narrow_synonym, broad_synonym, related_synonym}

    # synonyms
    for s, p, o in added:
        if p in include:
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
