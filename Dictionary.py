import abc

class Dictionary(object):
    __metaclass__ = abc.ABCMeta

    """Look up an array of word"""
    @abc.abstractmethod
    def lookup(words):
        return
