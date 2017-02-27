import unittest

from dframe.dataset.sample import CacheValue


class CacheValueTest(unittest.TestCase):
    def test_get_data_with_cache_should_cache_it(self):
        data = 'data'
        sut = DummyCacheValue(data, cache=True)
        sut.get_data()
        self.assertEqual(data, sut._cached_data)

    def test_get_data_without_cache_should_not_cache_it(self):
        data = 'data'
        sut = DummyCacheValue(data, cache=False)
        sut.get_data()
        self.assertIsNone(sut._cached_data)


class DummyCacheValue(CacheValue):
    def __init__(self, data, cache=True):
        super(DummyCacheValue, self).__init__(cache)
        self.data = data

    @CacheValue.cache_data
    def get_data(self):
        return self.data


if __name__ == '__main__':
    unittest.main()
