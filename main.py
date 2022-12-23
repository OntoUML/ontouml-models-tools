""" Main function for the ontouml-models-tools application. """
from modules.catalog_verifications import verify_unwanted_characters
from modules.initialization_arguments import treat_arguments
from modules.logger_config import initialize_logger
from modules.results_file import create_output_file, append_problems_output_file
from modules.utils_general import get_list_unhidden_directories
from modules.utils_rdf import load_all_graph_safely

SOFTWARE_ACRONYM = "OntoUML/UFO Catalog Tools"
SOFTWARE_NAME = "catalog_tools"
SOFTWARE_VERSION = "0.22.12.22"
SOFTWARE_URL = "https://github.com/unibz-core/ontouml-models-tools"


def run_catalog_tools():
    """ Calls each feature/tool for the catalog. """

    arguments = treat_arguments(SOFTWARE_ACRONYM, SOFTWARE_NAME, SOFTWARE_VERSION, SOFTWARE_URL)

    logger = initialize_logger()

    # Building directories structure
    datasets_list = get_list_unhidden_directories(arguments["catalog_path"])
    datasets_list.sort()
    datasets_list_length = len(datasets_list)

    for dataset_number, dataset_name in enumerate(datasets_list):

        logger.info(f"Evaluating dataset {dataset_number + 1}/{datasets_list_length}: {dataset_name}")

        if dataset_number == 0:
            create_output_file()

        problems_found_list = []
        dataset_location = arguments["catalog_path"] + "\\" + dataset_name
        dataset_ontology_location = dataset_location + "\\ontology.ttl"

        evaluated_ontology = load_all_graph_safely(dataset_ontology_location)

        problems_found_list = verify_unwanted_characters(evaluated_ontology)

        if problems_found_list:
            append_problems_output_file(dataset_name, problems_found_list)
            logger.warning(f"Dataset {dataset_name} has {len(problems_found_list)} problem(s).")

    logger.info(f"Evaluation of problems concluded for all {datasets_list_length} datasets. "
                f"The evaluation results are available in the results.csv file.")


if __name__ == "__main__":
    run_catalog_tools()
