from prosci.interface.IInterfaceLigPrep import *
from prosci.util.command import *
from prosci.util.common import *
from prosci.util.cd import *
import os


class GlideLigPrep(IInterfaceLigPrep):


    def __init__(self, LIG_ADD, OUTDIR, GRIDPointList):

	self.lig_Add = LIG_ADD
	self.ouPutDir =OUTDIR
	self.Program_path = Command().Get_program_path("maestro").replace("maestro","")

	self.preparedLigAdd = ""


    def Process(self):
	
	if not self.lig_Add.endswith("mae"):
		self.ArrangeLigInputFormat()

    def ArrangeLigInputFormat(self):
	"""Change ligand format from pdb to mae"""
	#$SCHRODINGER/utilities/structconvert -ipdb 5HT2B_1106_0001_ligand.pdb -omae 5HT2B_1106_0001_ligand.mae
        mainExecutablePath = os.path.join(self.Program_path,"utilities/structconvert")
	outputLigName = FileManager().changeExtention(os.path.basename(self.lig_Add),".mae")
	outputFile = os.path.join(self.ouPutDir,outputlLgName)
	arguments=[mainExecutablePath,"-ipdb", self.ligAdd, "-omae", outputFile]
	commandLine =" ".join(arguments)
	print commandLine
	return outputFile


    def PrepareLig (self, ligmaeFormat):
	"""Change ligand format from pdb to mae"""
	#$SCHRODINGER/ligprep -WAIT -W e,-ph,7.0,-pht,2.0 -epik -i 1 -r 1 -nz -bff 14 -ac -imae 5HT2B_1106_0001_ligand.mae -omae 5HT2B_1106_0001_ligand_prep.mae

        mainExecutablePath = os.path.join(self.Program_path,"SCHRODINGER/ligprep")
	outputLigName = FileManager().changeExtention(os.path.basename(self.lig_Add),"_Prep.mae")
	outputFile = os.path.join(self.ouPutDir,outputlLgName)
	arguments=[mainExecutablePath,"-WAIT -W e,-ph,7.0,-pht,2.0 -epik -i 1 -r 1 -nz -bff 14 -ac",  "-imae", ligmaeFormat, "-omae", outputFile]
	commandLine =" ".join(arguments)
	self.prepareLigAdd = outputFile
	#print commandLine
