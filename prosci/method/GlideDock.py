from prosci.interface.IInterfaceDock import *
from prosci.method.DockParams import DockParams
from prosci.util.command import *
import ntpath
from prosci.util.cd import *
import os

class GlideDock(IInterfaceDock):
	

    #def __init__(self, LIG_ADD= None, GRID_Files_List = None):
    def __init__(self):
	
	#self.dockPrecision = "XP"
	#self.lig_Add = LIG_ADD
	#self.ouPutDir =OUTDIR
	self.Program_path = Command().Get_program_path("maestro").replace("maestro","")


    def Dock(self):
	print "start Docking"
	
	#for each grid file we should one set of docking
	for index, gridfile in enumerate(DockParams.glidegridZipAdds):
		SP_selected_poses_add = self.DockLigRec_SP(gridfile, index+1, "SP")
		self.DockLigRec_XP(gridfile, SP_selected_poses_add, index+1, "XP")


    def DockLigRec_SP(self, gridfile, index, dockPrecision):
	"""This is only to do one dock. if multiple dock is required then an input should be defined!!!!!"""	
    	dock_command="""
WRITEREPT YES
DOCKING_METHOD confgen
CALC_INPUT_RMS True
GRIDFILE {0}
LIGANDFILE {1}
PRECISION {2}"""
	#COMPRESS_POSES FALSE
	mainExecutablePath = os.path.join(self.Program_path,"glide")
	dockNameFile = "dock"+ str(index)+"_"+ dockPrecision #ntpath.basename(gridfile)
	#os.path.dirname(gridfile)
	#print "gridfile",gridfile
	#$SCHRODINGER/utilities/sdconvert -n 1 -imae dock_sorted.mae -osd pose_1.sdf
	
	with cd (os.path.dirname(gridfile)): 
		cur_dockcommand = dock_command.format(gridfile, DockParams.glideLigAdd, dockPrecision)
		with open (dockNameFile+".in", "w") as f:
			f.write(cur_dockcommand)	
		arguments=[mainExecutablePath,"-WAIT",  dockNameFile+".in"]
		#uncommnet to run
		Command().Process_Command(arguments," ","Glid Dock using "+ dockPrecision + str(index) + "the output is in: " + os.path.dirname(gridfile))
	###******FYI
		self.Sort( dockNameFile+"_pv.maegz",dockNameFile+ "_sorted.mae",dockPrecision,msg = "...sorting "+dockNameFile +"only keeping scores better than -6"  ,gscore_cutoff=-6 )
	return os.path.join(os.path.dirname(gridfile),dockNameFile+ "_sorted.mae")
		
		




    def DockLigRec_XP(self, gridfile,SP_selected_poses_add, index, dockPrecision):
	"""This is only to do one dock. if multiple dock is required then an input should be defined!!!!!"""	
    	dock_command="""WRITEREPT YES
DOCKING_METHOD confgen
CALC_INPUT_RMS True
WRITE_XP_DESC True
GRIDFILE {0}
LIGANDFILE {1}
PRECISION {2}"""
	mainExecutablePath = os.path.join(self.Program_path,"glide")
	dockNameFile = "dock"+ str(index)+"_"+ dockPrecision #ntpath.basename(gridfile)
	#os.path.dirname(gridfile)
	#print "gridfile",gridfile
	#$SCHRODINGER/utilities/sdconvert -n 1 -imae dock_sorted.mae -osd pose_1.sdf
			###build a folder for XP solutions here sinve we have 
	XP_folder=os.path.join(os.path.dirname(gridfile),"XP")
	if not os.path.exists(XP_folder):
		os.mkdir(XP_folder)
		
	with cd (XP_folder): 
		cur_dockcommand = dock_command.format(gridfile, SP_selected_poses_add, dockPrecision)
		with open (dockNameFile+".in", "w") as f:
			f.write(cur_dockcommand)
		
		arguments=[mainExecutablePath,"-WAIT",  dockNameFile+".in"]
		#uncommnet to run
		Command().Process_Command(arguments," ","Glid Dock using "+ dockPrecision + str(index) + "the oupt is in: " +XP_folder)
	###******FYI
		self.Sort( dockNameFile+"_pv.maegz",dockNameFile+ "_sorted.mae",dockPrecision,msg = "...sorting "+dockNameFile)
		

    def Sort(self,unsorted_dock_poses, sorted_ouput_dock_poses, dockPrecision, msg = None, gscore_cutoff = None):
	"""to sort the docked poses. sort_SP.rept file contains the dock poses sorted by -use_gscore and only the ones with better score than (lower) than -6 (-gscore_cut -6) so all of the models reported here can be submitted to decok_XP. Also, dock1_SP_sorted.mae will only contain these models """
	###******FYI
 	#$SCHRODINGER/utilities/glide_sort -r sort_SP2.rept -o dock1_SP_sorted.mae -use_gscore -gscore_cut -6 dock1_SP_pv.mae
	#norecep: dont include receptor structure in output file
	# if u wanna sort based on other functuions:  -use_cvdw
	# another way try do so if several re-ranking... just split the unsorted_dock_poses and then generate several sort file and then correlate the rank list to the pdb file number generated
	###******FYI
	mainExecutablePath = os.path.join(self.Program_path,"utilities/glide_sort")
	if gscore_cutoff is not None:
		arguments=[mainExecutablePath,"-r","sort_"+dockPrecision+".rept","-o", sorted_ouput_dock_poses ,"-use_gscore","-gscore_cut", str(gscore_cutoff),unsorted_dock_poses]
	else:
		arguments=[mainExecutablePath,"-r","sort_"+dockPrecision+".rept","-o", sorted_ouput_dock_poses ,"-use_gscore",unsorted_dock_poses]	
	#uncommnet to run
	Command().Process_Command(arguments," ",msg)
	





####
#self.Gnerate_individual_poses(dockNameFile+ "_sorted.mae",dockNameFile+ "_sorted.pdb", msg = "splitting docked poses")
	
    #def Re_score(self):
	#"""to re_score using another function""""
    	#print "to do" e.g  
	#$SCHRODINGER/utilities/glide_rescore [options] pv-or-lib-files
	###******FYI
	
	

    #def Gnerate_individual_poses(self, sorted_dock_poses, dock_poses_pdb, msg):
	# $SCHRODINGER/utilities/pdbconvert -imae dock1_SP_sorted.mae -opdb dock1_SP_sorted.pdb
	#mainExecutablePath = os.path.join(self.Program_path,"utilities/pdbconvert")
	#arguments=[mainExecutablePath,"-WAIT","-imae", sorted_dock_poses,"-opdb", dock_poses_pdb]
	#uncommnet to run
	#Command().Process_Command(arguments," ",msg)
	
	###******FYI
	# the outpu is a several files named dock1_SP_sorted-n.pdb where n==1 is the receptor and n>1 are all the modelled ligands. The numbering is based on the best model has a n=2.



