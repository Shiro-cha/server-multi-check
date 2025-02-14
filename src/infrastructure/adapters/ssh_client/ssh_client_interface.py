import abc


class SSHClientInterface(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def connect(selft, host,port,user,password):
        """Establishes a connection to the host"""
        pass

    @abc.abstractmethod
    def close(self):
        """Closes the connection"""
        pass