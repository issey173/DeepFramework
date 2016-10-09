from abc import ABCMeta, abstractmethod


# noinspection PyClassHasNoInit
class Model:
    """Interface like class to encapsulate model's logic"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def train(self, dataset):
        pass

    @abstractmethod
    def validate(self, dataset):
        pass

    @abstractmethod
    def test(self, dataset):
        pass

    @abstractmethod
    def predict(self, sample):
        pass
