from prosci.method.DockParams import DockParams


class Pipeline(object):

    def __init__(self, RECPREP, LIGPREP = None, DOCK = None):
	self._recPrep = RECPREP
	self._ligPrep = LIGPREP	
	self._dock = DOCK

    def RunPipeline(self):
	
	self._recPrep.Process()
	if self._ligPrep:
		self._ligPrep.Process()
	#print "lig address", self._ligPrep.prepareLigAdd
	
	#RE_INITIALISE TO UPDATE THE DOCKPARAMS IN THE NEW INSANTIATION. BECAUSE IN MAIN.PY WHEN WE INSTANTIATED DOCK WE USED THE DOCKPARAMS CLASS WHICH WAS NOT UPDATED AFTER RECEPTOR AND LIGAND PREPERATION (Not anymore since the Dockparam is a treated as static)
	#self._dock.__new__(DockParams)
	import time
	start_time = time.time()
	if self._dock:
		self._dock.Dock()
	print("--- %s seconds ---" % str(time.time() - start_time))

