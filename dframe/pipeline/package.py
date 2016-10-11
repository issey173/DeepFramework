from abc import ABCMeta, abstractmethod


class Package:
    """Class that holds the input to be processed and that the Core interacts with to store the results.

    A package object is what flows through the Pipeline.
    The package is a stack of layers, the first layer being the input (what needs to be processed by the pipeline/core)
    and the following ones being the result of each of the cores composing a pipeline. Therefore, the last layer (the
    one at the top) is the final result of the whole processing chain.
    """

    def __init__(self, package_id):
        self.package_id = package_id
        self._layers = []

    def add_layer(self, layer):
        self._layers.append(layer)

    def remove_layer(self, layer):
        self._layers.remove(layer)

    def get_layer(self, n):
        try:
            return self._layers[n]
        except IndexError:
            raise IndexError(
                'The layer number {} does not exist. This package only has {} layers'.format(n, self.num_layers()))

    def num_layers(self):
        return len(self._layers)

    def get_input(self):
        """Alias method to get the input"""
        try:
            return self._layers[0]
        except IndexError:
            raise ValueError('This package does not have an input layer')

    def get_output(self):
        """Alias method to get the output"""
        try:
            return self._layers[-1]
        except IndexError:
            raise ValueError('This package does not have an output layer')


# noinspection PyClassHasNoInit
class PackageProcessor:
    """Interface like class for those classes that are able to process a dframe.pipeline.package.Package"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def process_package(self, package):
        if not isinstance(package, Package):
            raise TypeError('The given package must be an instance of dframe.pipeline.package.Package')
