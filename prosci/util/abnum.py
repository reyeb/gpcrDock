#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ABNUM output parser
#
# Based on James Dunbar's parser in SAbDab, 2013
#


import sys
import os
import shutil
import tempfile
import subprocess

from prosci.util.ali import Ali
from prosci.util.protein import Protein, ResidueList


class AbnumAnnotationError(ValueError):
  pass
class NotAnAntibodyError(AbnumAnnotationError):
  pass

def _interpret(x):
    """
    Function to interpret an annotation in the form H100A into the form ( 100, 'A' )
    """
    assert x[0] in ("H", "L"), "Illegal format for residue number: '%s'"%x
    try:
      return ( int(x[1:]), '')
    except ValueError:
      return ( int(x[1:-1]), x[-1] )

def abnum_sequence(seq):
    """
    Use abnum to number the sequence and test whether the chain is an antibody chain.

    This function requires that abnum installed locally.

    Abnum is currently available as a part of Abysis, a licence for which can be obtained from bionf.org.
    
    @param seq: An amino acid sequence that you wish to number.
    
    @return: numbering, chain type
    
    o chain type is either "H" or "L"
    
    o numbering is a list of position - residue type tuples
        o each position is a tuple of the residue id and insertion code:
            - e.g. position 100A --> (100, "A")
            - e.g. position 44   --> (44, "")
    o e.g. numbering for a sequence  "EVQL...VTVS": 
        [((1, ''), 'E'), ((2, ''), 'V'), ((3, ''), 'Q'), ((4, ''), 'L'),
        ...,
        ((109, ''), 'V'), ((110, ''), 'T'), ((111, ''), 'V'), ((112, ''), 'S') ]

    Only the numbered variable region will be returned.
    
    """
    
    fd, fname=tempfile.mkstemp(".pir")
    try:
      f = os.fdopen(fd, "w")
      try:
        f.write(">seq\nsequence\n%s*\n" % (seq))
      finally:
        f.close()
      
      p = subprocess.Popen(["kabnum_wrapper.pl", fname, "-c"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
      out, err = p.communicate()
    finally:
      os.remove(fname)
    
    if err:
      raise AbnumAnnotationError("ERROR: ABNUM returned an error: "+err)
    elif not out:
      raise NotAnAntibodyError("ERROR: ABNUM could not annotate the given sequence: "+seq)
    elif "Warning" in out:
      warns = [line for line in out.splitlines() if "Warning" in line]
      raise AbnumAnnotationError("ERROR: ABNUM gave warnings: "+"\n".join(warns)+"\n")
    
    try:
        result = map( str.split, out.strip().splitlines() )
        numbering = [ (_interpret(res[0]), res[1])  for res in result if "-" not in res ]
        chain_type = result[0][0][0]
    except IndexError:
        raise Exception("Annotation failed. Unexpected annotation file format. Starts with: %s "%out[:50])
    return numbering, chain_type


def abnum_chain_structure(struc):
  "Annotate a single ResidueList object by changing its residue and chain labels if the chain can be annotated with ABNUM"
  if isinstance(struc, Protein):
    struc = struc.to_residuelist()
  elif not isinstance(struc, ResidueList):
    struc = ResidueList(struc)
  
  seq = struc.get_seq()
  numbering, chain_type = abnum_sequence(seq)
  
  numbered_seq = "".join([x[1] for x in numbering])
  
  ix = seq.index(numbered_seq)
  numbered_seq_ali = "-"*ix + numbered_seq
  ix_end = len(numbered_seq_ali)
  numbered_seq_ali += "-"*(len(seq)-len(numbered_seq_ali))
  
  #print seq
  #print numbered_seq_ali
  
  num_start = numbering[0][0][0]
  num_end = numbering[-1][0][0]
  numbers = [(i, '') for i in xrange(num_start-ix, num_start)] + [x[0] for x in numbering] + [(i, '') for i in xrange(num_end+1, num_end+1+len(numbered_seq_ali)-ix_end)]
  assert len(numbers) == len(numbered_seq_ali)
  
  #print numbers
  
  for res, (ires, inscode) in zip(struc, numbers):
    res.ires = ires
    res.inscode = inscode
    res.chain = chain_type
  
  return struc


def abnum_protein_structure(struc, noerror=True, reorder_chains=True):
  if not isinstance(struc, Protein):
    struc = Protein(struc)
  
  abchains = []
  agchains = []
  for chain in struc:
    if noerror:
      try:
        abnum_chain_structure(chain)
        abchains.append(chain)
      except AbnumAnnotationError:
        agchains.append(chain)
        pass
    else:
      try:
        abnum_chain_structure(chain)
        abchains.append(chain)
      except NotAnAntibodyError:
        agchains.append(chain)
        pass
  chaincodes = [c.chain for c in agchains]
  for c in abchains:
    code = c.chain
    while code in chaincodes:
      code = chr(ord(code)+1)
    if code != c.chain:
      c.chain = code
    chaincodes.append(code)
  
  abchain_codes = [c.chain for c in abchains]
  abchain_codes.sort()
  agchain_codes = [c.chain for c in agchains]
  agchain_codes.sort()
  
  order = abchain_codes + agchain_codes
  struc.sort(key=lambda x: order.index(x.chain))
  
  return struc, abchain_codes, agchain_codes


if __name__ == "__main__":
  from glob import glob
  
  for fname in glob("*.pdb"):
    if "test" in fname:
      continue
    
    p = Protein(fname)
    abnum_protein_structure(p)
    print p
    break
    
