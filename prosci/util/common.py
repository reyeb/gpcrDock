"""a class for storing public functionalities"""
import os

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
	main_name = inputName.split(".")[0]
	return main_name+extention
