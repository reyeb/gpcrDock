from prosci.interface.IInterfaceRecPrep import *
from prosci.util.command import *
from prosci.util.common import *
import os,sys
from prosci.util.cd import *
import traceback

from prosci.method.DockParams import DockParams

"""all these have a process class which does the pipeline in the class itself"""

class GlideRecPrep(IInterfaceRecPrep):

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
		print "Prepare Receptor"
		DockParams.glideRecAdd = self.ArrangeRecInputFormat()
		DockParams.glidegridZipAdds = self.PrepareRec()
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
	
	"""Prepares the receptor and saves it as .mae file format.command eg. $SCHRODINGER/utilities/prepwizard -WAIT -fix 5HT2B_1106_0001_receptor.pdb 5HT2B_1106_0001_receptor_prep.mae"""
	
        mainExecutablePath = os.path.join(self.Program_path,"utilities/prepwizard")
	outputRecName = FileManager().changeExtention(os.path.basename(self.rec_Add),"_Prep.mae")
	self.prep_receptor_file = os.path.join(self.ouPutDir,outputRecName)
	#print os.getcwd()
	# outside the context manager we are back wherever we started.
	with cd (self.ouPutDir): 
		arguments=[mainExecutablePath,"-WAIT","-fix", self.rec_Add, outputRecName]
		Command().Process_Command(arguments," ","Preparing Receptror input.")
		###not delet anything
		#FileManager().Delete_unwanted_dirs_basedon_Names(mainDir = self.ouPutDir , files_to_keep = [outputRecName])
	return os.path.join(self.ouPutDir, outputRecName)

    def PrepareRec(self):
	
	"""Prepares the grid points on the receptor. To do so for ecah grid point we should create a gridX.in file (X: is an index which ciorresponds to the number of grid points) .command eg.$SCHRODINGER/glide -WAIT grid.in"""

    	grid_command="""
USECOMPMAE YES
INNERBOX 10, 10, 10
ACTXRANGE 30.000000
ACTYRANGE 30.000000
ACTZRANGE 30.000000
GRID_CENTER {0}
OUTERBOX 30.000000, 30.000000, 30.000000
GRIDFILE {1}.zip
RECEP_FILE {2}"""
	mainExecutablePath = os.path.join(self.Program_path,"glide")
	index=1
	gridZipAdd = []
        gridName = "grid"+ str(index)
	for center in self.gridPoints:
		center_str =", ".join(center)
		ouputpath_grid = os.path.join(self.ouPutDir ,gridName)
		if not os.path.exists(ouputpath_grid ):
			os.mkdir(ouputpath_grid)

   		with cd (ouputpath_grid): 
			cur_gridcommand = grid_command.format(center_str, gridName,  self.prep_receptor_file)
			with open (gridName+".in", "w") as f:
				f.write(cur_gridcommand)
			arguments=[mainExecutablePath,"-WAIT", gridName+".in"]
			Command().Process_Command(arguments," ","Preparing grid point "+str(index))

			index = index+1
			gridZipAdd.append(os.path.join(ouputpath_grid,gridName+".zip"))
	return gridZipAdd



    
