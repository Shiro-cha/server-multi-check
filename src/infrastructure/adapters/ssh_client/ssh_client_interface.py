from abc import ABCMeta, abstractmethod


class SSHClientInterface(ABCMeta):
    __metaclass__ = ABCMeta

    @abstractmethod
    def connect(selft, host,port,user,password):
        """Establishes a connection to the host"""
        pass

    @abstractmethod
    def close(self):
        """Closes the connection"""
        pass