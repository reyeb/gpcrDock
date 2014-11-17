from prosci.interface.IInterfaceDock import *

class GlideDock(IInterfaceDock):
	

    def __init__(self, LIG_ADD, GRID_Files_List):

	self.lig_Add = LIG_ADD
	self.ouPutDir =OUTDIR
	self.Program_path = Command().Get_program_path("maestro").replace("maestro","")


    def Dock(self):
	 
	

