from pipeline import *
from prosci.method.GlideRecPrep import *
#from prosci.method.GlideligPrep import *

#Pipeline(GlideRecPrep(),GlideligPrep()).RunPipeline()
class main():
	
	def __init__(self, REC_ADD, LIG_ADD, COMPLEXNAME, OUTDIR, MODE):
		self.rec_Add = REC_ADD
		self.lig_Add = LIG_ADD
		self.complex_Name = COMPLEXNAME
		self.out_Dir = OUTDIR
		self.mode = MODE

	
	def Run_Dock(self):
		
		#if mode==all means run all docking methods
		if self.mode == all:
			run_mode=1
		else:
			run_mode=0
		

		if run_mode ==1 or self.mode == "Glide":
			glideRecPrepInstance=GlideRecPrep(self.rec_Add,self.lig_Add)
			#glideLigPrepInstance=GlideRecPrep(self.rec_Add,self.lig_Add)
			#Pipeline(glideRecPrepInstance,glideLigPrepInstance).RunPipeline()
			Pipeline(glideRecPrepInstance).RunPipeline()

		#if run_mode ==1 or self.mode == "Gold":
			#Pipeline(GoldRecPrep()).RunPipeline()
