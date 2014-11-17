
class Pipeline(object):

    def __init__(self, RECPREP, LIGPREP):
	self._recPrep = RECPREP
	self._ligPrep= LIGPREP	

    def RunPipeline(self):
	
	self._recPrep.Process()
	print "zzip files",  self._recPrep.gridZipAdd
	self._ligPrep.Process()
	print "lig address", self._ligPrep.prepareLigAdd
