""" Main module for the catalog release file generation. """
from datetime import date

from rdflib import Graph

from modules.logger_config import initialize_logger
from modules.utils.utils_catalog import list_all_ttl_files
from modules.utils.utils_rdf import load_all_graph_safely, save_ontology_file_safely

LOGGER = initialize_logger()


def generate_release_file(catalog_path: str):
    """ Generates a single file with all content from all ttl files in the catalog to be used as a release version. """

    aggregated_graph = Graph()
    today = date.today().strftime("%Y%m%d")

    release_file_name = f"./ontouml-models-{today}.ttl"

    # Get all TTL files' complete paths
    LOGGER.info(f"Identifying all TTL files in directory {catalog_path} and in its subdirectories.")

    list_ttl_files = list_all_ttl_files(catalog_path)

    # Removing shapes files. Using [:] keeps the reference to the list
    # Reference: https://stackoverflow.com/questions/30764196/find-and-delete-list-elements-if-matching-a-string)
    list_ttl_files[:] = [i for i in list_ttl_files if "-shape.ttl" not in i]

    # Removing vocabulary.ttl
    list_ttl_files[:] = [i for i in list_ttl_files if "\\vocabulary.ttl" not in i]

    len_list_tt_files = len(list_ttl_files)

    # Load all TTL files in a single graph
    LOGGER.info(f"Generating single graph containing information from {len_list_tt_files} TTL files.")
    for count, ttl_file in enumerate(list_ttl_files):
        LOGGER.info(f"Including file {count + 1}/{len_list_tt_files}: {ttl_file}")
        item_graph = load_all_graph_safely(ttl_file)
        aggregated_graph += item_graph

    # Fixing prefixes
    aggregated_graph.bind("ontouml", "https://w3id.org/ontouml#")
    aggregated_graph.bind("dcat", "http://www.w3.org/ns/dcat#")
    aggregated_graph.bind("dct", "http://purl.org/dc/terms/")
    aggregated_graph.bind("ocmv", "https://w3id.org/ontouml-models/vocabulary#")
    aggregated_graph.bind("skos", "http://www.w3.org/2004/02/skos/core#")
    aggregated_graph.bind("mod", "https://w3id.org/mod#")
    aggregated_graph.bind("vcard", "http://www.w3.org/2006/vcard/ns#")
    aggregated_graph.bind("vann", "http://purl.org/vocab/vann/")

    # Saving graph as release file
    LOGGER.info(f"Saving a single file with graph's content.")
    save_ontology_file_safely(aggregated_graph, release_file_name)
    LOGGER.info(f"Release file successfully saved as {release_file_name}.")
