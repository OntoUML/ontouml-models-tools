""" Logging configurations. """

import logging
import os

from modules.utils.utils_general import get_date_time


def initialize_logger(source="default"):
    """ Initialize Logger. """

    # Create a custom logger
    new_logger = logging.getLogger("logger")

    if source == "default":
        new_logger.setLevel(logging.DEBUG)
    else:
        print(f"Logger parameter unknown ({source}). Aborting execution.")

    # Creates a new logger only if logger does not exist yet
    if not logging.getLogger("logger").hasHandlers():

        # Creating CONSOLE handler
        console_handler = logging.StreamHandler()
        if source == "default":
            console_handler.setLevel(logging.INFO)
        else:
            print(f"Logger parameter unknown ({source}). Aborting execution.")

        # If directory "/log" does not exist, create it
        log_dir = "logs/"
        try:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
        except OSError as error:
            print(f"Could not create {log_dir} directory. Exiting program."
                  f"System error reported: {error}")
            exit(1)

        # Creating FILE handler
        file_handler = logging.FileHandler(f"{log_dir}{get_date_time()}.log")
        if source == "default":
            file_handler.setLevel(logging.DEBUG)
        else:
            print(f"Logger parameter unknown ({source}). Aborting execution.")

        # Create formatters and add it to handlers
        console_format = logging.Formatter('%(levelname)s - %(message)s')
        file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s [func: %(funcName)s '
                                        'in %(filename)s]')
        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)

        # Add handlers to the logger
        new_logger.addHandler(console_handler)
        new_logger.addHandler(file_handler)

    return new_logger
