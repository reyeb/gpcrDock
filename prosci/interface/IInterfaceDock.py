from abc import ABCMeta, abstractmethod

class IInterfaceDock(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def Dock(self):
	raise NotImplementedError

