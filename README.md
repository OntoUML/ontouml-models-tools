# OntoUML/UFO Models Tools

The aim of the **ontouml-models-tools** is to offer a set of useful tools for
the [OntoUML/UFO Catalog](https://github.com/unibz-core/ontouml-models) collaborators and administrators.

## Contents

- [OntoUML/UFO Models Tools](#ontoumlufo-models-tools)
    - [Contents](#contents)
    - [Provided Tools](#provided-tools)
        - [Data Quality Tools](#data-quality-tools)
            - [Identification of Unwanted Characters](#identification-of-unwanted-characters)
            - [Identification of Possible Multiplicities in Association Ends Roles](#identification-of-possible-multiplicities-in-association-ends-roles)
            - [Identification of Possible Meta-properties Written as Names in Generalizations](#identification-of-possible-meta-properties-written-as-names-in-generalizations)
            - [Identification of Stereotypes that can be Updated](#identification-of-stereotypes-that-can-be-updated)
        - [Release File Generation](#release-file-generation)
        - [Syntax Validation for TTL Files](#syntax-validation-for-ttl-files)
        - [Future Features](#future-features)
    - [Execution Instructions](#execution-instructions)
    - [Contributors](#contributors)

## Provided Tools

### Data Quality Tools

The data quality evaluation feature can be executed by using the *-d* argument. When executed, all features here
presented as subsections are performed.

#### Identification of Unwanted Characters

The `ontology.ttl` files inside each one of the catalog’s datasets are evaluated intending to identify the following
unwanted characters in any elements:

- starts with space
- ends with space
- has double space
- has line break (presence of “\n”)
- has indentation (presence of “\t”)
- stereotype in name (presence of “\<\<” or “\>\>”)
- derivation in name (presence of “/”)
- imported class represented in name (presence of “::”)

The ontouml-models-tools software reports the found problems in the `results_char.csv` file, which is generated into the
project’s `result` folder. This file is a *csv* with the following headers:

- `dataset`: the dataset in which the identified problem is located.
- `instance`: the name of the instance that has the identified problem.
- `type`: the type of the problematic instance (e.g., Class, Relation).
- `problem`: a brief phrase describing the problem found.

#### Identification of Possible Multiplicities in Association Ends Roles

This functionality verifies if there are numbers or asterisks in association end roles. When providing manual
information to
the modeling software, a modeler can easily insert the association cardinality (multiplicity) in the incorrect field,
filling the association end role instead of the association end multiplicity.

The ontouml-models-tools software reports the found possible problems in the `results_ends.csv` file, which is generated
into the project’s `result` folder. This file is a *csv* with the following headers:

- `dataset`: the dataset in which the identified problem is located.
- `related_class`: a class that is related via the association that may have a problem (this information is provided for
  more easily locating the relation).
- `relation_name`: the name of the association that contains the association end that may have a problem.
- `end_value`: the value attributed to the association end role.
- `problem`: a brief phrase describing the problem found.

#### Identification of Possible Problems in Generalizations

This functionality performs three verifications.

1) It verifies if there are certain strings that indicate that the modeler has set generalization sets'
   meta-properties as a generalization name. The results display only cases in which the generalization has a name and
   is
   not part of any generalization set.
2) It verifies if there are generalization sets with both covering and disjoint metaproperties set as False.
3) It verifies if there are generalization sets with less than two generalizations as their parts.

The ontouml-models-tools software reports the found possible problems in the `results_gens.csv` file, which is generated
into the project’s `result` folder. This file is a *csv* with the following headers:

- `dataset`: the dataset in which the identified problem is located.
- `generalization_name`: the name provided by the modeler to the generalization.
- `specific_name` For 1: the name of the subclass that participates in the generalization. For 2) empty, For 3)
  information about the generalization set's quantity of generalizations.
- `general_name`: For 1: the name of the superclass that participates in the generalization. For 2 and 3) empty.
- `problem`: a brief phrase describing the problem found.

#### Identification of Stereotypes that can be Updated

This functionality verifies if there are stereotypes that can be substituted by a more recent name, as defined in
the [catalog's documentation](https://github.com/OntoUML/ontouml-models/wiki/Frequently-Asked-Questions#how-do-i-document-stereotypes-that-are-not-part-of-the-current-ontouml-profile)
.

The ontouml-models-tools software reports the found possible problems in the `results_ster.csv` file, which is generated
into the project’s `result` folder. This file is a *csv* with the following headers:

- `dataset`: the dataset in which the identified problem is located.
- `class_name`: the name of the class with the outdated stereotype.
- `old_stereotype` the stereotype to be substituted.
- `new_stereotype`: the updated stereotype that must be used to substitute the outdated one.

### Release File Generation

This feature can be executed by providing the *-r* argument. When selected, it will generate a single ttl file as output
in the `results` folder following the nomenclature `ontouml-models-<YYYY><MM><DD>.ttl`, with Y, M, and D being
substituted by the current date. The output file contains all information available in every ttl file that is part of
the catalog, except from the [shape files](https://github.com/OntoUML/ontouml-models/tree/master/shapes).

### Syntax Validation for TTL Files

Uses the [MMLab TurtleValidator](https://github.com/MMLab/TurtleValidator), an external command line application, for
validating every TTL file in the catalog folder.

This functionality requires the previous installation of
the [MMLab TurtleValidator](https://github.com/MMLab/TurtleValidator). The installation instructions can be found in the
provided link.

### Future Features

The intended features to be implemented are available [as issues](https://github.com/OntoUML/ontouml-models-tools/issues) in this repository.

## Execution Instructions

You need to [download and install Python](https://www.python.org/downloads/) for executing the ontouml-catalog-tools.
Its code was developed and tested using Python v3.11.0.

For installing all necessary dependencies, run the following command on the terminal inside the project’s folder:

```text
pip install -r requirements.txt
```

For executing the software, run the following command on the terminal inside the project’s folder,
where `path_to_catalog` must be substituted for the location of the catalog’s directory on your computer:

```text
python main.py path_to_catalog -arg
```

As mentioned, the OntoUML/UFO Catalog must be available as a folder in the user’s filesystem. For that, you
must [clone its GitHub repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
. All available ontouml-models-tools arguments can be observed below.

```text
usage: ontouml-models-tools [-h] [-v] [-d | -r] catalog_path

OntoUML/UFO Catalog Tools - ontouml-models-tools

positional arguments:
  catalog_path        The path of the OntoUML/UFO Catalog directory.

options:
  -h, --help          show this help message and exit
  -v, --version       Prints the software version and exit.
  -d, --data_quality  Execute data quality verifications.
  -r, --release       Execute release file generation.
  -t, --validate_ttl  Validate the syntax of all ttl files.
```

## Contributors

- [Pedro Paulo Favato Barcelos](https://orcid.org/0000-0003-2736-7817) [[GitHub](https://github.com/pedropaulofb)] [[LinkedIn](https://www.linkedin.com/in/pedropaulofavatobarcelos/)]

Please get in touch with this software’s contributors using the provided links or **
preferably** [open an issue](https://github.com/unibz-core/ontouml-models-tools/issues/) in case of doubts or problems
found.
