#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import tempfile
from prosci.util.protein import Protein, ResidueList, Pdb
from prosci.common import join

re_mainchainWithoutO = re.compile("atom1:(N|CA|C) atom2:(N|CA|C) ")
re_mainchainWithCB = re.compile("atom1:(N|CA|C|O|CB) atom2:(N|CA|C|O|CB) ")
re_mainchainWithCB2other = re.compile("atom[12]:(N|CA|C|O|CB) ")

re_atom_types = re.compile(r"atom1:(\w+) atom2:(\w+) ")


def get_clash_dict(decoy):
  "Get clashes in the given structure, indexed by atom type"
  if isinstance(decoy, basestring) and "\n" not in decoy:
    p = subprocess.Popen(["clashdet", decoy], stdout=subprocess.PIPE)
    out, err = p.communicate()
  else:
    p = subprocess.Popen(["clashdet", "-"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = p.communicate(str(decoy))
  
  clashes = {}
  for line in out.splitlines():
    if line.startswith("Clash:"):
      m = re_atom_types.search(line)
      atype1 = m.group(1)
      atype2 = m.group(2)
      key = [atype1, atype2]
      key.sort()
      key = " ".join(key)
      try:
        clashes[key] += 1
      except KeyError:
        clashes[key] = 1
  return clashes


def count_stratified_clashes(decoy):
  "Count clashes in the given structure, return counts for (mainchainCB2mainchainCB, mainchainCB2other, other2other)"
  
  clashdict = get_clash_dict(decoy)
  
  N_CA_C = 0
  N_CA_C_O = 0
  N_CA_C_O_CB = 0
  N_CA_C_O_CB_2_other = 0
  other_2_other = 0
  for key in clashdict:
    a, b = key.split(" ")
    if a in ("N", "CA", "C", "O", "CB"):
      if b in ("N", "CA", "C", "O", "CB"):
        if "CB" not in (a, b):
          if "O" not in (a, b):
            N_CA_C += 1
          else:
            N_CA_C_O += 1
        else:
          N_CA_C_O_CB += 1
      else:
        N_CA_C_O_CB_2_other += 1
    elif b in ("N", "CA", "C", "O", "CB"):
        N_CA_C_O_CB_2_other += 1
    else:
        other_2_other += 1
  N_CA_C /= 2
  N_CA_C_O /= 2
  N_CA_C_O_CB /= 2
  N_CA_C_O_CB_2_other /= 2
  other_2_other /= 2
  
  # Make the clash counts cumulative
  #
  result = [N_CA_C, N_CA_C_O, N_CA_C_O_CB, N_CA_C_O_CB_2_other, other_2_other]
  for i in xrange(1, len(result)):
    result[i] += result[i-1]
  
  return result


def has_backbone_or_CB_clash(decoy):
    "Check if there is at least one clash between backbone or CB atoms"
    if isinstance(decoy, basestring):
        if "\n" not in decoy:
            decoy = ResidueList(decoy)
        else:
            decoy = ResidueList(Pdb(decoy, nofilter=True))
    elif isinstance(decoy, Protein):
        decoy = decoy.to_residuelist()
    elif not isinstance(decoy, ResidueList):
        decoy = ResidueList(decoy)
    data = []
    for res in decoy:
        for a in (res.N, res.CA, res.C, res.O, res.CB):
            if a is not None:
                data.append(a)
    p = subprocess.Popen(["clashdet", "-b", "-"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = p.communicate(join(data))
    for line in out.splitlines():
        if line.startswith("Total clashes:"):
            return int(line.split(":")[-1].strip()) > 0
    raise RuntimeError("Failed to parse clashdet output")


def has_backbone_clash(decoy):
    "Check if there is at least one clash between backbone or CB atoms"
    if isinstance(decoy, basestring):
        if "\n" not in decoy:
            decoy = ResidueList(decoy)
        else:
            decoy = ResidueList(Pdb(decoy, nofilter=True))
    elif isinstance(decoy, Protein):
        decoy = decoy.to_residuelist()
    elif not isinstance(decoy, ResidueList):
        decoy = ResidueList(decoy)
    data = []
    for res in decoy:
        for a in res.iter_backbone():
            data.append(a)
    p = subprocess.Popen(["clashdet", "-b", "-"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = p.communicate(join(data))
    for line in out.splitlines():
        if line.startswith("Total clashes:"):
            return int(line.split(":")[-1].strip()) > 0
    raise RuntimeError("Failed to parse clashdet output")
