from multiprocessing import Queue, Process

from abc import ABCMeta

from dframe.pipeline.package import PackageProcessor


class Core(Process, PackageProcessor):
    """Processing unit.

    As Core is an abstract class, the actual logic to process the package must be implemented extending it and
    overriding the process_package method defined in dframe.pipeline.package.PackageProcessor, which Core extends from.
    The run method only deals with getting the package, delivering it to process_package and sending the result through
    the output pipe, and thus it should commonly remain untouched (not overrided)
    """

    __metaclass__ = ABCMeta

    def __init__(self, pipe_in, pipe_out):
        super(Core, self).__init__()
        self.queue = Queue()        # FIFO queue
        self.pipe_in = pipe_in      # The input channel. Package get into the core through this pipe
        self.pipe_out = pipe_out    # The output channel. The core send the result through this pipe

        # Child process that listens for incoming packages through pipe_in and adds them to the processing queue.
        # From the Core perspective, this is the producer of packages (the one that puts them in the processing queue)
        self.producer = PipeConsumer(self.pipe_in, self.queue)

    def start(self):
        # Start the producer process before starting this one
        self.producer.start()
        super(Core, self).start()

    def terminate(self):
        """Terminates the core's execution processes.

        This method calls the terminate method to the underlaying processes, which are not 'safe' and can lead to
        corrupted pipes and unprocessed packages. In order to safely stop the core, inject None (poison pill) through
        its input pipe. This will stop smoothly the core and will propagate the signal.
        """

        # Terminate the producer process and wait until it has completely finished
        self.producer.terminate()
        self.producer.join()
        # Terminate self process
        super(Core, self).terminate()

    def run(self):
        """Logic of the core is executed here in a different process.

        This is the consumer part of the architecture. Packages are caught from the processing queue, processed and
        sent to the next module through the output pipe.
        """

        while True:
            # Get the next package to process from the queue. Blocking if there is none
            package = self.queue.get()
            # If we receive None, propagate the signal through the pipe and break the infinite loop to stop
            # the process
            if package is None:
                self.pipe_out.send(package)
                break
            # Process the package
            self.process_package(package)
            # Send the result to the next block through the output pipe
            self.pipe_out.send(package)


class PipeConsumer(Process):
    """Process that is in charge of reading a pipe and putting the incoming packages in a queue"""

    def __init__(self, pipe, queue):
        super(PipeConsumer, self).__init__()
        self.pipe = pipe
        self.queue = queue

    def run(self):
        while True:
            try:
                # Wait for the other end of the pipe to send the package and add it to the processing queue
                package = self.pipe.recv()
                self.queue.put(package)
                # If we receive None, break the infinite loop so that the process dies
                if package is None:
                    break
            except EOFError:
                break
