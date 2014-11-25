from prosci.interface.IInterfaceRecPrep import *
from prosci.util.command import *
from prosci.util.common import *
import os,sys
from prosci.util.cd import *
import traceback

from prosci.method.GlideRecPrep import *
from prosci.method.DockParams import DockParams

"""all these have a process class which does the pipeline in the class itself"""

class GoldRecPrep(IInterfaceRecPrep):

    def __init__(self, REC_ADD, LIG_ADD, OUTDIR, GRIDPointList):
	self.rec_Add = REC_ADD
	self.lig_Add = LIG_ADD
	self.ouPutDir =OUTDIR
	#Let's have grid point as a list since in future we might have more of a pocket detection which will be added here
	self.gridPoints = GRIDPointList
	self.Program_path = Command().Get_program_path("maestro").replace("maestro","")
	#self.gridZipAdd = []

    def Process(self):

	try:
		
		print "prepare receptor"
		self.ArrangeRecInputFormat()
		self.PrepareRec()

	except Exception, err:
    		try:
        		exc_info = sys.exc_info()
       		except:
            		pass
    		finally:
			print "Display the *original* exception"
			traceback.print_exception(*exc_info)
			del exc_info

    def ArrangeRecInputFormat(self):

	#if Glide has run previously and the prepered receptor is still available use that else re_run that and in both cases converet the files to the .mol2 format	
	if DockParams.glideRecAdd is not None and os.path.exists(DockParams.glideRecAdd):
		pass
	else:	
		#re_run and save in the glide folder
		glideRecPrepInstance = GlideRecPrep(self.rec_Add,self.lig_Add, glideoutDir,self.gridPoints)
		DockParams.glideRecAdd = glideRecPrepInstance.ArrangeRecInputFormat()
		
	DockParams.GoldRecAdd = self.ChangeFormattoMol2()


    def ChangeFormattoMol2(self):
	"""Change ligand format from pdb to mae. Command e.g. $SCHRODINGER/utilities/structconvert -imae gold_5HT2B_1106_0001_receptor_prep.mae -omol2 gold_5HT2B_1106_0001_lreceptor_prep.mol2"""
	
        mainExecutablePath = os.path.join(self.Program_path,"utilities/structconvert")
	outputLigName = FileManager().changeExtention(os.path.basename(DockParams.glideRecAdd),".mol2")
	outputFile = os.path.join(self.ouPutDir,outputLigName)
	
	#if the file is already there just return its address
	if os.path.exists(outputFile):
		return outputFile
	
	with cd (self.ouPutDir): 
		arguments=[mainExecutablePath,"-imae", DockParams.glideRecAdd , "-omol2", outputLigName]
		
		Command().Process_Command(arguments," ", "Converting ligand format to mol2.")
	return outputFile
	
    def PrepareRec(self):
    	return 0

    
