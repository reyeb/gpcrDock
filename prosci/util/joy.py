#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import tempfile
import subprocess

from prosci.util.ali import Ali
from prosci.util.protein import Protein, ResidueList


def annotate_single_chain(struc, setcode=None):
  code = struc.code
  strucfname = code+".atm"
  
  tmpdir = tempfile.mkdtemp()
  try:
    f = open(os.path.join(tmpdir, strucfname), "w")
    f.write(str(struc))
    f.close()
    
    p = subprocess.Popen("joy --nohtml --nops --nortf --nodomain %s"%(strucfname), cwd=tmpdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    
    try:
      annot = Ali(os.path.join(tmpdir, code+".tem"))
    except:
      sys.stderr.write("""
Joy output:
%s

Joy errors:
%s
      \n""" % (out, err))
      raise
    
  finally:
    shutil.rmtree(tmpdir)
  
  if setcode:
    for eg in annot:
      for entry in eg:
        entry.code = setcode
  
  return annot



def annotate_protein(struc):
  if not isinstance(struc, Protein):
    struc = Protein(struc)
  
  annot = annotate_single_chain(struc)
  
  seq = annot[0].master.seq
  protein_indices = struc.map_to_seq(seq)
  
  output = []
  for chain, chain_indices in zip(struc, protein_indices):
    a = annot.copy_columns(chain_indices)
    a[0].code = struc.code + chain.chain
    output.append(a[0])
  
  return Ali(output)



"""
def annotate_segment(struc, startresidue, endresidue, setcode=None):
  annot = annotate_single_chain(struc, setcode)
  
  if isinstance(struc, Protein):
    struc = struc.to_residuelist()
  elif not isinstance(struc, ResidueList):
    struc = ResidueList(struc)
  
  seq = annot[0].master.seq
  indeces = struc.map_to_seq(seq)
  
  assert len(indeces) == len(struc)
  
  indeces_subset = []
  saw_end = False
  for res, ix in zip(struc, indeces):
    if indeces_subset or res.equals_in_name(startresidue):
      indeces_subset.append(ix)
    if res.equals_in_name(endresidue):
      saw_end = True
      break
  
  assert saw_end, "Did not finish mapping JOY output structure to sequence - JOY may have parsed the structure differently from us?"
  
  annot.keep_columns(indeces_subset)
  
  return annot
"""
