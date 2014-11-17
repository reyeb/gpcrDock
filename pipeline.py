
class Pipeline(object):

    def __init__(self, RECPREP, LIGPREP=None):
	self._recPrep = RECPREP
	#self._ligPrep= LIGPREP	

    def RunPipeline(self):
	#print "running pipeline"
	self._recPrep.Process()
	#print "new add",  self._recPrep.gridZipAdd
	#self._ligPrep.process()
