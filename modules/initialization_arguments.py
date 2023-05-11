""" Argument Treatments """

import argparse

from modules.logger_config import initialize_logger


def treat_arguments(software_acronym, software_name, software_version, software_url):
    """ Treats user ontologies arguments. """

    logger = initialize_logger()
    logger.debug("Parsing arguments...")

    about_message = software_acronym + " - version " + software_version

    # PARSING ARGUMENTS
    arguments_parser = argparse.ArgumentParser(prog="ontouml-models-tools",
                                               description=software_acronym + " - " + software_name,
                                               allow_abbrev=False,
                                               epilog=software_url)

    arguments_parser.version = about_message

    # AUTOMATIC ARGUMENT
    arguments_parser.add_argument("-v", "--version", action="version", help="Prints the software version and exit.")

    # POSITIONAL ARGUMENT
    arguments_parser.add_argument("catalog_path", type=str, action="store",
                                  help="The path of the OntoUML/UFO Catalog directory.")

    # OPTIONAL ARGUMENTS

    automation_group = arguments_parser.add_mutually_exclusive_group()

    automation_group.add_argument("-d", "--data_quality.py", action='store_true',
                                  help="Execute data quality verifications.")

    automation_group.add_argument("-j", "--fix_json", action='store_true',
                                  help="Fix small issues on the ontology.json file.")

    automation_group.add_argument("-r", "--release", action='store_true',
                                  help="Execute release file generation.")

    automation_group.add_argument("-t", "--validate_ttl", action='store_true',
                                  help="Validate the syntax of all ttl files.")

    # Execute arguments parser
    arguments = arguments_parser.parse_args()

    received_arguments = {
        "catalog_path": arguments.catalog_path,
        "verify_data_quality": arguments.data_quality,
        "fix_json": arguments.fix_json,
        "generate_release": arguments.release,
        "validate_ttl": arguments.validate_ttl
    }

    logger.debug(f"Arguments Parsed. Obtained values are: {received_arguments}")

    return received_arguments
