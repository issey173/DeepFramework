import random

from dframe.dataset.sample import IO


class Dataset(IO):
    """Class representing a dataset that holds its information as a list of samples."""

    def __init__(self, samples=None):
        """The samples parameter should be a list of dframe.dataset.sample.Sample instances or
        instances of subclasses"""

        if samples:
            if not isinstance(samples, list):
                raise TypeError('The parameter samples must be a list or a subclass of list')
            self._samples = samples
        else:
            self._samples = []

    def get_samples(self):
        return self._samples

    def add(self, samples):
        """Add a single sample or a list of them"""

        if not samples:
            return

        try:
            # samples is a collection (actually an Iterable)
            self._samples.extend(samples)
        except TypeError:
            # samples is a single item (or not Iterable)
            self._samples.append(samples)

    def remove(self, samples):
        """Remove a single sample or a list of them. If the sample/s is not found, an exception will be raised.

        If you are removing a list of samples and one of them is not present in the dataset, all the previous samples
        before that one will be effectively erased.
        """

        try:
            # Samples is a collection
            for sample in samples:
                self._samples.remove(sample)
        except TypeError:
            # Samples is a single item
            self._samples.remove(samples)

    def shuffle(self):
        random.shuffle(self._samples)

    def get_input(self):
        pass

    def get_output(self):
        pass

    def batch_generator(self):
        pass

    def save(self):
        pass

    def load(self):
        pass
