from multiprocessing import Pipe, Manager
from multiprocessing import Process

from dframe.pipeline.package import PackageProcessor


class Pipeline(PackageProcessor):
    """Represents a process pipeline made of different processing cores.

    Note: as the pipeline is made of cores, and each of them spawns two processes, the number of processes that this
    pipeline will create is (2*num_cores + 2). The last two are needed for the pipeline itself, one to put the results
    of the last core into the results dictionary (to be able to access them) and the second one is the
    multiprocessing.Manager that holds this shared results dictionary.
    """

    KEY_CLASS = 'class'
    KEY_KWARGS = 'kwargs'

    def __init__(self, core_classes_map):
        """Creates a Pipeline object.

        Args:
            core_classes_map (list[dict]): Each element in the list corresponds to a Core. The element must be a
                dictionary with the key Pipeline.KEY_CLASS and value the class that should be instantiated (the Core
                subclass). You can provide arguments to the constructor using the key Pipeline.KEY_KWARGS.
        """

        self.input_pipe, self.output_pipe = self._construct_pipes(core_classes_map)
        # Instantiate the core classes, connecting them with the created pipes
        self.cores = [core_class[self.KEY_CLASS](**core_class[self.KEY_KWARGS]) for core_class in core_classes_map]
        self.started = False
        self.results_manager = Manager()
        self.results = self.results_manager.dict()
        self.results_producer = PipeConsumer(self.output_pipe, self.results)

    def start(self):
        """Starts the pipeline.

        The pipeline cannot process a package until it has been started. This will start all the core processes.
        """

        for core in self.cores:
            core.start()
        self.results_producer.start()

        self.started = True

    def stop(self, block=True):
        """Stops the pipeline and all its cores smoothly.

        After stopping the pipeline, you need to start it again in order to process more packages.

        Args:
            block (bool): Either if the stop method should be blocking or not. If True, the method will block the
                calling process until all cores are stopped.
        """

        self.input_pipe.send(None)
        if block:
            self.results_producer.join()
        self.started = False

    def terminate(self):
        """Terminates the pipeline and all its cores in a hard way"""

        for core in self.cores:
            # Terminate a core and wait until it finish
            core.terminate()
            core.join()
        self.results_producer.terminate()
        self.results_producer.join()

    def process_package(self, package):
        if not self.started:
            raise EnvironmentError('The pipeline is not ready to process any package. You need to call '
                                   'Pipeline.start() before calling process_package (only the first time)')
        self.input_pipe.send(package)

    def get_result(self, package_id):
        """Returns the resulting package of being processed by the pipeline.

        If it has not finished yet, None is returned.
        """

        return self.results.pop(package_id, None)

    @staticmethod
    def _construct_pipes(core_classes_map):
        """Creates all the pipes needed to connect the cores"""

        # Create the first pipe
        receiver, sender = Pipe(duplex=False)
        # The input pipe of the pipeline is the sender end (introduced the packages to the first core)
        input_pipe = sender

        for core_class in core_classes_map:
            # If no kwargs passed, initialize as empty object
            if Pipeline.KEY_KWARGS not in core_class:
                core_class[Pipeline.KEY_KWARGS] = {}
            # The input pipe of a core is the end that receives packages
            core_class[Pipeline.KEY_KWARGS]['pipe_in'] = receiver
            # Create the inter-core pipe
            receiver, sender = Pipe(duplex=False)
            # The output pipe of a core is the end that sends the result
            core_class[Pipeline.KEY_KWARGS]['pipe_out'] = sender

        # The output pipe of the pipeline is the receiver end of the last core (in order to receive its result)
        output_pipe = receiver
        return input_pipe, output_pipe


class PipeConsumer(Process):
    """Process that is in charge of reading a pipe and putting the incoming packages in a dictionary"""

    def __init__(self, pipe, dictionary):
        super(PipeConsumer, self).__init__()
        self.pipe = pipe
        self.dictionary = dictionary

    def run(self):
        while True:
            try:
                # Wait for the other end of the pipe to send the package and add it to the processing queue
                package = self.pipe.recv()
                # If we receive None, break the infinite loop so that the process dies
                if package is None:
                    break
                # Otherwise add the resulting package in the dictionary with its ID as key
                self.dictionary[package.package_id] = package
            except EOFError:
                break
