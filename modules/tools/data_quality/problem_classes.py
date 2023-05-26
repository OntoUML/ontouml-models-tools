""" Definition of classes for storing different types of problems identified in each data quality sub-feature. """


class DataQualityProblemClass(object):
    """ Main class to identify problems for each feature. Used for type hinting. """
    pass


class ProblemChar(DataQualityProblemClass):
    """ Class that contains information about problems found in evaluations for characters. """

    def __init__(self, instance_name, type_name, description):
        self.instance = instance_name
        self.type = type_name
        self.description = description


class ProblemEnds(DataQualityProblemClass):
    """ Class that contains information about problems found in evaluations for association ends. """

    def __init__(self, related_class, relation_name, end_name, description):
        self.related_class = related_class
        self.relation_name = relation_name
        self.end_name = end_name
        self.description = description


class ProblemGeneralizations(DataQualityProblemClass):
    """ Class that contains information about problems found in generalizations. """

    def __init__(self, generalization_name, specific_name, general_name, description):
        self.generalization_name = generalization_name
        self.specific_name = specific_name
        self.general_name = general_name
        self.description = description


class ProblemOldStereotypes(DataQualityProblemClass):
    """ Class that contains information about problems found in generalizations. """

    def __init__(self, class_name, old_stereotype, new_stereotype):
        self.class_name = class_name
        self.old_stereotype = old_stereotype
        self.new_stereotype = new_stereotype
