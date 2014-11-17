from prosci.interface.IInterfaceRecPrep import *
from prosci.util.command import *
from prosci.util.common import *
import os
from prosci.util.cd import *

"""all these have a process class which does the pipeline in the class itself"""

class GlideRecPrep(IInterfaceRecPrep):
    print "in GlideRecPrep"




    def __init__(self, REC_ADD, LIG_ADD, OUTDIR, GRIDPointList):
	self.rec_Add = REC_ADD
	self.lig_Add = LIG_ADD
	self.ouPutDir =OUTDIR
	
	
	#Let's have grid point as a list since in future we might have more of a pocket detection which will be added here
	self.gridPoints = GRIDPointList
	
	self.Program_path = Command().Get_program_path("maestro").replace("maestro","")
	self.gridZipAdd = []






    def Process(self):
	print "the main pipeline happens here for Glide"
	if not self.rec_Add.endswith("mae"):
		self.ArrangeRecInputFormat()
	#self.PrepareRec()

    def ArrangeRecInputFormat(self):
	
	#$SCHRODINGER/utilities/prepwizard -WAIT -fix 5HT2B_1106_0001_receptor.pdb 5HT2B_1106_0001_receptor_prep.mae
        mainExecutablePath = os.path.join(self.Program_path,"utilities/prepwizard")
	outputRecName = FileManager().changeExtention(os.path.basename(self.rec_Add),"_Prep.mae")
	self.prep_receptor_file = os.path.join(self.ouPutDir,outputRecName)
	arguments=[mainExecutablePath,"-WAIT","-fix", self.rec_Add, self.prep_receptor_file]
	commandLine =" ".join(arguments)
	print commandLine
        #error:#prepwizard_startup.py: error: Error: output file must be relative path: /home/t701033/data/docking/test/Glide/5HT2B_1106_0001/5HT2B_1106_0001_receptor_Prep.mae


	#currentWorkingDir = os.path.dirname(os.path.realpath(__file__))
	#print os.getcwd()
        #print os.path.commonprefix([os.getcwd(),outputFile])
	#Command.Process_Command(commandLine)
	#../../docking/test/Glide/5HT2B_1106_0001/


    def PrepareRec(self):
	
    	grid_command="""
USECOMPMAE YES
INNERBOX 10, 10, 10
ACTXRANGE 30.000000
ACTYRANGE 30.000000
ACTZRANGE 30.000000
GRID_CENTER {1}
OUTERBOX 30.000000, 30.000000, 30.000000
GRIDFILE {2}.zip
RECEP_FILE {3}"""

	index=1

        folderName="grid "+ str(index)
	for center in self.gridPoints:
		center_str =" ".join(center)
		ouputpath_grid = os.path.join(self.ouPutDir ,self.prep_receptor_file)
   		with cd ("s"): 
			grid_command.format(center_str, ouputpath_grid, self.prep_receptor_file )
		index = index+1
		self.gridZipAdd.append(ouputpath_grid)



    
