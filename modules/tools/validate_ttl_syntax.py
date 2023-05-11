""" Main module for the verification of the ttl syntax for all files in the catalog. """
import subprocess

from modules.logger_config import initialize_logger
from modules.utils.utils_catalog import list_all_ttl_files

LOGGER = initialize_logger()


def validate_ttl_syntax(catalog_path: str):
    """ Uses external ttl software to validate the syntax of all ttl files in the catalog. """

    list_ttl_files = list_all_ttl_files(catalog_path)
    len_list_ttl_files = len(list_ttl_files)
    LOGGER.info(f"Starting ttl syntax validation of {len_list_ttl_files} files in {catalog_path[2:]}.")

    problems_list = []

    for count, ttl_file in enumerate(list_ttl_files):

        file_name = ttl_file.split("\\ontouml-models\\", 1)[1]
        ttl_output = subprocess.run(f"ttl {catalog_path[2:]}\\{file_name}", shell=True, capture_output=True)

        result = str(ttl_output.stdout)
        result = result[2:-3].replace("\\n", " ")

        if "Validator finished with 0 warnings and 0 errors" in result:
            LOGGER.info(f"File {count + 1}/{len_list_ttl_files}: {file_name} is valid.")
        else:
            LOGGER.warning(f"File {count + 1}/{len_list_ttl_files}: {file_name} has invalid syntax. {result}")
            problems_list.append(file_name)

    if problems_list:
        LOGGER.warning(f"VALIDATION FINISHED. The verification found {len(problems_list)} problem(s): {problems_list}")
    else:
        LOGGER.info(f"VALIDATION FINISHED. No problems found in the verification of {len_list_ttl_files} files.")
