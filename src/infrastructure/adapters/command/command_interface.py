import abc

class CommandeInterface(object):
    
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def execute(self, command):
        """Executes a command in the host"""
        pass