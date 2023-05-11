""" Main module for the data quality functionality. """

from modules.logger_config import initialize_logger
from modules.tools.data_quality.catalog_verifications import verify_unwanted_characters, verify_association_ends, \
    verify_generalizations_properties, verify_old_stereotypes
from modules.tools.data_quality.results_file import create_output_char_file, create_output_ster_file, \
    create_output_ends_file, create_output_gens_file, append_problems_output_char_file, \
    append_problems_output_ends_file, append_problems_output_generalizations_file, \
    append_problems_output_old_stereotypes_file
from modules.utils.utils_general import get_list_unhidden_directories
from modules.utils.utils_rdf import load_all_graph_safely

LOGGER = initialize_logger()


def run_data_quality_verifications(arguments: dict):
    """ Calls every data quality verification features for the catalog. """

    # Building directories structure
    datasets_list = get_list_unhidden_directories(arguments["catalog_path"] + "/models/")
    datasets_list.sort()
    datasets_list_length = len(datasets_list)

    for dataset_number, dataset_name in enumerate(datasets_list):

        LOGGER.info(f"Evaluating dataset {dataset_number + 1}/{datasets_list_length}: {dataset_name}")

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
            LOGGER.warning(f"Dataset {dataset_name} has {len(problems_char_list)} problem_char case(s).")
        if problems_ends_list:
            append_problems_output_ends_file(dataset_name, problems_ends_list)
            LOGGER.warning(f"Dataset {dataset_name} has {len(problems_ends_list)} problem_ends case(s).")
        if problems_gens_list:
            append_problems_output_generalizations_file(dataset_name, problems_gens_list)
            LOGGER.warning(f"Dataset {dataset_name} has {len(problems_gens_list)} problem_generalization case(s).")
        if problems_ster_list:
            append_problems_output_old_stereotypes_file(dataset_name, problems_ster_list)
            LOGGER.warning(f"Dataset {dataset_name} has {len(problems_ster_list)} problem_old_stereotypes case(s).")

    LOGGER.info(f"Evaluation of problems concluded for all {datasets_list_length} datasets. "
                f"The evaluation results are available in the csv files.")
