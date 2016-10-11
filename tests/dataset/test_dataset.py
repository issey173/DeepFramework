import unittest

from dframe.dataset.dataset import Dataset
from dframe.dataset.sample import Sample


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

    # ----------------------- Get input ---------------------------
    def test_get_input_given_invalid_samples_should_raise_exception(self):
        sut = Dataset([1, 2, 3])
        self.assertRaises(TypeError, sut.get_input)

    def test_get_input_given_axis_samples_true_should_return_array_with_sample_as_first_axis(self):
        samples = [Sample([1, 2], 1), Sample([3, 4], 3)]
        sut = Dataset(samples)
        self.assertListEqual([[1, 2], [3, 4]], sut.get_input(axis_samples=True))

    def test_get_input_given_axis_samples_false_should_return_array_with_input_as_first_axis(self):
        samples = [Sample([1, 2], 1), Sample([3, 4], 3)]
        sut = Dataset(samples)
        self.assertListEqual([[1, 3], [2, 4]], sut.get_input(axis_samples=False))

    def test_get_input_given_axis_samples_false_and_inconsisten_samples_should_raise_exception(self):
        samples = [Sample(1, 1), Sample([3, 4], 3)]
        sut = Dataset(samples)
        self.assertRaises(ValueError, sut.get_input, False)

    def test_get_input_given_offset_should_return_array_without_offset_first_elems(self):
        samples = [Sample(1, None), Sample(2, None), Sample(3, None), Sample(4, None), Sample(5, None)]
        sut = Dataset(list(samples))
        self.assertListEqual([[2], [3], [4], [5]], sut.get_input(offset=1))

    def test_get_input_given_offset_and_num_elems_should_return_chunked_array(self):
        samples = [Sample(1, None), Sample(2, None), Sample(3, None), Sample(4, None), Sample(5, None)]
        sut = Dataset(list(samples))
        self.assertListEqual([[2], [3], [4]], sut.get_input(offset=1, num_elems=3))

    # ----------------------- Get output ---------------------------
    def test_get_output_given_invalid_samples_should_raise_exception(self):
        sut = Dataset([1, 2, 3])
        self.assertRaises(TypeError, sut.get_output)

    def test_get_output_given_axis_samples_true_should_return_array_with_sample_as_first_axis(self):
        samples = [Sample(1, [1, 2]), Sample(3, [3, 4])]
        sut = Dataset(samples)
        self.assertListEqual([[1, 2], [3, 4]], sut.get_output(axis_samples=True))

    def test_get_output_given_axis_samples_false_should_return_array_with_output_as_first_axis(self):
        samples = [Sample(1, [1, 2]), Sample(3, [3, 4])]
        sut = Dataset(samples)
        self.assertListEqual([[1, 3], [2, 4]], sut.get_output(axis_samples=False))

    def test_get_output_given_axis_samples_false_and_inconsisten_samples_should_raise_exception(self):
        samples = [Sample(1, 1), Sample(3, [3, 4])]
        sut = Dataset(samples)
        self.assertRaises(ValueError, sut.get_output, False)

    def test_get_output_given_offset_should_return_array_without_offset_first_elems(self):
        samples = [Sample(1, 1), Sample(1, 2), Sample(1, 3), Sample(1, 4), Sample(1, 5)]
        sut = Dataset(list(samples))
        self.assertListEqual([[2], [3], [4], [5]], sut.get_output(offset=1))

    def test_get_output_given_offset_and_num_elems_should_return_chunked_array(self):
        samples = [Sample(1, 1), Sample(1, 2), Sample(1, 3), Sample(1, 4), Sample(1, 5)]
        sut = Dataset(list(samples))
        self.assertListEqual([[2], [3], [4]], sut.get_output(offset=1, num_elems=3))

    def test_get_output_without_output_samples_should_raise_exception(self):
        sut = Dataset([Sample(1), Sample(2)])
        self.assertRaises(TypeError, sut.get_output)

    # ------------------------------ Merge ----------------------------------
    def test_merge_given_non_dataset_should_raise_exception(self):
        sut = Dataset()
        self.assertRaises(TypeError, sut.merge, 'no dataset')

    def test_merge_given_dataset_should_extend_original_dataset_with_given_one(self):
        samples_sut = [Sample(1, 1), Sample(2, 2)]
        samples_dataset = [Sample(3, 3), Sample(4, 4)]
        sut = Dataset(list(samples_sut))
        dataset = Dataset(list(samples_dataset))
        sut.merge(dataset)
        samples_sut.extend(samples_dataset)
        self.assertListEqual(samples_sut, sut.get_samples())

    # ---------------------------- Add Operator --------------------------
    def test_add_operator_with_non_dataset_should_raise_exception(self):
        sut = Dataset()
        self.assertRaises(TypeError, sut.__add__, 1)

    def test_add_operator_with_datasets_should_return_new_dataset_instance(self):
        d1 = Dataset()
        d2 = Dataset()
        d3 = d1 + d2
        self.assertIsInstance(d3, Dataset)
        self.assertNotEqual(d3, d1)
        self.assertNotEqual(d3, d2)

    def test_add_operator_with_datasets_should_return_dataset_with_all_samples(self):
        s1 = [Sample(1, 1), Sample(2, 2)]
        s2 = [Sample(3, 3), Sample(4, 4)]
        d1 = Dataset(list(s1))
        d2 = Dataset(list(s2))
        d3 = d1 + d2
        self.assertListEqual(s1 + s2, d3.get_samples())

    # ------------------------ Reverse Add Operator -------------------------
    def test_radd_operator_with_datasets_should_return_new_dataset_instance(self):
        d1 = Dataset()
        d2 = Dataset()
        d3 = sum([d1, d2])
        self.assertIsInstance(d3, Dataset)
        self.assertNotEqual(d3, d1)
        self.assertNotEqual(d3, d2)

    def test_radd_operator_with_datasets_should_return_dataset_with_all_samples(self):
        s1 = [Sample(1, 1), Sample(2, 2)]
        s2 = [Sample(3, 3), Sample(4, 4)]
        d1 = Dataset(list(s1))
        d2 = Dataset(list(s2))
        d3 = sum([d1, d2])
        self.assertListEqual(s1 + s2, d3.get_samples())


if __name__ == '__main__':
    unittest.main()
