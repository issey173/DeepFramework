import unittest

from multiprocessing import Queue, Pipe

import time

from dframe.pipeline.core import PipeConsumer


class PipeConsumerTest(unittest.TestCase):
    def test_run(self):
        # Create Queue and pipe
        queue = Queue()
        pipe_in, pipe_out = Pipe(duplex=False)
        # Create and start Producer
        self.sut = PipeConsumer(pipe_in, queue)
        self.sut.start()
        # Send package and assert that the producer has put the package in the queue
        package = 'package'
        pipe_out.send(package)
        time.sleep(1)
        self.assertEqual(package, queue.get())
        # Send poison pill and exit
        pipe_out.send(None)
        self.sut.join()


if __name__ == '__main__':
    unittest.main()
