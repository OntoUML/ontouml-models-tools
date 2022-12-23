""" Verifications over the catalog.ttl file. """
from rdflib import RDF, URIRef

from modules.utils_general import contains_number

NAMESPACE_ONTOUML = "https://purl.org/ontouml-models/vocabulary/"


class problem_char(object):
    """ Class that contains information about problems found in evaluations for characters. """

    def __init__(self, instance_name, type_name, description):
        self.instance = instance_name
        self.type = type_name
        self.description = description


class problem_ends(object):
    """ Class that contains information about problems found in evaluations for association ends. """

    def __init__(self, related_class, relation_name, end_name, description):
        self.related_class = related_class
        self.relation_name = relation_name
        self.end_name = end_name
        self.description = description


def verify_unwanted_characters(graph):
    """ For the entity types in the list, verify if their instances have unwanted characters. """

    problems_list_char = []

    entity_name = URIRef(NAMESPACE_ONTOUML + "name")

    for subj, pred, obj in graph.triples((None, RDF.type, None)):
        for name in graph.objects(subj, entity_name):
            name_before = name.value
            type_clean = obj.n3()[1:-1].replace(NAMESPACE_ONTOUML, "")

            if "\n" in name_before:
                name_before = name_before.replace("\n", "")
                problems_list_char.append(problem_char(name_before, type_clean, "has line break"))

            try:
                name_before.encode("utf-8", errors='strict')
            except:
                name_before = name_before.encode("utf-8", errors='ignore')
                problems_list_char.append(problem_char(name_before, type_clean, "non utf-8 characters"))

            if name_before.startswith(" "):
                problems_list_char.append(problem_char(name_before, type_clean, "starts with space"))

            if name_before.endswith(" "):
                problems_list_char.append(problem_char(name_before, type_clean, "ends with space"))

            if "  " in name_before:
                problems_list_char.append(problem_char(name_before, type_clean, "has double space"))

            if "\t" in name_before:
                problems_list_char.append(problem_char(name_before, type_clean, "has indentation"))

            if ("<<" in name_before) or (">>" in name_before):
                problems_list_char.append(problem_char(name_before, type_clean, "stereotype in name"))

            if name_before.startswith("/"):
                problems_list_char.append(problem_char(name_before, type_clean, "derivation in name"))

    return problems_list_char


def verify_association_ends(graph):
    """ Perform verifications in association ends. """

    problems_list_ends = []

    knows_query = """
    PREFIX ontouml: <https://purl.org/ontouml-models/vocabulary/>
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
        # Get association ends with numbers
        if contains_number(row.prop_value.value):
            problems_list_ends.append(problem_ends(row.class_name, row.relation_name, row.prop_value.value,
                                                   "association end with number"))

    return problems_list_ends

#         ?class rdf:type ontouml:Class .
#         ?class ontouml:name ?class_name .
#         ?relation rdf:type ontouml:Relation .
#         ?relation ontouml:relationEnd ?prop_inst .
#         ?relation ontouml:name ?relation_name .
#         ?prop_inst rdf:type ontouml:Property .
#         ?prop_inst ontouml:name ?prop_value .
#         ?prop_inst ontouml:propertyType ?class
