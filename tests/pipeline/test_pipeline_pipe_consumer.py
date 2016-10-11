import unittest

from multiprocessing import Pipe, Manager

import time

from dframe.pipeline.package import Package
from dframe.pipeline.pipeline import PipeConsumer


class PipeConsumerTest(unittest.TestCase):
    def test_run(self):
        # Create dictionary and pipe
        dictionary = Manager().dict()
        pipe_in, pipe_out = Pipe(duplex=False)
        # Create and start Producer
        self.sut = PipeConsumer(pipe_in, dictionary)
        self.sut.start()
        # Send package and assert that the producer has put the package in the queue
        package = Package(package_id=1)
        pipe_out.send(package)
        time.sleep(1)
        print dictionary
        self.assertEqual(package.package_id, dictionary[1].package_id)
        # Send poison pill and exit
        pipe_out.send(None)
        self.sut.join()


if __name__ == '__main__':
    unittest.main()
