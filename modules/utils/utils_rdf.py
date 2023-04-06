""" Auxiliary functions for extending and complementing RDFLib's RDF treatment functions """
import copy
import os
import time

from owlrl import DeductiveClosure, RDFS_Semantics
from rdflib import RDF, OWL, Graph

from modules.logger_config import initialize_logger


def load_graph_safely_considering_restrictions(ontology_file, graph_restriction=None):
    """ Safely load graph from file to working memory.
        graph_restriction indicates items that must be kept when loading the ontology.
    """

    if graph_restriction == None:
        ontology_graph = load_all_graph_safely(ontology_file)
    else:
        ontology_graph = load_restrictions_only_graph_safely(ontology_file, graph_restriction)

    return ontology_graph


def load_all_graph_safely(ontology_location):
    """ Safely load graph from file to working memory. """

    logger = initialize_logger()

    ontology_graph = Graph()

    try:
        ontology_graph.parse(ontology_location, encoding='utf-8')
    except OSError as error:
        logger.error(f"Could not load {ontology_location}. Exiting program.\n"
                     f"System error reported: {error}")
        exit(1)

    logger.debug(f"Ontology {ontology_location} successfully loaded to working memory.")

    return ontology_graph


def reduce_graph_considering_restrictions(original_graph, restrictions_list):
    """ Reduce the already loaded ontology model to only allowed statements (contained in the restrictions_list). """

    # Copying original graph to a new graph
    working_graph = copy.deepcopy(original_graph)

    for subj, pred, obj in working_graph:
        if pred not in restrictions_list:
            working_graph.remove((subj, pred, obj))

    return working_graph


def load_restrictions_only_graph_safely(owl_file_path, restrictions_list):
    """ Extract the dataset model's taxonomy into a new graph. """

    working_graph = load_all_graph_safely(owl_file_path)

    for subj, pred, obj in working_graph:
        if pred not in restrictions_list:
            working_graph.remove((subj, pred, obj))

    return working_graph


def has_prefix(ontology_graph, prefix):
    """ Return boolean indicating if the argument prefix exists in the graph"""
    result = False

    for pre, nam in ontology_graph.namespaces():
        if prefix == pre:
            result = True

    return result


def has_namespace(ontology_graph, namespace):
    """ Return boolean indicating if the argument namespace exists in the graph.
        The argument namespace must be provided without the surrounding <>"""
    result = False

    for pre, nam in ontology_graph.namespaces():
        if namespace == nam.n3()[1:-1]:
            result = True

    return result


def list_prefixes(ontology_graph):
    """ Return a list of all prefixes in the graph"""
    result = []

    for pre, nam in ontology_graph.namespaces():
        result.append(pre)

    return result


def list_namespaces(ontology_graph):
    """ Return a list of all namespaces in the graph without the surrounding <>"""
    result = []

    for pre, nam in ontology_graph.namespaces():
        # N3 necessary for returning string and [1:-1] necessary for removing <>
        result.append(nam.n3()[1:-1])

    return result


def get_ontology_uri(ontology_graph):
    """ Return the URI of the ontology graph. """

    ontology_uri = ontology_graph.value(predicate=RDF.type, object=OWL.Ontology)

    return ontology_uri


def get_list_of_all_classes(ontology_graph, exceptions_list=None):
    """ Returns a list of all classes as URI strings without repetitions available in a Graph.
    Classes that have namespaces included in the exception_list parameter are not included in the returned list. """

    if exceptions_list == None:
        exceptions_list = []

    classes_list = []

    for sub, pred, obj in ontology_graph:
        if (sub, RDF.type, OWL.Class) in ontology_graph:
            # Eliminating BNodes
            if type(sub).__name__ != "BNode":
                # N3 necessary for returning string and [1:-1] necessary for removing <>
                classes_list.append(sub.n3()[1:-1])
        if (obj, RDF.type, OWL.Class) in ontology_graph:
            # Eliminating BNodes
            if type(obj).__name__ != "BNode":
                # N3 necessary for returning string and [1:-1] necessary for removing <>
                classes_list.append(obj.n3()[1:-1])

    # Removing repetitions
    no_rep_classes_list = [*set(classes_list)]

    # Removing classes that have namespace in the exceptions_list
    classes_list = no_rep_classes_list.copy()
    for class_uri in no_rep_classes_list:
        for exception_item in exceptions_list:
            if class_uri.startswith(exception_item):
                classes_list.remove(class_uri)
                break

    return classes_list


def perform_reasoning(ontology_graph):
    """Perform reasoner and consequently expands the ontology graph. """

    logger = initialize_logger()

    logger.info("Initializing RDFS reasoning. This may take a while...")

    st = time.perf_counter()
    DeductiveClosure(RDFS_Semantics).expand(ontology_graph)
    et = time.perf_counter()
    elapsed_time = round((et - st), 4)

    logger.info(f"Reasoning process completed in {elapsed_time} seconds.")


def save_ontology_file_safely(ontology_graph, output_file_path):
    """  Saves the ontology graph into a TTL file. """

    logger = initialize_logger()

    logger.debug("Saving the output ontology file...")

    try:
        ontology_graph.serialize(destination=output_file_path)
        logger.info(f"Output ontology file saved. Access it in {os.path.abspath(output_file_path)}.")
    except OSError as error:
        logger.error(f"Could not save the output ontology file ({output_file_path}). Exiting program."
                     f"System error reported: {error}")
        exit(1)
