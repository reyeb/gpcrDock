from abc import ABCMeta, abstractmethod

class IInterfaceLigPrep(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def ArrangeLigInputFormat(self):
	raise NotImplementedError

    @abstractmethod
    def PrepareLig(self):
	raise NotImplementedError


    #@abstractmethod
    #def prepareLigand(self): raise NotImplementedError
