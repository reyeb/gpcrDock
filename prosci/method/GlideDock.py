from prosci.interface.IInterfaceDock import *
from prosci.method.DockParams import DockParams
from prosci.util.command import *
import ntpath
from prosci.util.cd import *

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
		self.DockLigRec(gridfile, index+1, "SP")


    def DockLigRec(self, gridfile, index, dockPrecision):
	"""This is only to do one dock. if multiple dock is required then an input should be defined!!!!!"""	
    	dock_command="""
WRITEREPT YES
USECOMPMAE YES
POSTDOCK_NPOSE 3
MAXREF 800
RINGCONFCUT 2.500000
CALC_INPUT_RMS True
GRIDFILE {0}
LIGANDFILE {1}
PRECISION {2}"""
	mainExecutablePath = os.path.join(self.Program_path,"glide")
	dockNameFile = "dock"+ str(index)+"_"+ dockPrecision #ntpath.basename(gridfile)
	#os.path.dirname(gridfile)
	#print "gridfile",gridfile
	#$SCHRODINGER/utilities/sdconvert -n 1 -imae dock_sorted.mae -osd pose_1.sdf
	
	with cd (os.path.dirname(gridfile)): 
		cur_dockcommand = dock_command.format(gridfile, DockParams.glideLigAdd, dockPrecision)
		with open (dockNameFile+".in", "a") as f:
			f.write(cur_dockcommand)
		arguments=[mainExecutablePath,"-WAIT","-NJOBS 10",  dockNameFile+".in"]
		#uncommnet to run
		#Command().Process_Command(arguments," ","Glid Dock using "+ dockPrecision + str(index))
###******FYI
		#self.Sort( dockNameFile+"_pv.maegz",dockNameFile+ "_sorted.mae",msg = "...sorting "+dockNameFile)
		#self.Gnerate_individual_poses(dockNameFile+ "_sorted.mae",dockNameFile+ "_sorted.pdb", msg = "splitting docked poses")
	
    #def Re_score(self):
	#"""to re_score using another function""""
    	#print "to do" e.g  
	#$SCHRODINGER/utilities/glide_rescore [options] pv-or-lib-files
###******FYI



    def Sort(self,unsorted_dock_poses, sorted_ouput_dock_poses, msg):
	"""to sort the docked poses. sort.rept file contains the dock poses"""
###******FYI
	#$SCHRODINGER/utilities/glide_sort -r sort.rept dock_XP_pv.maegz -o dock_sorted.mae
	#$SCHRODINGER/utilities/glide_sort -r sort.rept dock_XP_pv.maegz -o dock_sorted.mae 
	#soty by as specific function: $SCHRODINGER/utilities/glide_sort -use_gscore dock_XP_pv.maegz
	#sort.rept : We can simply suppose that the best poses are those with the most negative score. 
	#norecep: dont include receptor structure in output file
	# if u wanna sort based on other functuions:  -use_cvdw
	# another way try do so if several re-ranking... just split the unsorted_dock_poses and then generate several sort file and then correlate the rank list to the pdb file number generated
###******FYI
	mainExecutablePath = os.path.join(self.Program_path,"utilities/glide_sort")
	arguments=[mainExecutablePath,"-WAIT","-r","sort.rept",unsorted_dock_poses,"-o", sorted_ouput_dock_poses]
	#uncommnet to run
	#Command().Process_Command(arguments," ",msg)

    def Gnerate_individual_poses(self, sorted_dock_poses, dock_poses_pdb, msg):
	# $SCHRODINGER/utilities/pdbconvert -imae dock1_SP_sorted.mae -opdb dock1_SP_sorted.pdb
	mainExecutablePath = os.path.join(self.Program_path,"utilities/pdbconvert")
	arguments=[mainExecutablePath,"-WAIT","-imae", sorted_dock_poses,"-opdb", dock_poses_pdb]
	#uncommnet to run
	#Command().Process_Command(arguments," ",msg)
	
###******FYI
	# the outpu is a several files named dock1_SP_sorted-n.pdb where n==1 is the receptor and n>1 are all the modelled ligands. The numbering is based on the best model has a n=2.



