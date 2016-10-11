from abc import ABCMeta, abstractmethod


# noinspection PyClassHasNoInit
class IO:
    """Interface like class for classes that have input-output operations"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_input(self):
        pass

    @abstractmethod
    def get_output(self):
        pass


# noinspection PyClassHasNoInit
class Value:
    """Interface like class for all the classes that are meant to be part of a sample (input or output)"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_data(self):
        """Return the content of this object"""
        pass


class Sample(IO):
    """Base class to hold the information of an example/sample in a dataset"""

    def __init__(self, inputs, outputs=None):
        """Creates a sample out of its inputs and outputs.

        They can be either collections or single objects. For 'non-primitive' types it is recomended to use classes
        that extend from Value, as this is the interface used to obtain 'numeric data' from these complex objects.

        If you want to provide a single input/output holding a collection, you must provide it within an enclosing
        list, otherwise each element in the collection will be taken as an input.
        e.g.:
            - Sample(1, None) -> sample with a single input (with value 1)
            - Sample([1, 2, 3], None) -> sample with 3 inputs with values 1, 2 and 3 respectively
            - Sample([[1, 2, 3]], None) -> sample with a single input which is a collection of three values
        """

        if inputs is None:
            raise ValueError('A sample must have some input data')

        self._inputs = inputs
        self._outputs = outputs

        self.num_inputs = self._get_elems_length(inputs)
        self.num_outputs = self._get_elems_length(outputs)

    def get_input(self):
        """Get the formatted input, the actual data.

        It will always return a list with as many items as inputs, each one holding the data of its input
        """
        return self._get_data(self._inputs)

    def get_exact_inputs(self):
        """Get the exact inputs that were given in creation time (in the constructor) as they are"""
        return self._inputs

    def get_output(self):
        """Get the formatted output, the actual data.

        If the sample has ouputs, it will return a list with as many items as outputs, each one holding the data of
        its output. Otherwise will raise an error as to sample do not have ouputs to get data from
        """

        if self._outputs is None:
            raise AttributeError('This sample has no output/s')
        return self._get_data(self._outputs)

    def get_exact_outputs(self):
        """Get the exact outputs that were given in creation time (in the constructor) as they are"""
        return self._outputs

    @staticmethod
    def _get_data(elems):
        """Obtains the data from the elements given, using the interface Value for complex items."""

        # If None
        if not elems:
            return

        try:  # Collection
            try:
                # Collection of items extending from Value ('complex' inputs)
                data = [i.get_data() for i in elems]
            except AttributeError:
                # Mixed collection with Value and non-Value objects
                data = []
                for item in elems:
                    if isinstance(item, Value):
                        data.append(item.get_data())
                    else:
                        data.append(item)
        except TypeError:  # Single item
            if isinstance(elems, Value):
                # Value
                # Wrap in a list to be consistent with the scenario where we have multiple elems
                data = [elems.get_data()]
            else:
                # Non-Value
                # Wrap in a list to be consistent with the scenario where we have multiple elems
                data = [elems]

        return data

    @staticmethod
    def _get_elems_length(elems):
        length = 0
        if elems is not None:
            try:
                length = len(elems)
            except TypeError:
                length = 1

        return length
