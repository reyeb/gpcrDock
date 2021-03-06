#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import tempfile
import subprocess

from prosci.common import ParsingError, DependencyError
from prosci.util.gaps import length_ungapped
from prosci.util.pdb import Pdb
from prosci.util.protein import Protein
from prosci.util.residue import ResidueList
from prosci.util.pdb3d import rmsd_static
#from prosci.util.pdb3d import superimpose as pdb3dsuperimpose

import numpy


class PoorSuperpositionError(RuntimeError):
  pass


def tmalign(pdb1, pdb2, opts=""):
    assert type(pdb1) == type(pdb2)
    if isinstance(pdb1, Pdb):
      return tmalign_objects(pdb1, pdb2, opts)
    else:
      return tmalign_files(pdb1, pdb2, opts)


tmalign_runs = [0]
def tmalign_files(pdb1, pdb2, opts=""):
    tmalign_runs[0] += 1
    fh_matrix, fname_matrix = tempfile.mkstemp()
    try:
      command = "TMalign %s %s -m %s %s"%(pdb1, pdb2, fname_matrix, opts)
      #print command
      p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      tm_result, tm_errors = p.communicate()
      #print "TMalign run %d times now." % tmalign_runs[0]
      #print "TMalign command:"
      #print "TMalign %s %s -m %s %s"%(pdb1, pdb2, fname_matrix, opts)
      #print "TMalign output:"
      #print tm_result
      #print "TMalign errors:"
      #print tm_errors
      f = os.fdopen(fh_matrix)
      rotation_matrix = f.read()
      f.close()
      #print "Rotation matrix:"
      #print rotation_matrix
      #print ""
      if p.returncode != 0 or tm_errors:
        raise DependencyError("TMalign was not found or produced errors. Return code = %d, error messages:\n%s\noutput:%s\n"%(p.returncode, str(tm_errors), str(tm_result)))
    finally:
      os.remove(fname_matrix)
    return parse_tmalign_output(tm_result.splitlines(), rotation_matrix.splitlines())


def tmalign_objects(pdb1, pdb2, opts=""):
    f1 = tempfile.NamedTemporaryFile()
    pdb1.write_renumbered(f1)
    f1.flush()
    
    f2 = tempfile.NamedTemporaryFile()
    pdb2.write_renumbered(f2)
    f2.flush()
    
    try:
      return tmalign_files(f1.name, f2.name, opts)
    finally:
      f1.close()
      f2.close()


def parse_tmalign_output(tm_result, matrix_lines):
    
    try:
      transform = [matrix_lines[2].split()[1:], matrix_lines[3].split()[1:], matrix_lines[4].split()[1:]]
      translate = numpy.array([float(t[0]) for t in transform])
      rotmat = numpy.array([[float(x) for x in t[1:]] for t in transform])
      transform = (translate, rotmat)
    except:
      print "Error parsing the following TMalign rotation matrix:"
      print "\n".join(matrix_lines)
      print "TMalign output was:"
      print "\n".join(tm_result)
      raise
    
    info={}
    seq1 = None
    seq2 = None
    for i, line in enumerate(tm_result):
      if line.startswith("Aligned"):
        fields = line.split(",")
        for f in fields:
          f_fields = f.split("=")
          k=f_fields[0].strip()
          v=f_fields[-1].strip()
          if "." not in v:
            info[k] = int(v)
          else:
            info[k] = float(v)
      elif line[0:4] == '(":"':
        # return sequence1, equivalence, sequence2
        # equivalence is a sequence of " ", "." and ":" chars, where ":" indicates that the residues are within 5 Angstroms of each other.
        seq1 = info["seq1"] = tm_result[i+1].rstrip("\n\r")
        info["equiv"] = tm_result[i+2].rstrip("\n\r")
        seq2 = info["seq2"] = tm_result[i+3].rstrip("\n\r")
      elif line.startswith("TM-score"):
        score, desc = line.split("=")[1].split(None, 1)
        score = float(score)
        if "Chain_1" in desc:
          info["TM-score (Chain_1)"] = score
        elif "Chain_2" in desc:
          info["TM-score (Chain_2)"] = score
    
    if not (seq1 and seq2):
      raise ParsingError("Could not parse TMalign output. No sequences???:\nseq1=%s\nseq2=%s\ntransform=%s\nTM-align output:\n%s"%(seq1, seq2, str(transform), "".join(tm_result)))
    
    if not "TM-score" in info:
      info["TM-score"] = info["TM-score (Chain_2)"]
    
    return transform, info



