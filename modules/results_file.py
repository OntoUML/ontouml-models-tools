""" Results CSV Output File """
import csv

from modules.logger_config import initialize_logger

CSV_FILE = "results.csv"


def create_output_file():
    """ Create an CSV file containing only a header.
        Header is: dataset, instance, type, problem

        Created once in the execution of the software.
        If file already exists from previous execution, it is overwritten.
    """

    logger = initialize_logger()

    csv_header = ["dataset", "instance", "type", "problem"]

    try:
        with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)
        logger.debug("CSV output file successfully created.")
    except OSError as error:
        logger.error(f"Could not save {CSV_FILE} file. Exiting program."
                     f"System error reported: {error}")
        exit(1)


def append_problems_output_file(dataset_name, problems_list):
    """ Receives dataset and problems information and saves in CSV output file.  """

    logger = initialize_logger()

    try:
        with open(CSV_FILE, 'a', encoding='utf-8', newline='') as f:
            for problem in problems_list:
                writer = csv.writer(f)
                csv_row = [dataset_name, problem.instance, problem.type, problem.description]
                writer.writerow(csv_row)
        logger.debug(f"CSV output file successfully updated for dataset {dataset_name} "
                     f"with {len(problems_list)} entries.")

    except OSError as error:
        logger.error(f"Could not save {CSV_FILE} csv file. Exiting program."
                     f"System error reported: {error}")
        exit(1)
