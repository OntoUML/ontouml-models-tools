""" Functions to identify problems in generalization sets. """
from rdflib import Graph, RDF, URIRef

from modules.tools.data_quality.problem_classes import ProblemGeneralizations

NAMESPACE_ONTOUML = "https://w3id.org/ontouml#"


def get_gens_properties_in_names(graph: Graph) -> list[ProblemGeneralizations]:
    """ Identifies generalization sets that have metaproperties (e.g., disjoint or complete) in their names.

    :param graph: Dataset's ontology to be evaluated.
    :type graph: Graph
    :return: List of identified problems.
    :rtype: list[ProblemGeneralizations]
    """
    problems_list = []

    # Get all generalizations that have a name and that are not in generalization sets
    knows_query = """
            PREFIX ontouml: <https://w3id.org/ontouml#>
            SELECT DISTINCT ?gen_inst_name ?specific_name ?general_name
            WHERE {
                ?gen_inst rdf:type ontouml:Generalization .
                ?gen_inst ontouml:name ?gen_inst_name .
                ?gen_inst ontouml:general ?general .
                ?general ontouml:name ?general_name .
                ?gen_inst ontouml:specific ?specific .
                ?specific ontouml:name ?specific_name .
                FILTER NOT EXISTS {?gs_inst ontouml:generalization ?gen_inst}
            }"""

    query_answer = graph.query(knows_query)

    substring_list = ["{", "}", "over", "disj", "joint", "compl", "cover"]

    for result in query_answer:
        if any(map(result.gen_inst_name.__contains__, substring_list)):
            problems_list.append(
                ProblemGeneralizations(result.gen_inst_name.value, result.specific_name.value,
                                       result.general_name.value, "metaproperty in generalization name"))

    return problems_list


def get_gens_without_properties(graph: Graph) -> list[ProblemGeneralizations]:
    """ Identify generalization sets without metaproperties (i.e., not disjoint and not complete).

    :param graph: Dataset's ontology to be evaluated.
    :type graph: Graph
    :return: List of identified problems.
    :rtype: list[ProblemGeneralizations]
    """

    problems_list = []

    knows_query = """
            PREFIX ontouml: <https://w3id.org/ontouml#>
            SELECT DISTINCT ?genset_name ?complete ?disjoint
            WHERE {
                ?genset_inst rdf:type ontouml:GeneralizationSet .
                ?genset_inst ontouml:name ?genset_name .
                ?genset_inst ontouml:isComplete ?complete .
                ?genset_inst ontouml:isDisjoint ?disjoint .
            }"""

    query_answer = graph.query(knows_query)

    for result in query_answer:
        if not result.complete.toPython() and not result.complete.toPython():
            problems_list.append(ProblemGeneralizations(result.genset_name.toPython(), "", "",
                                                        "complete and disjoint are false"))

    return problems_list


def get_insuficient_gens(graph: Graph) -> list[ProblemGeneralizations]:
    """ Identify generalization sets with zero or one specialization.

    :param graph: Dataset's ontology to be evaluated.
    :type graph: Graph
    :return: List of identified problems.
    :rtype: list[ProblemGeneralizations]
    """

    problems_list = []

    graph.bind("ontouml", NAMESPACE_ONTOUML)

    for genset in graph.subjects(RDF.type, URIRef(NAMESPACE_ONTOUML + "GeneralizationSet")):

        num_generalizations = 0

        for gen in graph.objects(genset, URIRef(NAMESPACE_ONTOUML + "generalization")):
            num_generalizations += 1

        if num_generalizations <= 1:
            genset_name = graph.value(subject=genset, predicate=URIRef(NAMESPACE_ONTOUML + "name"))
            problems_list.append(
                ProblemGeneralizations(genset_name.toPython(), f"has only {num_generalizations} generalizations", "",
                                       "generalization set with less than two generalizations"))

    return problems_list
