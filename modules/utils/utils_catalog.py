""" Functions related to the catalog used in multiple features. """
import pathlib


def list_all_ttl_files(catalog_path: str) -> list:
    """ Return a list of all ttl files (complete path) from the catalog folder. """

    list_ttl_files = []

    catalog_pathlib = pathlib.Path(catalog_path)
    for ttl_item in list(catalog_pathlib.rglob('*.ttl')):
        if "\\." not in str(ttl_item):
            list_ttl_files.append(str(ttl_item))

    return list_ttl_files
