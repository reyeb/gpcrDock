"""a class for storing public functionalities"""

class FileManager():

    def BuildDirectory(self,OUTDIR):
	mainOutDir=os.path.join(OUTDIR,"Gold")
	if not os.path.exist(mainOutDir):
		os.mkdir(mainOutDir)
	print "made directory '%s' ", %(mainOutDir)

    def changeExtention(inputName,extention):
	main_name = inputName.split(".")[0]
	return main_name+"."+extention
