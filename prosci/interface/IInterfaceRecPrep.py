from abc import ABCMeta, abstractmethod

"""An abstract interafce class for preparing the receptor file before docking"""

class IInterfaceRecPrep(object):
    __metaclass__ = ABCMeta
    print "in IInterfaceRecPrep"


    @abstractmethod
    def ArrangeRecInputFormat(self):
	raise NotImplementedError

    @abstractmethod
    def PrepareRec(self):
	raise NotImplementedError



    
