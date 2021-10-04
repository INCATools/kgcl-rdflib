import rdflib
from model.kgcl import (
    NodeRename,
    NodeObsoletion,
    NodeUnobsoletion,
    NodeDeletion,
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
    ExistentialRestrictionCreation,
    ExistentialRestrictionDeletion,
)
from diff.graph_diff import (
    get_added_existentials,
    get_deleted_existentials,
)
from diff.render_operations import render


def id_generator():
    id = 0
    while True:
        yield id
        id += 1


id_gen = id_generator()


class ExistentialChangeSummary:
    """
    Dataclass holding information about (atomic) existential restriction changes.
    """

    def __init__(self):

        self.existential_additions = []
        self.existential_deletions = []
        self.covered_triples_triple_existential_additions = []
        self.covered_triples_triple_existential_deletions = []

    def get_commands(self):
        kgcl_commands = []
        for k in self.existential_additions:
            kgcl_commands.append(k)
        for k in self.existential_deletions:
            kgcl_commands.append(k)
        return kgcl_commands

    def get_existential_additions(self):
        return self.existential_additions

    def get_existential_deletions(self):
        return self.existential_deletions

    def get_summary_KGCL_commands(self):
        out = (
            "ExistentialRestrictionCreations: "
            + str(len(self.existential_additions))
            + "\n"
            "ExistentialRestrictionDeletions: "
            + str(len(self.existential_deletions))
            + "\n"
        )
        return out

    def get_summary_RDF_triples(self):
        out = (
            "ExistentialRestrictionCreations"
            + str(len(self.covered_triples_triple_existential_additions))
            + "\n"
            "ExistentialRestrictionDeletions"
            + str(len(self.covered_triples_triple_existential_deletions))
            + "\n"
        )
        return out

    # RDF data

    def get_covered_triples_existential_additions(self):
        return self.covered_triples_triple_existential_additions

    def get_covered_triples_existential_deletions(self):
        return self.covered_triples_triple_existential_deletions

    def add_covered_triples_existential_additions(self, triples):
        for t in triples:
            self.covered_triples_triple_existential_additions.append(t)

    def add_covered_triples_existential_deletions(self, triples):
        for t in triples:
            self.covered_triples_triple_existential_deletions.append(t)

    # KGCL data

    def add_existential_addition(self, i):
        self.existential_additions.append(i)

    def add_existential_deletion(self, i):
        self.existential_deletions.append(i)


def generate_atomic_existential_commands(g1, g2):
    """
    Given two graphs g1 and g2,
    return all ExistentialRestrictionCreation and
    ExistentialRestrictionDeletion to account for their diff.
    """
    summary = ExistentialChangeSummary()

    added = get_added_existentials(g1, g2)
    deleted = get_deleted_existentials(g1, g2)

    existential_additions, covered = generate_existential_additions(added)
    summary.add_covered_triples_existential_additions(covered)

    existential_deletions, covered = generate_existential_deletions(deleted)
    summary.add_covered_triples_existential_deletions(covered)

    for a in existential_additions:
        summary.add_existential_addition(render(a))
    for d in existential_deletions:
        summary.add_existential_deletion(render(d))

    return summary


def generate_existential_deletions(deleted):
    """
    Return ExistentialRestrictionDeletion instances for given (deleted) triples.
    """
    covered = rdflib.Graph()
    kgcl = []

    for a in deleted:
        subclass = str(a.subclass)
        property = str(a.property)
        filler = str(a.filler)

        id = "test_id_" + str(next(id_gen))

        node = ExistentialRestrictionDeletion(
            id=id, subclass=subclass, property=property, filler=filler
        )

        kgcl.append(node)
        for t in a.triples:
            covered.add(t)

    return kgcl, covered


def generate_existential_additions(added):
    """
    Return ExistentialRestrictionCreation instances for given (added) triples.
    """
    covered = rdflib.Graph()
    kgcl = []

    for a in added:
        subclass = str(a.subclass)
        property = str(a.property)
        filler = str(a.filler)

        id = "test_id_" + str(next(id_gen))

        node = ExistentialRestrictionCreation(
            id=id, subclass=subclass, property=property, filler=filler
        )

        kgcl.append(node)
        for t in a.triples:
            covered.add(t)

    return kgcl, covered
