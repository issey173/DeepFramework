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
        if not samples:
            return

        try:
            # samples is a collection (actually an Iterable)
            self._samples.extend(samples)
        except TypeError:
            # samples is a single item (or not Iterable)
            self._samples.append(samples)

    def remove(self):
        pass

    def shuffle(self):
        pass

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
