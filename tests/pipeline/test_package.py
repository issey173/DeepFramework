import unittest

from dframe.pipeline.package import Package


class PackageTest(unittest.TestCase):
    def setUp(self):
        self.sut = Package(package_id=1)

    def test_add_layer_should_increase_num_layers(self):
        self.sut.add_layer('new layer')
        self.assertTrue(self.sut.num_layers() == 1)

    def test_remove_layer_with_non_existing_layer_should_raise_exception(self):
        self.assertRaises(ValueError, self.sut.remove_layer, 'non existing layer')

    def test_remove_layer_with_existing_layer_should_decrease_num_layers(self):
        layer = 'layer'
        self.sut.add_layer(layer)
        self.assertTrue(self.sut.num_layers() == 1)
        self.sut.remove_layer(layer)
        self.assertTrue(self.sut.num_layers() == 0)

    def test_get_layer_with_non_existing_index_should_raise_exception(self):
        self.assertRaises(IndexError, self.sut.get_layer, 1)

    def test_get_layer_with_existing_index_should_return_layer(self):
        layer = 'layer'
        self.sut.add_layer(layer)
        self.assertEqual(layer, self.sut.get_layer(0))

    def test_num_layers_should_return_integer_with_number_layers(self):
        self.assertIsInstance(self.sut.num_layers(), int)
        self.assertEqual(0, self.sut.num_layers())
        self.sut.add_layer('layer')
        self.assertEqual(1, self.sut.num_layers())

    def test_get_input_without_layers_should_raise_exception(self):
        self.assertRaises(ValueError, self.sut.get_input)

    def test_get_input_should_return_first_layer(self):
        layer_one = 'layer 1'
        layer_two = 'layer 2'
        self.sut.add_layer(layer_one)
        self.sut.add_layer(layer_two)
        self.assertEqual(layer_one, self.sut.get_input())

    def test_get_output_without_layers_should_raise_exception(self):
        self.assertRaises(ValueError, self.sut.get_output)

    def test_get_output_should_return_last_layer(self):
        layer_one = 'layer 1'
        layer_two = 'layer 2'
        self.sut.add_layer(layer_one)
        self.sut.add_layer(layer_two)
        self.assertEqual(layer_two, self.sut.get_output())


if __name__ == '__main__':
    unittest.main()
