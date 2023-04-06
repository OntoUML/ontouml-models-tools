""" Functions related to the catalog used in multiple features. """
import pathlib


def list_all_ttl_files(catalog_path: str, exclusion_string: str = "not_set_not_set") -> list:
    """ Return a list of all ttl files (complete path) from the catalog that do not contain exclusion_string on its
    file name. """

    list_ttl_files = []

    catalog_pathlib = pathlib.Path(catalog_path)
    for ttl_item in list(catalog_pathlib.rglob('*.ttl')):
        if (".git" not in str(ttl_item)) and (exclusion_string not in str(ttl_item)):
            list_ttl_files.append(str(ttl_item))

    return list_ttl_files
