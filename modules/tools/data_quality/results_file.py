""" Results CSV Output File """
import csv
import inspect
import os

from modules.logger_config import initialize_logger
from modules.tools.data_quality.catalog_verifications import DataQualityProblemClass
from modules.utils.error_treatment import report_error_io_write, report_error_end_of_switch

LOGGER = initialize_logger()


def create_directory_if_not_exists(directory_path: str) -> None:
    """ Checks if the directory that has the path received as argument exists.
    If it does, do nothing. If it does not, create it.

    :param directory_path: Path to the directory to be created (if it does not exist).
    :type directory_path: str
    """

    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            LOGGER.debug(f"CSV output file {directory_path} successfully created.")
    except OSError as error:
        file_description = f"directory"
        report_error_io_write(directory_path, file_description, error)


def get_csv_header(feature_code: str) -> list[str]:
    """ Returns the argument feature's corresponding CSV header to be used in the CSV output file.

    :param feature_code: Data quality specific feature that is processed.
    :type feature_code: list[str]
    """

    csv_header = []

    if feature_code == "char":
        csv_header = ["dataset", "instance", "type", "problem"]
    elif feature_code == "ends":
        csv_header = ["dataset", "related_class", "relation_name", "end_value", "problem"]
    elif feature_code == "gens":
        csv_header = ["dataset", "generalization_name", "specific_name", "general_name", "problem"]
    elif feature_code == "ster":
        csv_header = ["dataset", "class_name", "old_stereotype", "new_stereotype"]
    else:
        current_function = inspect.stack()[0][3]
        report_error_end_of_switch("feature_code", current_function)

    return csv_header


def get_feature_problem_content(dataset_name: str, feature_code: str, problem: DataQualityProblemClass) -> list:
    """ Returns the argument feature's corresponding CSV content to be used in the CSV output file.

    :param dataset_name: Dataset that is going to have its problem reported.
    :type dataset_name: str
    :param feature_code: Data quality specific feature that is processed.
    :type feature_code: str
    :param problem: Specific problem for the dataset.
    :type problem: DataQualityProblemClass
    :return: List with specific problems to be printed in the csv file.
    :rtype: list
    """

    if feature_code == "char":
        csv_row = [dataset_name, problem.instance, problem.type, problem.description]
    elif feature_code == "ends":
        csv_row = [dataset_name, problem.related_class, problem.relation_name, problem.end_name,
                   problem.description]
    elif feature_code == "gens":
        csv_row = [dataset_name, problem.generalization_name, problem.specific_name, problem.general_name,
                   problem.description]
    elif feature_code == "ster":
        csv_row = [dataset_name, problem.class_name, problem.old_stereotype, problem.new_stereotype]
    else:
        current_function = inspect.stack()[0][3]
        report_error_end_of_switch("feature_code", current_function)

    return csv_row


def create_output_csv_file(feature_code: str):
    """ Create an CSV file containing only a header according to the feature_code received as argument.
    Created once in the execution of the software. If file already exists from previous execution, it is overwritten.

    :param feature_code: Code for the feature that is going to have its result csv file created.
    :type feature_code: str
    """

    csv_file_path = "results/results_" + feature_code + ".csv"
    csv_file_header = get_csv_header(feature_code)

    try:
        with open(csv_file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_file_header)
        LOGGER.debug(f"CSV output file {csv_file_path} successfully created.")
    except OSError as error:
        report_error_io_write(csv_file_path, f"csv output file for {feature_code} feature", error)


def append_problems_output_csv_file(dataset_name: str, feature_code: str, problems_list: list[DataQualityProblemClass]):
    """ Saves all problems identified for the selected feature in the corresponding CSV output file. """

    csv_file_path = "results/results_" + feature_code + ".csv"

    try:
        with open(csv_file_path, 'a', encoding='utf-8', newline='') as f:
            for problem in problems_list:
                writer = csv.writer(f)
                csv_row = get_feature_problem_content(dataset_name, feature_code, problem)
                writer.writerow(csv_row)
        LOGGER.debug(f"CSV output file successfully updated for dataset {dataset_name} "
                     f"with {len(problems_list)} entries.")
    except OSError as error:
        report_error_io_write(csv_file_path, f"csv output content for {feature_code} feature", error)
