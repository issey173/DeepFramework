from abc import ABCMeta, abstractmethod


# noinspection PyClassHasNoInit
class PersistenceManager:
    """Interface like class that exposes the methods that all persistence managers must have.

    Classes extending from this are supposo to be in charge of persisting dataset into some sort of persistence system
    (file, DB...).
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, dataset):
        """Saves the dataset into the persistence system"""
        pass

    @abstractmethod
    def load(self):
        """Loads the dataset from the persistence system.

        This should return an instance of dframe.dataset.dataset.Dataset
        """
        pass

    @abstractmethod
    def supports_persistence(self, dataset):
        """Returns if this PersistenceManager can persist the given dataset or not.

        A boolean should be returned
        """
        pass
