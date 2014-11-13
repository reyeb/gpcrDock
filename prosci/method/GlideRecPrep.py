from prosci.interface.IInterfaceRecPrep import *
from prosci.util.command import *
from prosci.util.common.FileManager import BuildDirectory,changeExtention
"""all these have a process class which does the pipeline in the class itself"""

class GlideRecPrep(IInterfaceRecPrep):

    def __init__(self, REC_ADD, LIG_ADD, OUTDIR):
	self.rec_Add = REC_ADD
	self.lig_Add = LIG_ADD
	self.Program_path = Command().Get_program_path("maestro").replace("maestro","SCHRODINGER")
	self.BuildOutputDir(OUTDIR)

    def Process(self):
	print "the main pipeline happens here for Glide"
	#self.ArrangeInputFormat()

    def ArrangeInputFormat(self):
	print "preepare input"
	#$SCHRODINGER/utilities/prepwizard -WAIT -fix 5HT2B_1106_0001_receptor.pdb 5HT2B_1106_0001_receptor_prep.mae
        mainpath = os.path.join(self.Program_path,"utilities/prepwizard")
	#arguments=["-WAIT","-fix"]
	#commandLine =" ".join(mainpath,)
	#Commadn.Process_Command(commandLine)
	


    def Prepare(self):
	print "preparing rec"


    def BuildGrid(self):
	print "overriding grid"

    
