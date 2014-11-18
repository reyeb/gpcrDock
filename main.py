from pipeline import *
from prosci.method.GlideRecPrep import *
from prosci.method.GridDetector import *
from prosci.method.GlideLigPrep import *
from prosci.method.GlideDock import *
from prosci.method.DockParams import DockParams


#Pipeline(GlideRecPrep(),GlideligPrep()).RunPipeline()
class main():
	
    def __init__(self, REC_ADD, LIG_ADD, COMPLEXNAME, OUTDIR, MODE):
	self.rec_Add = REC_ADD
	self.lig_Add = LIG_ADD
	self.complex_Name = COMPLEXNAME
	self.out_Dir = OUTDIR
	self.mode = MODE
	#Let's have grid point as a list since in future we might have more of a pocket detection which will be added here
	self.gridPoints = GridDetector(LIG_ADD).BuildGridUsingLigandPositionAverage()

	
    def Run_Dock(self):
		
	#if mode==all means run all docking methods
	if self.mode == 'all':
		run_mode=1
	else:
		run_mode=0
		
	
	if run_mode ==1 or self.mode == "Glide":
		#prepare output dir. build here since lig and rest will need it
		glideoutDir = FileManager().BuildDirectory(self.out_Dir,["Glide",self.complex_Name])
		glideRecPrepInstance = GlideRecPrep(self.rec_Add,self.lig_Add, glideoutDir,self.gridPoints)
		glideLigPrepInstance = GlideLigPrep(self.lig_Add,glideoutDir)
		glideDockInstance = GlideDock()
		Pipeline(glideRecPrepInstance, glideLigPrepInstance, glideDockInstance).RunPipeline()
		#Pipeline(glideRecPrepInstance).RunPipeline()

	if run_mode ==1 or self.mode == "Gold":
		Pipeline(GoldRecPrep()).RunPipeline()


