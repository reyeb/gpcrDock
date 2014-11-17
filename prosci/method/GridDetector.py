import Bio.PDB
import numpy as np


"""Thic class is uysed to build grids around recptor. This can be accompanied by a pocket detection method."""


class GridDetector():

	
    def __init__(self, LIG_ADD):
	self.lig_Add = LIG_ADD
	#Let's have grid point as a list since in future we might have more of a pocket detection which will be added here
	#self.gridPoints = []



    def BuildGridUsingLigandPositionAverage(self):
	"""Build one grid point based on avergaaing the ligand position (center of the ligand coordinates)"""
	gridPoints=[]
	pdb_parser = Bio.PDB.PDBParser(QUIET = True)
	structure = pdb_parser.get_structure("ligand", self.lig_Add)
	atoms = structure.get_atoms()
	coor_list = [a.get_coord() for a in atoms]
	coor_array = np.array(coor_list)
        gridPoint = [float(sum(l))/len(l) for l in zip(*coor_array)]
	str_gridpoint = [str(x) for x in gridPoint]
	gridPoints.append(str_gridpoint)
	
	return gridPoints
