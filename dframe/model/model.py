from abc import ABCMeta, abstractmethod


# noinspection PyClassHasNoInit
class Model:
    """Interface like class to encapsulate model's logic"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def build(self):
        """Creates the architecture of the model given its parameters"""
        pass

    @abstractmethod
    def train(self, dataset):
        """Trains the model with the given dataset"""
        pass

    @abstractmethod
    def validate(self, dataset):
        """Validates the model using the given dataset"""
        pass

    @abstractmethod
    def test(self, dataset):
        """Tests the model using the given dataset.

        Returns the collection of results, one for each sample"""
        pass

    @abstractmethod
    def predict(self, sample):
        """Predicts the output for the given sample"""
        pass
