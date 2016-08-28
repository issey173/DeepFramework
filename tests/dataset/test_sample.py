import unittest

from dframe.dataset.sample import Sample, Value


class SampleTest(unittest.TestCase):
    def test_get_data_with_none_should_return_none(self):
        self.assertIsNone(Sample._get_data(None))

    def test_get_data_with_primitive_should_return_primitive(self):
        elem = 1
        self.assertEqual([elem], Sample._get_data(elem))

    def test_get_data_with_list_primitives_should_return_list_primitives(self):
        elems = [1, 2, 3]
        self.assertItemsEqual(elems, Sample._get_data(elems))

    def test_get_data_with_value_object_should_return_its_data(self):
        data = [1, 2, 3]
        elem = DummyValue(data)
        self.assertItemsEqual([data], Sample._get_data(elem))

    def test_get_data_with_list_value_objects_should_return_list_data(self):
        data = [1, 2, 3]
        elems = [DummyValue(data), DummyValue(data)]
        self.assertIsInstance(Sample._get_data(elems), list)
        self.assertItemsEqual([data, data], Sample._get_data(elems))

    def test_get_data_with_mixed_list_should_return_list_data(self):
        elems = [1, DummyValue([1, 2, 3])]
        self.assertItemsEqual([1, [1, 2, 3]], Sample._get_data(elems))


class DummyValue(Value):
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data


if __name__ == '__main__':
    unittest.main()
