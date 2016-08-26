from abc import ABCMeta, abstractmethod


# noinspection PyClassHasNoInit
class Value:
    """Interface like class for all the classes that are meant to be part of a sample (input or output)"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_data(self):
        """Return the content of this object"""
        pass


class Sample:
    """Base class to hold the information of an example/sample in a dataset"""

    __metaclass__ = ABCMeta

    def __init__(self, inputs, outputs):
        """Creates a sample out of its inputs and outputs.

        They can be either collections or single objects. For 'non-primitive' types it is recomended to use classes
        that extend from Value, as this is the interface used to obtain 'numeric data' from these complex objects
        """
        
        self.inputs = inputs
        self.outputs = outputs

    def get_input(self):
        return self._get_data(self.inputs)

    def get_output(self):
        return self._get_data(self.outputs)

    @staticmethod
    def _get_data(elems):
        """Obtains the data from the elements given, using the interface Value for complex items."""

        try:
            # Collection of items extending from Value ('complex' inputs)
            data = [i.get_data() for i in elems]
        except TypeError:
            # It is not a collection but a single element
            try:
                data = elems.get_data()
            except AttributeError:
                # elems is not a collection of Value neither a single Value
                data = elems
        except AttributeError:
            # elems is not a collection of Value neither a single Value
            data = elems

        return data
