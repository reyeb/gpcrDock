#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path
import subprocess
from prosci.util.pdb import Pdb
from prosci.common import NotFoundError, ParsingError

def get_pdb_path(pdb_code, pdb_dir):
  pdb_code = pdb_code.lower()
  return os.path.normpath(pdb_dir)+'/'+pdb_code[1:3]+'/pdb'+pdb_code+'.ent.gz'

def get_pdb_file(pdb_code, pdb_dir):
  stringpath = get_pdb_path(pdb_code, pdb_dir)
  if os.path.isfile(stringpath):
    return subprocess.Popen("zcat "+stringpath, shell=True, stdout=subprocess.PIPE).stdout
  return None

def getpdb(pdb_code, pdb_dir, online=False):
  openfile = get_pdb_file(pdb_code, pdb_dir)
  if openfile is None:
    if not online:
      raise NotFoundError("PDB file '%s' not found in database dir '%s'"%(pdb_code, pdb_dir))
    else:
      return getpdb_online(pdb_code)
  return Pdb(pdb_code, openfile)

get_pdb = getpdb



def getpdb_online(pdb_code):
  f=subprocess.Popen("wget -q -O - http://www.pdb.org/pdb/files/%s.pdb.gz | gunzip 2>/dev/null" % (pdb_code.upper()), shell=True, stdout=subprocess.PIPE).stdout
  try:
    try:
      a = Pdb(pdb_code, f)
    except ParsingError:
      raise NotFoundError("Could not retrieve pdb '%s' from www.pdb.org"%(pdb_code))
  finally:
    f.close()
