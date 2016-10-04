import cPickle
import os
from abc import ABCMeta, abstractmethod

import h5py

from dframe.dataset.dataset import Dataset
from dframe.dataset.sample import Sample


# noinspection PyClassHasNoInit
class PersistenceManager:
    """Interface like class that exposes the methods that all persistence managers must have.

    Classes extending from this are supposed to be in charge of persisting dataset into some sort of persistence system
    (file, DB...).
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, dataset, path):
        """Saves the dataset into the persistence system"""
        if not self.supports_saving(dataset):
            raise TypeError('This persistence manager cannot save this dataset')

    @abstractmethod
    def load(self, path):
        """Loads the dataset from the persistence system.

        This should return an instance of dframe.dataset.dataset.Dataset
        """
        if not self.supports_loading(path):
            raise TypeError('This persistence manager cannot load the dataset from the specified path')
        pass

    @abstractmethod
    def supports_saving(self, dataset):
        """Returns if this PersistenceManager can save the given dataset or not.

        A boolean should be returned.
        """
        pass

    @abstractmethod
    def supports_loading(self, path):
        """Returns if this PersistenceManager can load the dataset from the file path given.

        A boolean should be returned.
        """
        pass


# noinspection PyClassHasNoInit
class H5pyPersistenceManager(PersistenceManager):
    """Persistence manager that will save/load the dataset using HDF5.

    Note that with this manager, only the actual data is persisted and thus the load method will not be able to create
    the dataset with its original classes. Use this for large datasets where memory is a problem.
    Use PicklePersistenceManager if a full recovery is needed"""

    INPUT_DATASET_NAME = 'inputs'
    OUTPUT_DATASET_NAME = 'outputs'

    def save(self, dataset, path):
        """Saves the dataset in disk using HDF5.

        Only the raw data will be persisted and thus the actual objects/classes will not be recovered when loading."""
        super(H5pyPersistenceManager, self).save(dataset, path)
        # If file exists, truncate
        with h5py.File(path, 'w') as f:
            # Get inputs and persist into a dataset in HDF5 root group
            inputs = dataset.get_input()
            f.create_dataset(self.INPUT_DATASET_NAME, data=inputs)
            # Get output (if some) and persist into a dataset in HDf5 root gorup
            try:
                outputs = dataset.get_output()
                f.create_dataset(self.OUTPUT_DATASET_NAME, data=outputs)
            except TypeError:
                # If there are no outputs (e.g. test dataset), do nothing
                pass

    def load(self, path):
        """Creates a Dataset object from the data saved in HDF5 file.

        The dataset will contain plain Sample objects with the raw data.
        """

        super(H5pyPersistenceManager, self).load(path)
        with h5py.File(path, 'r') as f:
            inputs = f[self.INPUT_DATASET_NAME]
            if self.OUTPUT_DATASET_NAME in f:
                outputs = f[self.OUTPUT_DATASET_NAME]
                samples = [Sample(sample_input, outputs[idx]) for idx, sample_input in enumerate(inputs)]
            else:
                samples = [Sample(sample_input) for sample_input in inputs]

            return Dataset(samples)

    def supports_saving(self, dataset):
        return isinstance(dataset, Dataset)

    def supports_loading(self, path):
        return os.path.isfile(path)


# noinspection PyClassHasNoInit
class PicklePersistenceManager(PersistenceManager):
    """Persistence manager that uses cPickle as its persistence system.

    This persistence manager is not as efficient as H5pyPersistenceManager but can persist and recover the dataset as
    it is.
    """

    def save(self, dataset, path):
        super(PicklePersistenceManager, self).save(dataset, path)
        with open(path, 'w') as f:
            cPickle.dump(dataset, f)

    def load(self, path):
        super(PicklePersistenceManager, self).load(path)
        with open(path) as f:
            return cPickle.load(f)

    def supports_saving(self, dataset):
        return isinstance(dataset, Dataset)

    def supports_loading(self, path):
        return os.path.isfile(path)
