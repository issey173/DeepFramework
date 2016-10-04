import os
import unittest

import h5py

from dframe.dataset.dataset import Dataset
from dframe.dataset.persistence import H5pyPersistenceManager
from dframe.dataset.sample import Sample


class H5pyPersistenceManagerTest(unittest.TestCase):
    def setUp(self):
        self.sut = H5pyPersistenceManager()
        self.file_path = '/vagrant/tests/dataset/test.h5'

    def tearDown(self):
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)

    # ----------------------- Save ---------------------------
    def test_save_given_non_dataset_should_raise_exception(self):
        self.assertRaises(TypeError, self.sut.save, 'non dataset')

    def test_save_given_dataset_without_output_should_persist_input(self):
        dataset = Dataset([Sample([1, 2]), Sample([3, 4])])
        self.sut.save(dataset, self.file_path)
        with h5py.File(self.file_path, 'r') as f:
            self.assertIn(H5pyPersistenceManager.INPUT_DATASET_NAME, f)
            self.assertNotIn(H5pyPersistenceManager.OUTPUT_DATASET_NAME, f)

    def test_save_given_dataset_with_input_output_should_persist_both(self):
        dataset = Dataset([Sample([1, 2], 1), Sample([3, 4], 3)])
        self.sut.save(dataset, self.file_path)
        with h5py.File(self.file_path, 'r') as f:
            self.assertIn(H5pyPersistenceManager.INPUT_DATASET_NAME, f)
            self.assertIn(H5pyPersistenceManager.OUTPUT_DATASET_NAME, f)

    # ----------------------- Load ---------------------------
    def test_load_given_unexisting_path_should_raise_exception(self):
        self.assertRaises(TypeError, self.sut.load)

    def test_load_given_existing_path_with_non_outputs_should_return_dataset_without_outputs(self):
        inputs = [[1, 2], [3, 4]]
        with h5py.File(self.file_path, 'w') as f:
            f.create_dataset(H5pyPersistenceManager.INPUT_DATASET_NAME, data=inputs)

        dataset = self.sut.load(self.file_path)
        self.assertIsInstance(dataset, Dataset)
        self.assertTrue(dataset.len() == 2)
        self.assertRaises(TypeError, dataset.get_output)

    def test_load_given_existing_path_wit_input_output_should_return_dataset(self):
        inputs = [[1, 2], [3, 4]]
        outputs = [[1], [3]]
        with h5py.File(self.file_path, 'w') as f:
            f.create_dataset(H5pyPersistenceManager.INPUT_DATASET_NAME, data=inputs)
            f.create_dataset(H5pyPersistenceManager.OUTPUT_DATASET_NAME, data=outputs)

        dataset = self.sut.load(self.file_path)
        self.assertIsInstance(dataset, Dataset)
        self.assertTrue(dataset.len() == 2)


if __name__ == '__main__':
    unittest.main()
