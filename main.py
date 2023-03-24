""" Main function for the ontouml-models-tools application. """
import glob
from datetime import date

from rdflib import Graph

from modules.data_quality.catalog_verifications import verify_unwanted_characters, verify_association_ends, \
    verify_generalizations_properties, verify_old_stereotypes
from modules.data_quality.results_file import create_output_char_file, append_problems_output_char_file, \
    append_problems_output_ends_file, create_output_ends_file, append_problems_output_generalizations_file, \
    create_output_gens_file, append_problems_output_old_stereotypes_file, create_output_ster_file
from modules.initialization_arguments import treat_arguments
from modules.logger_config import initialize_logger
from modules.utils_general import get_list_unhidden_directories
from modules.utils_rdf import load_all_graph_safely, save_ontology_file_safely

SOFTWARE_ACRONYM = "OntoUML/UFO Catalog Tools"
SOFTWARE_NAME = "ontouml-models-tools"
SOFTWARE_VERSION = "0.23.03.23"
SOFTWARE_URL = "https://github.com/OntoUML/ontouml-models-tools"


def run_data_quality_verifications(arguments):
    """ Calls every data quality verification features for the catalog. """

    # Building directories structure
    datasets_list = get_list_unhidden_directories(arguments["catalog_path"] + "/models/")
    datasets_list.sort()
    datasets_list_length = len(datasets_list)

    for dataset_number, dataset_name in enumerate(datasets_list):

        logger.info(f"Evaluating dataset {dataset_number + 1}/{datasets_list_length}: {dataset_name}")

        if dataset_number == 0:
            create_output_char_file()
            create_output_ends_file()
            create_output_gens_file()
            create_output_ster_file()

        dataset_location = arguments["catalog_path"] + "models\\" + dataset_name
        dataset_ontology_location = dataset_location + "\\ontology.ttl"

        evaluated_ontology = load_all_graph_safely(dataset_ontology_location)

        problems_char_list = verify_unwanted_characters(evaluated_ontology)
        problems_ends_list = verify_association_ends(evaluated_ontology)
        problems_gens_list = verify_generalizations_properties(evaluated_ontology)
        problems_ster_list = verify_old_stereotypes(evaluated_ontology)

        if problems_char_list:
            append_problems_output_char_file(dataset_name, problems_char_list)
            logger.warning(f"Dataset {dataset_name} has {len(problems_char_list)} problem_char case(s).")
        if problems_ends_list:
            append_problems_output_ends_file(dataset_name, problems_ends_list)
            logger.warning(f"Dataset {dataset_name} has {len(problems_ends_list)} problem_ends case(s).")
        if problems_gens_list:
            append_problems_output_generalizations_file(dataset_name, problems_gens_list)
            logger.warning(f"Dataset {dataset_name} has {len(problems_gens_list)} problem_generalization case(s).")
        if problems_ster_list:
            append_problems_output_old_stereotypes_file(dataset_name, problems_ster_list)
            logger.warning(f"Dataset {dataset_name} has {len(problems_ster_list)} problem_old_stereotypes case(s).")

    logger.info(f"Evaluation of problems concluded for all {datasets_list_length} datasets. "
                f"The evaluation results are available in the csv files.")


def generate_release_file(catalog_path: str):
    """ Generates a single file with all content from all ttl files in the catalog to be used as a release version. """

    list_tt_files = []
    aggregated_graph = Graph()
    today = date.today()
    release_file_name = f"./ontouml-models-{today}.ttl"

    # Get all TTL files' complete paths
    logger.info(f"Identifying all TTL files in directory {catalog_path} and in its subdirectories.")
    for ttl_file in glob.glob(catalog_path + '**/*.ttl', recursive=True):
        if "\\shapes\\" not in ttl_file:
            list_tt_files.append(ttl_file)

    len_list_tt_files = len(list_tt_files)

    # Load all TTL files in a single graph
    logger.info("Generating single graph containing all TTL files' information.")
    for count, ttl_file in enumerate(list_tt_files):
        logger.info(f"Including file {count + 1}/{len_list_tt_files}: {ttl_file}")
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
    logger.info("Generating single graph containing all TTL files' information.")
    save_ontology_file_safely(aggregated_graph, release_file_name)
    logger.info(f"Release file successfully saved as {release_file_name}.")


if __name__ == "__main__":

    arguments = treat_arguments(SOFTWARE_ACRONYM, SOFTWARE_NAME, SOFTWARE_VERSION, SOFTWARE_URL)
    logger = initialize_logger()

    if arguments["verify_data_quality"]:
        run_data_quality_verifications(arguments)
    elif arguments["generate_release"]:
        generate_release_file(arguments["catalog_path"])
    else:
        logger.error("No feature selected. Please provide at least one valid argument. Enter '-h' for help.")
        exit(1)
