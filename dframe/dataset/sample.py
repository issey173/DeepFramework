from abc import ABCMeta, abstractmethod


# noinspection PyClassHasNoInit
class Input:
    """Interface like class for all the classes that are meant to be an input"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_input(self): pass


# noinspection PyClassHasNoInit
class Output:
    """Interface like class for all the classes that are meant to be an output"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_output(self): pass
