from abc import ABCMeta, abstractmethod

class IInterfaceB(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def prepareLigand(self):
	raise NotImplementedError
    #@abstractmethod
    #def prepareLigand(self): raise NotImplementedError
