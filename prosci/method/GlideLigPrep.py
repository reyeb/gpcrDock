from prosci.interface.IInterfaceLigPrep import *
from prosci.util.command import *
from prosci.util.common import *
from prosci.util.cd import *

import os

from prosci.method.DockParams import DockParams

class GlideLigPrep(IInterfaceLigPrep):


    def __init__(self, LIG_ADD, OUTDIR):

	self.lig_Add = LIG_ADD
	self.ouPutDir =OUTDIR
	self.Program_path = Command().Get_program_path("maestro").replace("maestro","")

    def Process(self):
	
	try:
		print "prepare ligand"
		#if not self.lig_Add.endswith("mae"):
		formated_ligand = self.ArrangeLigInputFormat()
		DockParams.glideLigAdd = self.PrepareLig(formated_ligand)
	except  Exception,err:
		raise Exception('failed to process ligand',str(err))

    def ArrangeLigInputFormat(self):
	"""Change ligand format from pdb to mae. Command e.g. $SCHRODINGER/utilities/structconvert -ipdb 5HT2B_1106_0001_ligand.pdb -omae 5HT2B_1106_0001_ligand.mae"""
	
        mainExecutablePath = os.path.join(self.Program_path,"utilities/structconvert")
	outputLigName = FileManager().changeExtention(os.path.basename(self.lig_Add),".mae")
	outputFile = os.path.join(self.ouPutDir,outputLigName)
	with cd (self.ouPutDir): 
		arguments=[mainExecutablePath,"-ipdb", self.lig_Add , "-omae", outputLigName]
		Command().Process_Command(arguments," ", "Converting ligand format to mae.")
	return outputFile


    def PrepareLig (self, ligmaeFormat):
	"""Change ligand format from pdb to mae. Command eg. $SCHRODINGER/ligprep -WAIT -W e,-ph,7.0,-pht,2.0 -epik -i 1 -r 1 -nz -bff 14 -ac -imae 5HT2B_1106_0001_ligand.mae -omae 5HT2B_1106_0001_ligand_prep.mae"""

        mainExecutablePath = os.path.join(self.Program_path,"ligprep")
	outputLigName = FileManager().changeExtention(os.path.basename(self.lig_Add),"_Prep.mae")
	outputFile = os.path.join(self.ouPutDir,outputLigName)
	with cd (self.ouPutDir): 
		arguments=[mainExecutablePath,"-WAIT -W e,-ph,7.0,-pht,2.0 -epik -s 1 -i 1 -r 1 -nz -bff 14 -ac",  "-imae", ligmaeFormat, "-omae", outputLigName]
		Command().Process_Command(arguments," ", "Preparing Ligand input.")
		###not delet anything
		#FileManager().Delete_unwanted_dirs_basedon_Extention (fileExtention_to_keep = "_Prep.mae" , mainDir =self.ouPutDir )
	return outputFile
