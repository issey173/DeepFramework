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
        sut = Dataset(list(samples))
        sut.add(None)
        self.assertListEqual(samples, sut.get_samples())

    def test_add_give_empty_list_should_do_nothing(self):
        samples = [1, 2, 3]
        sut = Dataset(list(samples))
        sut.add([])
        self.assertListEqual(samples, sut.get_samples())

    def test_add_given_single_item_should_add_elem(self):
        samples = [1, 2, 3]
        sut = Dataset(list(samples))
        sut.add(4)
        samples.append(4)
        self.assertListEqual(samples, sut.get_samples())

    def test_add_given_list_should_add_elements(self):
        samples = [1, 2, 3]
        sut = Dataset(list(samples))
        sut.add([4, 5, 6])
        samples.extend([4, 5, 6])
        self.assertListEqual(samples, sut.get_samples())

    # ------------------- Remove ------------------------
    def test_remove_given_unexistent_sample_should_raise_exception(self):
        sut = Dataset([1, 2, 3])
        self.assertRaises(ValueError, sut.remove, 4)

    def test_remove_given_existent_sample_should_remove_it(self):
        samples = [1, 2, 3]
        sut = Dataset(list(samples))
        sut.remove(3)
        samples.remove(3)
        self.assertListEqual(samples, sut.get_samples())

    def test_remove_given_list_with_unexistent_sample_should_raise_exception(self):
        samples = [1, 2, 3]
        sut = Dataset(list(samples))
        self.assertRaises(ValueError, sut.remove, [1, 4])

    def test_remove_give_list_with_existent_samples_should_remove_them(self):
        samples = [1, 2, 3]
        sut = Dataset(list(samples))
        sut.remove([1, 2])
        samples.remove(1)
        samples.remove(2)
        self.assertListEqual(samples, sut.get_samples())


if __name__ == '__main__':
    unittest.main()
