from prosci.interface.IInterfaceRecPrep import *
from prosci.util.command import *
from prosci.util.common import *
import os,sys
from prosci.util.cd import *
import traceback

from prosci.method.GlideRecPrep import *
from prosci.method.DockParams import DockParams

"""all these have a process class which does the pipeline in the class itself"""

class VinaRecPrep(IInterfaceRecPrep):

    def __init__(self, REC_ADD, LIG_ADD, OUTDIR, GRIDPointList):
	self.rec_Add = REC_ADD
	self.lig_Add = LIG_ADD
	self.ouPutDir =OUTDIR
	#Let's have grid point as a list since in future we might have more of a pocket detection which will be added here
	self.gridPoints = GRIDPointList

    def Process(self):

	try:
		
		print "prepare receptor"
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

	#return outputFile
	
    def PrepareRec(self):
	"""prepare receptor "python prepare_receptor4.py -r 5HT1B_2683_0001_receptor.pdb -o recprepe.pdbqt -A checkhydrogens" #The script is in: /opt/local/mgltools/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py """
	outputRecName = FileManager().changeExtention(os.path.basename(self.rec_Add),"_Prep.pdbqt")
	mainExecutablePath="/opt/local/mgltools/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py"
	self.prep_receptor_file = os.path.join(self.ouPutDir,outputRecName)
	with cd (self.ouPutDir): 
		print self.ouPutDir
		arguments=["python",mainExecutablePath,"-r", self.rec_Add, "-o",outputRecName,"-A","checkhydrogens"]
		commandLine=" ".join(arguments)
		os.system(commandLine)
	DockParams.VinaRecAdd=os.path.join(self.ouPutDir, outputRecName)

    def ArrangeRecInputFormat(self):
	return 0

    
