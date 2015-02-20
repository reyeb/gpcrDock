#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Protein class represents a protein, as defined by a PDB file.
#
# Author: Sebastian Kelm
# Created: 19/04/2012
#
from prosci.common import write_file
from prosci.util.pdb import Pdb, Atom, residueLetter, residueCode
from prosci.util.residue import ResidueList, Residue, SequenceMappingError, AtomTypeNotFoundError
from prosci.util.gaps import isGap

class Protein(list):
  "A list of ResidueList objects, each of which represents one PDB chain."
  
  def __init__(self, pdb, code=None, ligands=None):
    "Takes a Pdb object or a list of ResidueLists as the first argument. Otherwise passes the argument to Pdb() first, which can deal with filenames. Second argument is an optional short decription (usually a PDB code)."
    self.code = ""
    self.ligands = ()
    
    if not pdb:
      pass
    elif not isinstance(pdb, Pdb):
      if isinstance(pdb[0], ResidueList):
        for reslist in pdb:
          self.append(reslist)
        self.code = pdb[0].code
      elif isinstance(pdb, ResidueList):
        self.extend(pdb.split_chains())
        self.code = pdb.code
      else:
        pdb = Pdb(pdb)
    
    if isinstance(pdb, Pdb):
      self.extend(ResidueList(pdb).split_chains())
      self.code = pdb.code
    
    if code is not None:
      self.code = code
    
    try:
      self.add_ligands(pdb.ligands)
    except AttributeError:
      pass
    
    self.add_ligands(ligands)
  
  def write(self, fname):
    write_file(fname, str(self))
  
  def __repr__(self):
    return "Protein(%s, %s, %s)"%(list.__repr__(self), repr(self.code), repr(self.ligands))
  
  def __str__(self):
    out=""
    for r in self:
      if r:
        out += str(r)
    for r in self.ligands:
      if r:
        out += str(r)
    return out
  
  def __getslice__(self, start=None, end=None):
    return Protein(list.__getslice__(self, start, end))
  
  
  def add_ligands(self, ligands):
    if not ligands:
      return
    if not isinstance(ligands, Protein):
      #print repr(ligands)
      #print Pdb(ligands, allowLigands=True)
      ligands = Protein(ResidueList(Pdb(ligands, allowLigands=True)).split_chains())
    if self.ligands:
      self.ligands.extend(ligands)
    else:
      self.ligands = ligands
  
  
  def get_chain(self, chaincode):
    "Get a particular chain by its chain code"
    for chain in self:
      if chain.chain == chaincode:
        return chain
    for chain in self.ligands:
      if chain.chain == chaincode:
        return chain
    raise KeyError("Chain %s not found in Protein object with code '%s'" % (chaincode, self.code))
  
  
  def get_seq(self):
    "Returns a FASTA string representation of the sequences."
    seq = ""
    for chain in self:
      if chain is not None:
        seq += chain.get_seq()+"/"
    return seq[:-1]
  
  
  def get_coords(self, atomfilter=lambda atom: True, ligands=False):
    "Get a numpy array of coordinates"
    coords=[]
    for chain in self:
      for r in chain:
        if r is not None:
          for a in r:
            if atomfilter(a):
              coords.append(a.xyz)
    if ligands:
      for chain in self.ligands:
        for r in chain:
          if r is not None:
            for a in r:
              if atomfilter(a):
                coords.append(a.xyz)
    return numpy.array(coords)
  
  
  def to_pdb(self, atomfilter=lambda atom: True):
    "Returns a Pdb object containing the Atom objects within this object"
    p = Pdb(self.code, [])
    for chain in self:
      for res in chain:
        for atm in res:
          if atomfilter(atm):
            p.data.append(atm)
    for chain in self.ligands:
      for res in chain:
        for atm in res:
          if atomfilter(atm):
            p.ligands.append(atm)
    return p
  
  
  def iter_atoms(self, ligands=True):
    for chain in self:
      for r in chain:
        for a in r:
          yield a
    if ligands:
      for chain in self.ligands:
        for r in chain:
          for a in r:
            yield a
  
  
  def to_residuelist(self, ligands=False):
    "Returns a single ResidueList object"
    rl = ResidueList([], self.code)
    for chain in self:
      rl.extend(chain)
    if ligands:
      for chain in self.ligands:
        rl.extend(chain)
    return rl
  
  def renumber(self):
    "Renumber residues in each chain from 1 upwards"
    for chain in self:
      chain.renumber()
    for chain in self.ligands:
      chain.renumber()
  
  def renumber_atoms(self):
    "Renumbers all atoms, starting from 1 upwards"
    i = 1
    for chain in self:
      for r in chain:
        for a in r:
          a.iatom = i
          i += 1
    for chain in self.ligands:
      for r in chain:
        for a in r:
          a.iatom = i
          i += 1
  
  
  def remove_residues(self, func, ligands=False):
    i=0
    while i < len(self):
      self[i].remove_residues(func)
      if not self[i]:
        del self[i]
      else:
        i += 1
    
    if ligands:
      i=0
      while i < len(self.ligands):
        self.ligands[i].remove_residues(func)
        if not self.ligands[i]:
          del self.ligands[i]
        else:
          i += 1
  
  
  def iter_backbone(self):
    "Iterate over all backbone atoms that aren't None"
    for chain in self:
      for r in chain:
        for a in r.iter_backbone():
          yield a
  
  
  def find_residue(self, ires, inscode="", chain="", reverse=False):
    instring = None
    if isinstance(ires, Residue) or isinstance(ires, Atom):
      inscode = ires.inscode
      chain = ires.chain
      ires = ires.ires
    elif isinstance(ires, basestring):
      instring = ires
      if ires[:1].isalpha():
        chain = ires[:1]
        ires = ires[1:]
      if ires[-1:].isalpha():
        inscode = ires[-1:]
        ires = ires[:-1]
      ires = int(ires)
    
    result = (-1, -1)
    for ichain, chainresidues in enumerate(self):
      if chainresidues.chain == chain:
        result = (ichain, chainresidues.find_residue(ires, inscode, chain, reverse=reverse))
        break
    
    if result == (-1, -1) and instring is not None:
      result = self.find_residue(instring[1:], chain=instring[:1], reverse=reverse)
    
    return result
  
  
  def map_to_seq(self, seq, renumber=False, start_number=1):
    output = []
    startoffset = 0
    for chain in self:
      #print "Mapping chain", chain.chain, "with sequence:", chain.get_seq(), "to sequence:", seq[startoffset:]
      indices = chain.map_to_seq(seq[startoffset:], renumber, start_number)
      if startoffset:
        for i, x in enumerate(indices):
          indices[i] = x + startoffset
      startoffset = indices[-1]+1
      for i in xrange(startoffset, len(seq)):
        if seq[i] == "/":
          startoffset += 1
        else:
          break
      output.append(indices)
    return output
