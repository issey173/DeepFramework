import unittest

from multiprocessing import Queue, Pipe

from dframe.pipeline.core import Producer


class ProducerTest(unittest.TestCase):
    def test_run(self):
        # Create Queue and pipe
        queue = Queue()
        pipe_in, pipe_out = Pipe(duplex=False)
        # Create and start Producer
        self.sut = Producer(pipe_in, queue)
        self.sut.start()
        # Send package and assert that the producer has put the package in the queue
        package = 'package'
        pipe_out.send(package)
        self.assertEqual(package, queue.get())
        # Send poison pill and exit
        pipe_out.send(None)
        self.sut.join()


if __name__ == '__main__':
    unittest.main()
