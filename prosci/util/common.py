"""a class for storing public functionalities"""
import os
from prosci.util.cd import *


class FileManager():


    def BuildDirectory(self,location,nameList):
	"""Build  folders & subfolder in the location directory and in the order of nameList"""
	curr_out=location
	for name in nameList:
		folderAdd = os.path.join(curr_out,name)
		if not os.path.exists(folderAdd):
			os.mkdir(folderAdd)
			print 'made directory %s ' %(folderAdd)
		curr_out = folderAdd
	return curr_out

			

    def changeExtention(self,inputName,extention):
	"""chnges the extention """
	main_name = inputName.split(".")[0]
	return main_name+extention



    def Delete_unwanted_dirs_basedon_Names(self, files_to_keep = [],  mainDir = ""):
	"""Takes as input a directory address. Looks into the directory and the files which their names are not mentioned in the files_to_keep list are removed. """
	print mainDir
	with cd (mainDir): 
		allfiles = [filen for filen in os.listdir(mainDir) if os.path.isfile(os.path.join(mainDir, filen))]
		for file_name in allfiles:	
			if file_name not in files_to_keep:
				print file_name
				#os.remove(file_name)

    def Delete_unwanted_dirs_basedon_Extention(self,fileExtention_to_keep = None, mainDir = ""):
	"""Takes as input a directory address. Looks into the directory and the files which their names have extention fileExtention_to_keep are kept"""
	print mainDir
	with cd (mainDir): 
		allfiles = [filen for filen in os.listdir(mainDir) if os.path.isfile(os.path.join(mainDir, filen))]
		for file_name in allfiles:
			if  not file_name.endswith(fileExtention_to_keep):
				print file_name
				#os.remove(file_name)
