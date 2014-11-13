#from util.Glide import *
from argparse import ArgumentParser
import ntpath


argparser = ArgumentParser()

argparser.add_argument("-ligand", dest = "l", nargs = "*", help = "ligand_address", type = str)
argparser.add_argument("-receptor", dest = "r", nargs = "*", help = "receptor_address", type = str)
argparser.add_argument("-complexname", dest = "n", nargs = "*", help = "complex_name", type = str)
argparser.add_argument('-mode', choices=['Gold', 'Glide'])


args = argparser.parse_args()

if args.l[0]:
	ligand_address =args.l[0]
else:
	raise "Enter a ligand address"
receptor_address=args.r[0]

if not os.path.exists(ligand_address):
   raise "Couldn't locate the ligand file"

if not os.path.exists(receptor_address):
   raise "Couldn't locate the receptor file"

if args.n:
    complexname=args.n[0]
else:
    complexname=ntpath.basename(receptor_address).split('.')[0]


if args(['Glide']):
	print Glide
	#model=SideChain_Torsion_Calculator(model_decoy_address)
