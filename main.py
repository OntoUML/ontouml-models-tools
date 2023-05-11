""" Main function for the ontouml-models-tools application. """

from modules.data_quality.data_quality import run_data_quality_verifications
from modules.release_file import generate_release_file
from modules.validate_ttl_syntax import validate_ttl_syntax

from modules.initialization_arguments import treat_arguments
from modules.logger_config import initialize_logger

SOFTWARE_ACRONYM = "OntoUML/UFO Catalog Tools"
SOFTWARE_NAME = "ontouml-models-tools"
SOFTWARE_VERSION = "0.23.05.11"
SOFTWARE_URL = "https://github.com/OntoUML/ontouml-models-tools"

if __name__ == "__main__":

    arguments = treat_arguments(SOFTWARE_ACRONYM, SOFTWARE_NAME, SOFTWARE_VERSION, SOFTWARE_URL)
    logger = initialize_logger()

    if arguments["verify_data_quality"]:
        run_data_quality_verifications(arguments)
    elif arguments["generate_release"]:
        generate_release_file(arguments["catalog_path"])
    elif arguments["validate_ttl"]:
        validate_ttl_syntax(arguments["catalog_path"])
    else:
        logger.error("No feature selected. Please provide at least one valid argument. Use argument '-h' for help.")
        exit(1)
