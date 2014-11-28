from prosci.interface.IInterfaceDock import *
from prosci.method.DockParams import DockParams
from prosci.util.command import *
from prosci.util.common import *
import ntpath
from prosci.util.cd import *

class GoldDock(IInterfaceDock):

    def __init__(self,OUTDIR, GRIDPointList):
	self.gridPoints = GRIDPointList
	self.ouPutDir = OUTDIR
	self.Program_path = Command().Get_program_path("gold_auto")
	#print "self.Program_path",self.Program_path

    def Dock(self):
	print "start Docking"
	#current_working_path = os.path.dirname(os.path.realpath(__file__))
	self.DockLigRec()
	
    def DockLigRec(self):
	
	current_working_path = os.path.dirname(os.path.realpath(__file__))
	
	#for each grid point do Gold dock
	with open (os.path.join(current_working_path,"goldDockCommandTemplate.conf")) as f:
		command_str = f.read()
#grid point
#ligand file
#howmanytimesdockligand
#directory
#ouputname: 5HT2B_1106_0001.mol2
#docking_fitfunc_path = {5}
#rescore_fitfunc_path = {6}Goldscore
#recpetor path	
	for index,center in enumerate(self.gridPoints):
		center_str =" ".join(center)
		#print center_str
		gridName = "grid"+ str(index+1)
		ouputpath_grid = os.path.join(self.ouPutDir ,gridName)
		output_Docked_models=os.path.join(ouputpath_grid,"FinalModels_"+str(index+1)+".mol2")
		#print ouputpath_grid
		if not os.path.exists(ouputpath_grid):
			os.mkdir(ouputpath_grid)
		cur_goldcommand = command_str.format(center_str, DockParams.GoldLigAdd, "10", ouputpath_grid,output_Docked_models,"goldscore","plp", DockParams.GoldRecAdd)
		
		new_conf_file_path= os.path.join(ouputpath_grid, "conf_grid"+str(index+1)+".conf")
   		with cd (ouputpath_grid): 
			with open (new_conf_file_path,"w") as f:
				f.write(cur_goldcommand)
			arguments=[self.Program_path,new_conf_file_path]
			#Command().Process_Command(arguments," ", "Dock Gold for "+gridName)
			FileManager().Delete_unwantedfiles_by_pattern(ouputpath_grid, pattern="ranked_.+\.sdf")


