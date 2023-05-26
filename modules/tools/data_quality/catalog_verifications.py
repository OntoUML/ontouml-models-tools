""" Verifications over the catalog.ttl file. """
from rdflib import RDF, URIRef, Graph

from modules.utils.utils_general import contains_number

NAMESPACE_ONTOUML = "https://w3id.org/ontouml#"


class ProblemChar(object):
    """ Class that contains information about problems found in evaluations for characters. """

    def __init__(self, instance_name, type_name, description):
        self.instance = instance_name
        self.type = type_name
        self.description = description


class ProblemEnds(object):
    """ Class that contains information about problems found in evaluations for association ends. """

    def __init__(self, related_class, relation_name, end_name, description):
        self.related_class = related_class
        self.relation_name = relation_name
        self.end_name = end_name
        self.description = description


class ProblemGeneralizations(object):
    """ Class that contains information about problems found in generalizations. """

    def __init__(self, generalization_name, specific_name, general_name, description):
        self.generalization_name = generalization_name
        self.specific_name = specific_name
        self.general_name = general_name
        self.description = description


class ProblemOldStereotypes(object):
    """ Class that contains information about problems found in generalizations. """

    def __init__(self, class_name, old_stereotype, new_stereotype):
        self.class_name = class_name
        self.old_stereotype = old_stereotype
        self.new_stereotype = new_stereotype


def verify_unwanted_characters(graph: Graph) -> list[ProblemChar]:
    """ For the entity types in the list, verify if their instances have unwanted characters.

    :param graph: Loaded ontology graph.
    :type graph: Graph
    :return: List containing all identified problems.
    :rtype: list[ProblemChar]
    """

    problems_list_char = []

    entity_name = URIRef(NAMESPACE_ONTOUML + "name")

    for subj, pred, obj in graph.triples((None, RDF.type, None)):
        for name in graph.objects(subj, entity_name):
            name_before = name.value
            type_clean = (obj.toPython()).replace(NAMESPACE_ONTOUML, "")

            if "\n" in name_before:
                name_before = name_before.replace("\n", "")
                problems_list_char.append(ProblemChar(name_before, type_clean, "has line break"))

            try:
                name_before.encode("utf-8", errors='strict')
            except:
                name_before = name_before.encode("utf-8", errors='ignore')
                problems_list_char.append(ProblemChar(name_before, type_clean, "non utf-8 characters"))

            if name_before.startswith(" "):
                problems_list_char.append(ProblemChar(name_before, type_clean, "starts with space"))

            if name_before.endswith(" "):
                problems_list_char.append(ProblemChar(name_before, type_clean, "ends with space"))

            if "  " in name_before:
                problems_list_char.append(ProblemChar(name_before, type_clean, "has double space"))

            if "\t" in name_before:
                problems_list_char.append(ProblemChar(name_before, type_clean, "has indentation"))

            if ("<<" in name_before) or (">>" in name_before):
                problems_list_char.append(ProblemChar(name_before, type_clean, "stereotype in name"))

            if name_before.startswith("/"):
                problems_list_char.append(ProblemChar(name_before, type_clean, "derivation in name"))

            if "::" in name_before:
                problems_list_char.append(ProblemChar(name_before, type_clean, "imported class in name"))

    return problems_list_char


def verify_association_ends(graph: Graph) -> list[ProblemEnds]:
    """ Perform verifications in association ends.

    :param graph: Loaded ontology graph.
    :type graph: Graph
    :return: List containing all identified problems.
    :rtype: list[ProblemEnds]
    """

    problems_list_ends = []

    knows_query = """
    PREFIX ontouml: <https://w3id.org/ontouml#>
    SELECT DISTINCT ?class_name ?relation_name ?prop_value
    WHERE {
        ?prop_inst ontouml:propertyType ?class .
        ?prop_inst ontouml:name ?prop_value .
        ?class ontouml:name ?class_name .
        ?relation ontouml:relationEnd ?prop_inst .
        ?relation ontouml:name ?relation_name .
    }"""

    qres = graph.query(knows_query)

    for row in qres:
        # Get association ends with numbers or asterisks
        if (contains_number(row.prop_value.value)) or ("*" in row.prop_value.value):
            # The replace function is necessary to generate a correct csv removing cases of line breaks in names
            problems_list_ends.append(
                ProblemEnds(row.class_name.replace("\n", ""), row.relation_name.replace("\n", ""),
                            row.prop_value.value.replace("\n", ""),
                            "association end with possible multiplicity"))

    return problems_list_ends


def verify_generalizations_properties(graph: Graph) -> list[ProblemGeneralizations]:
    """ Identifies cases in which meta-properties are written as names in generalization sets.

    :param graph: Loaded ontology graph.
    :type graph: Graph
    :return: List containing all identified problems.
    :rtype: list[ProblemGeneralizations]
    """

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

    qres = graph.query(knows_query)

    substring_list = ["{", "}", "over", "disj", "joint", "compl", "cover"]

    problems_list_generalizations = []

    for gen in qres:
        if any(map(gen.gen_inst_name.__contains__, substring_list)):
            problems_list_generalizations.append(ProblemGeneralizations(gen.gen_inst_name.value,
                                                                        gen.specific_name.value,
                                                                        gen.general_name.value,
                                                                        "property in generalization name"))

    return problems_list_generalizations


def verify_old_stereotypes(graph: Graph) -> list[ProblemOldStereotypes]:
    """ Identifies cases in which the used stereotypes can be substituted by correct ones.
    According to: https://github.com/OntoUML/ontouml-models/wiki/Frequently-Asked-Questions
    #how-do-i-document-stereotypes-that-are-not-part-of-the-current-ontouml-profile

    :param graph: Loaded ontology graph.
    :type graph: Graph
    :return: List containing all identified problems.
    :rtype: list[ProblemOldStereotypes]
    """

    problems_list_old_stereotypes = []

    # Dictionary with stereotypes that can be substituted (all lowercase) and their substitution
    old_stereotypes_dict = {
        "powertype": "type",
        "highordertype": "type",
        "hou": "type",
        "universal": "type",
        "2ndot": "type",
        "relatorkind": "relator",
        "modekind": "mode",
        "quantitykind": "quantity",
        "collectivekind": "collective",
        "qualitykind": "quality"
    }

    knows_query = """
    PREFIX ontouml: <https://w3id.org/ontouml#>
    SELECT DISTINCT ?class_name ?stereotype
    WHERE {
        ?class rdf:type ontouml:Class .
        ?class ontouml:name ?class_name .
        ?class ontouml:stereotype ?stereotype
    }"""

    qres = graph.query(knows_query)

    for row in qres:
        # Remove line breaks in class names
        class_name = (row.class_name).replace("\n", "")

        # Remove prefix, set to lowercase, and clean hyphens and underscores in stereotypes
        no_prefix_stereotype_name = (row.stereotype).replace(NAMESPACE_ONTOUML, "")
        stereotype_name = no_prefix_stereotype_name.lower()
        stereotype_name = stereotype_name.replace("_", "")
        stereotype_name = stereotype_name.replace("-", "")

        # if in list, add to problems_list
        if stereotype_name in old_stereotypes_dict.keys():
            problems_list_old_stereotypes.append(ProblemOldStereotypes(class_name,
                                                                       no_prefix_stereotype_name,
                                                                       old_stereotypes_dict[stereotype_name]))

    return problems_list_old_stereotypes
