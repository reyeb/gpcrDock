from abc import ABCMeta, abstractmethod

"""An abstract interafce class for preparing the receptor file before docking"""

class IInterfaceRecPrep(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def ArrangeInputFormat(self):
	raise NotImplementedError

    @abstractmethod
    def Prepare(self):
	raise NotImplementedError

##If you define as asbstract u hav to implement it in the main classes if u dion't want to do so just remove @abstractmethod and override it later
    #@abstractmethod
    def BuildGrid(self):
	print "building grid"
	#raise NotImplementedError

    
