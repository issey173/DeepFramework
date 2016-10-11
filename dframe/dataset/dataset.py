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

    def get_input(self, axis_samples=True, offset=0, num_elems=None):
        """Return the dataset input.

        This input is an array with the input of all of its samples. It is responsability of the user to make sure that
        all samples have the same number of inputs, otherwise the returned array will not match with its samples. In
        some specific cases the method can raise a ValueError to notify of this inconsistency, but you should not
        depend on that as this will not always be the case. A consistency check is not performed to avoid unnecessary
        overhead with large datasets.

        Args:
            axis_samples (bool): If true, the first axis of the returned array will be the sample index (input[0]
                will be the inputs of the first sample). Otherwise, the first axis will be the input (input[0] will be
                a list with the first input of all samples)
            offset (int): The offset of the chunk of dataset to retrieve the input from. Default is 0
            num_elems (int): The size of the chunk. If not specified, it will be all the elements from the offset until
                the end. This will also be the maximum, if more than len-offset elements are specified
        """

        end = self.len()
        if num_elems is not None:
            end = offset + num_elems

        try:
            if axis_samples:
                inputs = [sample.get_input() for sample in self._samples[offset:end]]
            else:
                num_inputs = self._samples[0].num_inputs
                inputs = [[] for _ in range(num_inputs)]
                map(
                    lambda idx, val: inputs[idx].append(val),
                    [input_num for sample in self._samples[offset:end] for input_num, _ in
                     enumerate(sample.get_input())],
                    [sample_input for sample in self._samples[offset:end] for sample_input in sample.get_input()]
                )
            return inputs
        except AttributeError:
            raise TypeError('Some of the samples are not an instance or subclass of dframe.dataset.sample.Sample')
        except IndexError:
            raise ValueError('The dataset has data inconsistency as some of it samples differ in number of inputs')

    def get_output(self, axis_samples=True, offset=0, num_elems=None):
        """Return the dataset output.

        This output is an array with the output of all of its samples. It is responsability of the user to make sure
        that all samples have the same number of outputs, otherwise the returned array will not match with its samples.
        In some specific cases the method can raise a ValueError to notify of this inconsistency, but you should not
        depend on that as this will not always be the case. A consistency check is not performed to avoid unnecessary
        overhead with large datasets.

        Args:
            axis_samples (bool): If true, the first axis of the returned array will be the sample index (output[0]
                will be the outputs of the first sample). Otherwise, the first axis will be the output (output[0] will
                be a list with the first output of all samples)
            offset (int): The offset of the chunk of dataset to retrieve the input from. Default is 0
            num_elems (int): The size of the chunk. If not specified, it will be all the elements from the offset until
                the end. This will also be the maximum, if more than len-offset elements are specified
        """

        end = self.len()
        if num_elems is not None:
            end = offset + num_elems

        try:
            if axis_samples:
                outputs = [sample.get_output() for sample in self._samples[offset:end]]
            else:
                num_outputs = self._samples[0].num_outputs
                outputs = [[] for _ in range(num_outputs)]
                map(
                    lambda idx, val: outputs[idx].append(val),
                    [output_num for sample in self._samples[offset:end] for output_num, _ in
                     enumerate(sample.get_output())],
                    [sample_output for sample in self._samples[offset:end] for sample_output in sample.get_output()]
                )
            return outputs
        except AttributeError:
            raise TypeError('Some of the samples are not an instance or subclass of dframe.dataset.sample.Sample '
                            'or they do not have output')
        except IndexError:
            raise ValueError('The dataset has data inconsistency as some of it samples differ in number of outputs')

    def batch_generator(self, batch_size, shuffle=True):
        batch_start = 0
        while True:
            # Get and yield the batch
            inputs = self.get_input(axis_samples=False, offset=batch_start, num_elems=batch_size)
            outputs = self.get_output(axis_samples=False, offset=batch_start, num_elems=batch_size)
            yield (inputs, outputs)

            # Update the counters
            batch_start += batch_size
            if batch_start >= self.len():
                # End of epoch - begining of the next one (first batch)
                batch_start = 0
                if shuffle:
                    self.shuffle()

    def len(self):
        return len(self._samples)

    def merge(self, dataset):
        """Shortcut to extend this dataset with the samples from the given one"""
        try:
            self.add(dataset.get_samples())
        except AttributeError:
            raise TypeError('The object you provided is not a Dataset (dframe.dataset.dataset.Dataset)')

    def __add__(self, other):
        try:
            return Dataset(self._samples + other.get_samples())
        except AttributeError:
            raise TypeError('A dataset cannot be added with \'' + type(other).__name__ + '\'')

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __iter__(self):
        return self._samples.__iter__()
