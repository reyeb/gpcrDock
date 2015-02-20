from pipeline import *
from argparse import ArgumentParser
import ntpath
import os
from main import *
from prosci.method.DockParams import DockParams

#python gpcrDockMain.py -ligand /home/t701033/data/docking/test/input/5HT2B_1106_0001_ligand.pdb -receptor /home/t701033/data/docking/test/input/5HT2B_1106_0001_receptor.pdb -outDirectory /home/t701033/data/docking/test -mode Glide

argparser = ArgumentParser()

argparser.add_argument("-ligand", dest = "l", nargs = "*", help = "ligand_address", type = str)
argparser.add_argument("-receptor", dest = "r", nargs = "*", help = "receptor_address", type = str)
argparser.add_argument("-complexname", dest = "n", nargs = "*", help = "complex_name", type = str)
argparser.add_argument("-outDirectory", dest = "o", nargs = "*", help = "complex_name", type = str)
argparser.add_argument('-mode', dest = "mode", choices=['Gold', 'Glide','Vina','all'])


args = argparser.parse_args()

if args.l:
	ligand_address =args.l[0]
else:
	raise IOError("Enter a ligand address")

if args.r:
	receptor_address=args.r[0]
else:
	raise IOError("Enter a receptor address")


if args.o:
	ouput_dir=args.o[0]
else:
	raise IOError("Enter an output location")


if not os.path.exists(ligand_address):
   raise IOError("Couldn't locate the ligand file")

if not os.path.exists(receptor_address):
   raise IOError("Couldn't locate the receptor file")

if not os.path.exists(ouput_dir):
   print "making directory", ouput_dir
   os.mkdir(ouput_dir)

if args.n:
    complexname=args.n[0]
else:
    complexname=ntpath.basename(receptor_address).split('_receptor.')[0]

	
#####********JUST FOR This Bash run
cparts=complexname.split("_")
#LigandFileAddress="/home/t701033/data/mydata/GPCR2013/LigandFiles"
LigandFileAddress="/data/rockthrush/esmaielb/MyCodes/GPCRTestSet/GPCR2013/LigandFiles"
DockParams.glideLigAdd=os.path.join(LigandFileAddress,cparts[0]+"_ligand_Prep.mae")
DockParams.GoldLigAdd=os.path.join(LigandFileAddress,cparts[0]+"_ligand_Prep.mol2")
DockParams.VinaLigAdd=os.path.join(LigandFileAddress,cparts[0]+"_ligand_Prep.pdbqt")
#####********
#print args.mode
	#print Glide
	#model=SideChain_Torsion_Calculator(model_decoy_address)

#EC_ADD, LIG_ADD, COMPLEXNAME, OUTDIR, MODE)
#import time
#start_time = time.time()


main(receptor_address,ligand_address,complexname,ouput_dir,args.mode).Run_Dock()
#print("--- %s seconds ---" % str(time.time() - start_time))

