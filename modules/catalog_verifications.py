""" Verifications over the catalog.ttl file. """
from rdflib import RDF, URIRef

NAMESPACE_ONTOUML = "https://purl.org/ontouml-models/vocabulary/"


class problem(object):
    """ Class that contains information about problems found in evaluations. """

    def __init__(self, instance_name, type_name, description):
        self.instance = instance_name
        self.type = type_name
        self.description = description


def verify_unwanted_characters(graph):
    """ For the entity types in the list, verify if their instances have unwanted characters. """

    problems_list = []

    entity_name = URIRef(NAMESPACE_ONTOUML + "name")

    for subj, pred, obj in graph.triples((None, RDF.type, None)):
        for name in graph.objects(subj, entity_name):
            name_before = name.value
            type_clean = obj.n3()[1:-1].replace(NAMESPACE_ONTOUML, "")

            if "\n" in name_before:
                name_before = name_before.replace("\n", "")
                problems_list.append(problem(name_before, type_clean, "has line break"))

            try:
                name_before.encode("utf-8", errors='strict')
            except:
                name_before = name_before.encode("utf-8", errors='ignore')
                problems_list.append(problem(name_before, type_clean, "non utf-8 characters"))

            if name_before.startswith(" "):
                problems_list.append(problem(name_before, type_clean, "starts with space"))

            if name_before.endswith(" "):
                problems_list.append(problem(name_before, type_clean, "ends with space"))

            if "  " in name_before:
                problems_list.append(problem(name_before, type_clean, "has double space"))

            if "\t" in name_before:
                problems_list.append(problem(name_before, type_clean, "has indentation"))

            if ("<<" in name_before) or (">>" in name_before):
                problems_list.append(problem(name_before, type_clean, "stereotype in name"))

            if name_before.startswith("/"):
                problems_list.append(problem(name_before, type_clean, "derivation in name"))

    return problems_list
