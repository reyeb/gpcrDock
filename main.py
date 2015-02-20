from pipeline import *
from prosci.method.GridDetector import *
from prosci.method.DockParams import DockParams

#for Glide
from prosci.method.GlideLigPrep import *
from prosci.method.GlideRecPrep import *
from prosci.method.GlideDock import *

#for Gold
from prosci.method.GoldRecPrep import *
from prosci.method.GoldLigPrep import *
from prosci.method.GoldDock import *



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
		print "***Running Glide ...."
		#prepare output dir. build here since lig and rest will need it
		glideoutDir = FileManager().BuildDirectory(self.out_Dir,["Glide",self.complex_Name])
		glideRecPrepInstance = GlideRecPrep(self.rec_Add,self.lig_Add, glideoutDir,self.gridPoints)
		glideLigPrepInstance = GlideLigPrep(self.lig_Add,glideoutDir)
		glideDockInstance = GlideDock()
		Pipeline(glideRecPrepInstance, glideLigPrepInstance, glideDockInstance).RunPipeline()
		#Pipeline(glideRecPrepInstance).RunPipeline()

	if run_mode ==1 or self.mode == "Gold":
		print "***Running Gold ....."
		goldoutDir = FileManager().BuildDirectory(self.out_Dir,["Gold",self.complex_Name])
		goldRecPrepInstance = GoldRecPrep(self.rec_Add,self.lig_Add, goldoutDir,self.gridPoints)
		goldLigPrepInstance = GoldLigPrep(self.lig_Add,goldoutDir)
		goldDockInstance = GoldDock(goldoutDir,self.gridPoints)
		Pipeline(goldRecPrepInstance,goldLigPrepInstance,goldDockInstance).RunPipeline()


