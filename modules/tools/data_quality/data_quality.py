""" Main module for the data quality functionality. """
import inspect

from rdflib import Graph

from modules.logger_config import initialize_logger
from modules.tools.data_quality.catalog_verifications import verify_unwanted_characters, verify_association_ends, \
    verify_generalizations_properties, verify_old_stereotypes, DataQualityProblemClass
from modules.tools.data_quality.results_file import create_directory_if_not_exists, create_output_csv_file, \
    append_problems_output_csv_file
from modules.utils.error_treatment import report_error_end_of_switch
from modules.utils.utils_general import get_list_unhidden_directories
from modules.utils.utils_rdf import load_all_graph_safely

LOGGER = initialize_logger()


def execute_feature_verification(feature_code: str, evaluated_ontology: Graph) -> list[DataQualityProblemClass]:
    """ Execute the feature verification for the evaluated_ontology according to the given feature_code.

    :param feature_code: Data quality sub-feature being performed.
    :type feature_code: str
    :param evaluated_ontology: Dataset's ontology that is being evaluated.
    :type evaluated_ontology: Graph
    :return: List of problems with the given feature_code type.
    :rtype: list[DataQualityProblemClass]
    """

    problems_list = []

    if feature_code == "char":
        problems_list = verify_unwanted_characters(evaluated_ontology)
    elif feature_code == "ends":
        problems_list = verify_association_ends(evaluated_ontology)
    elif feature_code == "gens":
        problems_list = verify_generalizations_properties(evaluated_ontology)
    elif feature_code == "ster":
        problems_list = verify_old_stereotypes(evaluated_ontology)
    else:
        current_function = inspect.stack()[0][3]
        report_error_end_of_switch("feature_code", current_function)

    return problems_list


def run_data_quality_verifications(catalog_path: str):
    """ Calls every data quality verification features for the catalog.

    :param catalog_path: Path to the ontouml-models catalog directory provided by the user as argument.
    :type catalog_path: str
    """

    # Available sub-features
    features_list = ["char", "ends", "gens", "ster"]

    # If directory 'results_directory' not exists, create it
    results_directory = "results"
    create_directory_if_not_exists(results_directory)

    # Building directories structure
    datasets_list = get_list_unhidden_directories(catalog_path + "/models/")
    datasets_list.sort()
    datasets_list_length = len(datasets_list)

    # Creating new csv file with header for each feature
    for feature_code in features_list:
        create_output_csv_file(feature_code)

    for dataset_number, dataset_name in enumerate(datasets_list):

        LOGGER.info(f"Evaluating dataset {dataset_number + 1}/{datasets_list_length}: {dataset_name}")

        dataset_location = catalog_path + "models\\" + dataset_name
        dataset_ontology_location = dataset_location + "\\ontology.ttl"
        evaluated_ontology = load_all_graph_safely(dataset_ontology_location)

        for feature_code in features_list:
            # Executing verifications
            problems_list = execute_feature_verification(feature_code, evaluated_ontology)
            # Registering problems
            append_problems_output_csv_file(dataset_name, feature_code, problems_list)
            # Printing message if any problem exists
            num_problem = len(problems_list)
            if num_problem > 0:
                LOGGER.warning(f"Dataset {dataset_name} has {num_problem} {feature_code.upper()} case(s).")

    LOGGER.info(f"Evaluation of problems concluded for all {datasets_list_length} datasets. "
                f"The evaluation results are available in the csv files.")
