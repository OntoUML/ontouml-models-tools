""" Functions related to the catalog used in multiple features. """
import pathlib


def list_all_files_with_filetype(catalog_path: str, filetype: str) -> list:
    """ Receives as argument the catalog path and an intended filetype.
        Return a list of all files (complete path) inside the catalog folder that have the informed filetype.
    """

    list_files = []

    catalog_pathlib = pathlib.Path(catalog_path)
    for filetype_item in list(catalog_pathlib.rglob(f'*.{filetype}')):
        if "\\." not in str(filetype_item):
            list_files.append(str(filetype_item))

    return list_files