def transform_structure(struc, transform):
  #tr, rotmat = transform
  #origin = numpy.array([0.0,0.0,0.0])
  #for atm in struc:
  #  origin += atm.xyz
  #origin /= len(struc)
  #
  #for atm in struc:
  #  atm.xyz = numpy.dot(atm.xyz - origin, rotmat) + origin + tr
  
  t, u = transform
  
  for atm in struc:
    x, y, z = atm.xyz
    atm.x = t[0] + u[0,0] * x + u[0,1] * y + u[0,2] * z
    atm.y = t[1] + u[1,0] * x + u[1,1] * y + u[1,2] * z
    atm.z = t[2] + u[2,0] * x + u[2,1] * y + u[2,2] * z
  
  # The above is the python translation of the following fortran code:
  #
  # Code for rotating Chain-1 from (x,y,z) to (X,Y,Z):   
  # do i=1,L     
  #   X(i)=t(1)+u(1,1)*x(i)+u(1,2)*y(i)+u(1,3)*z(i)
  #   Y(i)=t(2)+u(2,1)*x(i)+u(2,2)*y(i)+u(2,3)*z(i)    
  #   Z(i)=t(3)+u(3,1)*x(i)+u(3,2)*y(i)+u(3,3)*z(i)
  # enddo





def superimpose(struc1_allchains, struc2_allchains, subset1=None, subset2=None, fname1=None, fname2=None, align_atoms=("N", "CA", "C", "O"), options="", modify_structures=True, normalise_by_first=False):
    """If modify_structures=True, structure1 will be rotated/translated onto structure2."""
    
    pdb1_filename=fname1
    pdb2_filename=fname2
    
    if isinstance(struc1_allchains, ResidueList) or isinstance(struc1_allchains, Protein):
      struc1_allchains = struc1_allchains.to_pdb()
    if isinstance(struc2_allchains, ResidueList) or isinstance(struc2_allchains, Protein):
      struc2_allchains = struc2_allchains.to_pdb()
    
    if isinstance(subset1, ResidueList) or isinstance(subset1, Protein):
      subset1 = subset1.to_pdb()
    if isinstance(subset2, ResidueList) or isinstance(subset2, Protein):
      subset2 = subset2.to_pdb()
    
    assert type(struc1_allchains) == type(struc2_allchains)
    assert type(subset1) == type(subset2)
    
    
    if not isinstance(struc1_allchains, Pdb):
        pdb1_filename = struc1_allchains
        pdb2_filename = struc2_allchains
        struc1_allchains = Pdb("pdb1", file(pdb1_filename))
        struc2_allchains = Pdb("pdb2", file(pdb2_filename))
        modify_structures=False # We're not returning the structures to the caller, so no use modifying them
    
    if None == subset1:
        subset1 = struc1_allchains
    if None == subset2:
        subset2 = struc2_allchains
    
    
    # if structure has more than 1 chain, only use the first one
    if subset1.chaincount() > 1:
      subset1 = subset1.get_first_chain()
    if subset2.chaincount() > 1:
      subset2 = subset2.get_first_chain()
    
    if normalise_by_first:
      options += " -L %d"%(subset1.rescount())
    
    #~ # align structures and get the sequence alignment
    #~ if pdb1_filename and pdb2_filename:
        #~ # This will run TMalign on the original structure files.
        #~ transform, alignment_info = tmalign_files(pdb1_filename, pdb2_filename, options)
    #~ else:
        #~ # This will create temporary PDB files and run TMalign on those.
        #~ transform, alignment_info = tmalign_objects(subset1, subset2, options)
    
    
    # FORCE PRE-PARSING AND CREATION OF TEMPORARY FILES!!!
    # This ensures predictable behaviour with regards to insertion codes, etc., which TM-align just removes from input files.
    #
    # This will create temporary PDB files and run TMalign on those.
    transform, alignment_info = tmalign_objects(subset1, subset2, options)
    
    
    if modify_structures:
      if not transform:
        raise PoorSuperpositionError("Poor superposition. TM-align did not generate a rotation matrix.")
      transform_structure(struc1_allchains, transform)
    
    #rmsd_value = pdb3dsuperimpose(struc1_allchains, struc2_allchains, seq1, seq2, subset1, subset2, align_atoms, modify_structures)
    
    if normalise_by_first:
      alignment_info["TM-score"] = alignment_info["TM-score (Chain_1)"]
    
    return alignment_info["seq1"], alignment_info["seq2"], alignment_info
