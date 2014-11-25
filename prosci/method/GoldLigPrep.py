from prosci.interface.IInterfaceLigPrep import *
from prosci.util.command import *
from prosci.util.common import *
from prosci.util.cd import *

import os

from prosci.method.DockParams import DockParams

class GoldLigPrep(IInterfaceLigPrep):


    def __init__(self, LIG_ADD, OUTDIR):
	
	self.lig_Add = LIG_ADD
	self.ouPutDir =OUTDIR
	self.Program_path = Command().Get_program_path("maestro").replace("maestro","")

    def Process(self):
	
	try:
		#if not self.lig_Add.endswith("mae"):
		print "prepare ligand"
		formated_ligand = self.ArrangeLigInputFormat(self.lig_Add,"pdb","mae")
		prepered_glide_lig_add = self.PrepareLig(formated_ligand)
		#print "prepered_glide_lig_add",prepered_glide_lig_add
		DockParams.GoldLigAdd = self.ArrangeLigInputFormat(prepered_glide_lig_add ,"mae","mol2")
		#print "DockParams.GoldLigAdd",DockParams.GoldLigAdd
	except  Exception,err:
		raise Exception('failed to process ligand',str(err))

    def ArrangeLigInputFormat(self, input_protein_Add,input_extention,output_extention):
	"""Change ligand format from pdb to mae. Command e.g. $SCHRODINGER/utilities/structconvert -ipdb 5HT2B_1106_0001_ligand.pdb -omae 5HT2B_1106_0001_ligand.mae"""
	
        mainExecutablePath = os.path.join(self.Program_path,"utilities/structconvert")
	outputLigName = FileManager().changeExtention(os.path.basename(input_protein_Add),"."+output_extention)
	outputFile = os.path.join(self.ouPutDir,outputLigName)
	
	#if the file is already there just return its address
	if os.path.exists(outputFile):
		return outputFile
		
	with cd (self.ouPutDir): 
		arguments=[mainExecutablePath,"-i"+input_extention, input_protein_Add , "-o"+output_extention, outputLigName]
		Command().Process_Command(arguments," ", "Converting ligand format to "+output_extention)
	return outputFile


    def PrepareLig (self, ligmaeFormat):
	"""Change ligand format from pdb to mae. Command eg. $SCHRODINGER/ligprep -WAIT -W e,-ph,7.0,-pht,2.0 -epik -i 1 -s 1 -nz -bff 14 -ac -imae 5HT2B_1106_0001_ligand.mae -omae 5HT2B_1106_0001_ligand_prep.mae"""

        mainExecutablePath = os.path.join(self.Program_path,"ligprep")
	outputLigName = FileManager().changeExtention(os.path.basename(self.lig_Add),"_Prep.mae")
	outputFile = os.path.join(self.ouPutDir,outputLigName)
	
	#if the file is already there just return its address
	if os.path.exists(outputFile):
		return outputFile
	
	with cd (self.ouPutDir): 
		arguments=[mainExecutablePath,"-WAIT -W e,-ph,7.0,-pht,2.0 -epik -s 1 -i 1 -r 1 -nz -bff 14 -ac",  "-imae", ligmaeFormat, "-omae", outputLigName]
		Command().Process_Command(arguments," ", "Preparing Ligand input.")
		FileManager().Delete_unwanted_dirs_basedon_Extention (fileExtention_to_keep = "_Prep.mae" , mainDir =self.ouPutDir )
	return outputFile

