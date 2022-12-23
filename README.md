# OntoUML/UFO Models Tools

The aim of the **ontouml-models-tools** is to offer a set of useful tools for the [OntoUML/UFO Catalog](https://github.com/unibz-core/ontouml-models) collaborators and administrators.

## Contents

- [Provided Tools](#provided-tools)
  - [Identification of Unwanted Characters](#identification-of-unwanted-characters)
  - [Identification of Possible Multiplicities in Association Ends Roles](#identification-of-possible-multiplicities-in-association-ends-roles)
  - [Future Features](#future-features)
- [Execution Instructions](#execution-instructions)
- [Contributors](#contributors)

## Provided Tools

### Identification of Unwanted Characters

The `ontology.ttl` files inside each one of the catalog’s datasets are evaluated intending to identify the following unwanted characters in any elements:

- starts with space
- ends with space
- has double space
- has line break (presence of “\n”)
- has indentation (presence of “\t”)
- stereotype in name (presence of “\<\<” or “\>\>”)
- derivation in name (presence of “/”)
- imported class represented in name (presence of “::”)

The ontouml-models-tools software reports the found problems in the `results_char.csv` file, which is generated into the project’s folder. This file is a *csv* with the following headers:

- `dataset`: the dataset in which the identified problem is located.
- `instance`: the name of the instance that has the identified problem.
- `type`: the type of the problematic instance (e.g., Class, Relation).
- `problem`: a brief phrase describing the problem found.

### Identification of Possible Multiplicities in Association Ends Roles

This function verifies if there are numbers in association end roles. When providing manual information to the modeling software, a modeler can easily insert the association cardinality (multiplicity) in the incorrect field, filling the association end role instead of the association end multiplicity.

The ontouml-models-tools software reports the found possible problems in the `results_ends.csv` file, which is generated into the project’s folder. This file is a *csv* with the following headers:

- `dataset`: the dataset in which the identified problem is located.
- `related_class`: a class that is related via the association that may have a problem (this information is provided for more easily locating the relation).
- `relation_name`: the name of the association that contains the association end that may have a problem.
- `end_value`: the value attributed to the association end role.
- `problem`: a brief phrase describing the problem found.

### Future Features

The intended features to be implemented are available as issues in this repository.

## Execution Instructions

You need to [download and install Python](https://www.python.org/downloads/) for executing the ontouml-catalog-tools. Its code was developed and tested using Python v3.11.0.

For installing all necessary dependencies, run the following command on the terminal inside the project’s folder:

```shell
pip install -r requirements.txt
```

For executing the software, run the following command on the terminal inside the project’s folder, where `path_to_catalog` must be substituted for the location of the catalog’s directory on your computer:

```shell
python main.py path_to_catalog
```

As mentioned, the OntoUML/UFO Catalog must be available as a folder in the user’s filesystem. For that, you must [clone its GitHub repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

## Contributors

- PhD. Pedro Paulo Favato Barcelos [[GitHub](https://github.com/pedropaulofb)] [[LinkedIn](https://www.linkedin.com/in/pedropaulofavatobarcelos/)]

Please get in touch with this software’s contributors using the provided links or **preferably** [open an issue](https://github.com/unibz-core/ontouml-models-tools/issues/) in case of doubts or problems found.
