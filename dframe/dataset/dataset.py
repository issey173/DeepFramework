from dframe.dataset.sample import IO


class Dataset(IO):
    """Class representing a dataset that holds its information as a list of samples."""

    def __init__(self, samples=None):
        """The samples parameter should be a list of dframe.dataset.sample.Sample instances or
        instances of subclasses"""

        if samples:
            self.samples = samples
        else:
            self.samples = []

    def add(self):
        pass

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
