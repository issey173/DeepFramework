from abc import ABCMeta, abstractmethod


class Input(metaclass=ABCMeta):
    """Interface like class for all the classes that are meant to be an input"""

    def __init__(self):
        pass

    @abstractmethod
    def get_input(self): pass


class Output(metaclass=ABCMeta):
    """Interface like class for all the classes that are meant to be an output"""

    def __init__(self):
        pass

    @abstractmethod
    def get_output(self): pass
