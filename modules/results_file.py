""" Results CSV Output File """
import csv

from modules.logger_config import initialize_logger

CSV_CHAR_FILE = "results_char.csv"
CSV_ENDS_FILE = "results_ends.csv"
CSV_GENS_FILE = "results_gens.csv"


def create_output_char_file():
    """ Create an CSV file containing only a header.
        Header is: dataset, instance, type, problem

        Created once in the execution of the software.
        If file already exists from previous execution, it is overwritten.
    """

    logger = initialize_logger()

    csv_header = ["dataset", "instance", "type", "problem"]

    try:
        with open(CSV_CHAR_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)
        logger.debug(f"CSV output file {CSV_CHAR_FILE} successfully created.")
    except OSError as error:
        logger.error(f"Could not save {CSV_CHAR_FILE} file. Exiting program."
                     f"System error reported: {error}")
        exit(1)


def create_output_ends_file():
    """ Create an CSV file containing only a header.
        Header is: dataset, related_class, end_value, problem

        Created once in the execution of the software.
        If file already exists from previous execution, it is overwritten.
    """

    logger = initialize_logger()

    csv_header = ["dataset", "related_class", "relation_name", "end_value", "problem"]

    try:
        with open(CSV_ENDS_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)
        logger.debug(f"CSV output file {CSV_ENDS_FILE} successfully created.")
    except OSError as error:
        logger.error(f"Could not save {CSV_ENDS_FILE} file. Exiting program."
                     f"System error reported: {error}")
        exit(1)


def create_output_gens_file():
    """ Create an CSV file containing only a header.
        Header is: dataset, generalization_name, specific_name, general_name, problem

        Created once in the execution of the software.
        If file already exists from previous execution, it is overwritten.
    """

    logger = initialize_logger()

    csv_header = ["dataset", "generalization_name", "specific_name", "general_name", "problem"]

    try:
        with open(CSV_GENS_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)
        logger.debug(f"CSV output file {CSV_GENS_FILE} successfully created.")
    except OSError as error:
        logger.error(f"Could not save {CSV_GENS_FILE} file. Exiting program."
                     f"System error reported: {error}")
        exit(1)


def append_problems_output_char_file(dataset_name, problems_list):
    """ Receives dataset and character problems information and saves in CSV output file.  """

    logger = initialize_logger()

    try:
        with open(CSV_CHAR_FILE, 'a', encoding='utf-8', newline='') as f:
            for problem in problems_list:
                writer = csv.writer(f)
                csv_row = [dataset_name, problem.instance, problem.type, problem.description]
                writer.writerow(csv_row)
        logger.debug(f"CSV output file successfully updated for dataset {dataset_name} "
                     f"with {len(problems_list)} entries.")

    except OSError as error:
        logger.error(f"Could not save {CSV_CHAR_FILE} csv file. Exiting program."
                     f"System error reported: {error}")
        exit(1)


def append_problems_output_ends_file(dataset_name, problems_list):
    """ Receives dataset and association ends problems information and saves in CSV output file.  """

    logger = initialize_logger()

    try:
        with open(CSV_ENDS_FILE, 'a', encoding='utf-8', newline='') as f:
            for problem in problems_list:
                writer = csv.writer(f)
                csv_row = [dataset_name, problem.related_class, problem.relation_name, problem.end_name,
                           problem.description]
                writer.writerow(csv_row)
        logger.debug(f"CSV output file successfully updated for dataset {dataset_name} "
                     f"with {len(problems_list)} entries.")

    except OSError as error:
        logger.error(f"Could not save {CSV_ENDS_FILE} csv file. Exiting program."
                     f"System error reported: {error}")
        exit(1)


def append_problems_output_generalizations_file(dataset_name, problems_list):
    """ Receives dataset and generalizations problems information and saves in CSV output file.  """

    logger = initialize_logger()

    try:
        with open(CSV_GENS_FILE, 'a', encoding='utf-8', newline='') as f:
            for problem in problems_list:
                writer = csv.writer(f)
                csv_row = [dataset_name, problem.generalization_name, problem.specific_name, problem.general_name,
                           problem.description]
                writer.writerow(csv_row)
        logger.debug(f"CSV output file successfully updated for dataset {dataset_name} "
                     f"with {len(problems_list)} entries.")

    except OSError as error:
        logger.error(f"Could not save {CSV_GENS_FILE} csv file. Exiting program."
                     f"System error reported: {error}")
        exit(1)
