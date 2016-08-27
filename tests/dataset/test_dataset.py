import unittest

from dframe.dataset.dataset import Dataset


class DatasetTest(unittest.TestCase):

    # ------------------- Init ----------------------
    def test_construct_given_none_should_initialize_samples_as_list(self):
        sut = Dataset()
        self.assertIsInstance(sut.get_samples(), list)
        self.assertListEqual([], sut.get_samples())

    def test_construct_given_non_iterable_should_raise_exception(self):
        self.assertRaises(TypeError, Dataset, 1)

    def test_construct_given_list_should_assign_samples(self):
        samples = [1, 2, 3]
        sut = Dataset(samples)
        self.assertIsInstance(sut.get_samples(), list)
        self.assertListEqual(samples, sut.get_samples())

    # ----------------------- Add ------------------
    def test_add_given_none_should_do_nothing(self):
        samples = [1, 2, 3]
        sut = Dataset(samples)
        sut.add(None)
        self.assertListEqual(samples, sut.get_samples())

    def test_add_give_empty_list_should_do_nothing(self):
        samples = [1, 2, 3]
        sut = Dataset(samples)
        sut.add([])
        self.assertListEqual(samples, sut.get_samples())

    def test_add_given_single_item_should_add_elem(self):
        samples = [1, 2, 3]
        sut = Dataset(samples)
        sut.add(4)
        samples.append(4)
        self.assertListEqual(samples, sut.get_samples())

    def test_add_given_list_should_add_elements(self):
        samples = [1, 2, 3]
        sut = Dataset(samples)
        sut.add([4, 5, 6])
        samples.extend([4, 5, 6])
        self.assertListEqual(samples, sut.get_samples())

if __name__ == '__main__':
    unittest.main()
