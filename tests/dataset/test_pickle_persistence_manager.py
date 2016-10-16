import cPickle
import os
import unittest

from dframe.dataset.dataset import Dataset
from dframe.dataset.persistence import PicklePersistenceManager
from dframe.dataset.sample import Sample


class PicklePersistenceManagerTest(unittest.TestCase):
    def setUp(self):
        self.sut = PicklePersistenceManager()
        self.file_path = './test.p'

    def tearDown(self):
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)

    # ----------------------- Save ---------------------------

    def test_save_given_non_dataset_should_raise_exception(self):
        self.assertRaises(TypeError, self.sut.save, 'non dataset')

    def test_save_given_dataset_should_persist_it(self):
        dataset = Dataset([Sample([1, 2]), Sample([3, 4])])
        self.sut.save(dataset, self.file_path)
        with open(self.file_path) as f:
            d = cPickle.load(f)
            self.assertIsInstance(d, Dataset)

    # ----------------------- Load ---------------------------
    def test_load_given_unexisting_path_should_raise_exception(self):
        self.assertRaises(TypeError, self.sut.load)

    def test_load_given_existing_path_should_return_dataset(self):
        with open(self.file_path, 'w') as f:
            cPickle.dump(Dataset([Sample([1, 2]), Sample([3, 4])]), f)
        dataset = self.sut.load(self.file_path)
        self.assertIsInstance(dataset, Dataset)
        self.assertTrue(dataset.len() == 2)


if __name__ == '__main__':
    unittest.main()
