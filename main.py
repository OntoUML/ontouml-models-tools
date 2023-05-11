""" Main function for the ontouml-models-tools application. """
import json
from base64 import encodebytes, encode

from modules.initialization_arguments import treat_arguments
from modules.logger_config import initialize_logger
from modules.tools.data_quality.data_quality import run_data_quality_verifications
from modules.tools.release_file import generate_release_file
from modules.tools.validate_ttl_syntax import validate_ttl_syntax
from modules.utils.utils_catalog import list_all_files_with_filetype
from pathlib import Path

SOFTWARE_ACRONYM = "OntoUML/UFO Catalog Tools"
SOFTWARE_NAME = "ontouml-models-tools"
SOFTWARE_VERSION = "0.23.05.11"
SOFTWARE_URL = "https://github.com/OntoUML/ontouml-models-tools"


def fix_json(catalog_path: str):
    """ Reads all ontology.json files and do minor fixes. """

    # Getting a list of all json files inside the catalog_path folder
    json_files = list_all_files_with_filetype(catalog_path, "json")

    for json_file in json_files:

        print(f"Working JSON: {json_file}")

        # returns JSON object as a dictionary
        try:

            # Opening specific JSON file
            with open(json_file, 'r', encoding='utf-8', newline='') as file:
                data = json.load(file, strict=False)
                print("JSON is open")

            for key in data.keys():
                print(f"{key = } ({type(data[key])})")

        except:
            print("JSON NOT open!!!")
        print()


if __name__ == "__main__":

    arguments = treat_arguments(SOFTWARE_ACRONYM, SOFTWARE_NAME, SOFTWARE_VERSION, SOFTWARE_URL)
    logger = initialize_logger()

    # Treating user argument catalog_path (it always must have a '/' by the end)
    if arguments["catalog_path"][-1] != "/":
        arguments["catalog_path"] += "/"

    # Switching tool according to received arguments
    if arguments["verify_data_quality"]:
        run_data_quality_verifications(arguments)
    elif arguments["generate_release"]:
        generate_release_file(arguments["catalog_path"])
    elif arguments["validate_ttl"]:
        validate_ttl_syntax(arguments["catalog_path"])
    elif arguments["fix_json"]:
        fix_json(arguments["catalog_path"])
    else:
        logger.error("No feature selected. Please provide at least one valid argument. Use argument '-h' for help.")
        exit(1)
