#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Common functions shared by all modules in prosci
#
# Author: Sebastian Kelm
# Created: 12/06/2009
#

import os
import sys
import subprocess
import shlex
import string
import collections
from array import array
from bisect import bisect_left


class OverridableField(object):
  "Descriptor to access a fields that should be the same for all contents of the owner object"
  
  def __init__(self, field):
    self.f = field
  
  def __get__(self, obj, cls=None):
      for item in obj:
        if item is not None:
          return getattr(item, self.f)
      return None


class SettableField(object):
  "Descriptor to access a fields that should be the same for all contents of the owner object"
  
  def __init__(self, field):
    self.f = field
  
  def __get__(self, obj, cls=None):
      for item in obj:
        if item is not None:
          return getattr(item, self.f)
      return None
  
  def __set__(self, obj, val):
      for item in obj:
        if item is not None:
          setattr(item, self.f, val)
  
  def __delete__(self, obj): 
      raise AttributeError("Illegal operation: cannot delete attribute")


def rxrange(start, end=None, step=1):
  if end is None:
    end = start
    start = 0
  return xrange(end-1, start-1, -step)

def rrange(start, end=None, step=1):
  if end is None:
    end = start
    start = 0
  return range(end-1, start-1, -step)


def average(lst, ignoreNone=False):
  total=0.0
  n=0
  for x in lst:
    if not (ignoreNone and None==x):
      total += x
      n+=1
  return float(total)/n


def AND(a, b):
  return a and b

def OR(a, b):
  return a or b

def NAND(a, b):
  return not (a and b)

def NOR(a, b):
  return not (a or b)

def XOR(a, b):
  return (a or b) and not (a and b)


# A generalised join function, that can join lists of non-string objects
# by Sebastian Kelm
#
def join(delim, lst):
    delim = str(delim)
    l = len(lst)
    if l < 1:
        return ""
    
    a = array('c')
    a.extend(str(lst[0]))
    i=1
    while i<l:
      a.extend(delim)
      a.extend(str(lst[i]))
      i+=1
    return a.tostring()


def findAll(sequence, value):
    result=[]
    for i,v in enumerate(sequence):
      if v==value:
        result.append(i)
    return result


def findAllBoolean(sequence, value):
    result=[False] * len(sequence)
    for i,v in enumerate(sequence):
      if v==value:
        result[i] = True
    return result


def tokenize2(separators, seq):
  """tokenize2(separators, seq) : Transforms any type of sequence into a list of words and a list of starting indeces
  
  seq : the sequence (any sequence type, e.g. a list, tuple, string, ...) [will not be modified]
  separators : a sequence of values to be used as separators between words. adjoining separators will be merged.
  
  Returns: words, starting_indeces
           where
              len(starting_indeces) = len(words) + 1
              starting_indeces[-1] = len(seq)
  
  If seq is a string, words are also returned as strings. Otherwise every word is a list. Starting indeces are integers >= 0.
  """
  words, gaps = tokenize(separators, seq)
  
  starting_indices = []
  n=0
  for w, g in zip(words, gaps[:-1]):
    n += g
    starting_indices.append(n)
    n += len(w)
  assert n+gaps[-1] == len(seq)
  starting_indices.append(len(seq))
  
  return words, starting_indices


def tokenize(separators, seq):
  """tokenize(separators, seq) : Transforms any type of sequence into a list of words and a list of gap lengths
  
  seq : the sequence (any sequence type, e.g. a list, tuple, string, ...) [will not be modified]
  separators : a sequence of values to be used as separators between words. adjoining separators will be merged.
  
  Returns: words, gaps
           where len(gaps) = len(words) + 1
  
  The first and last gaps are at the beginning and end of the sequence and may have length 0.
  
  If seq is a string, words are also returned as strings. Otherwise every word is a list. Gap lengths are integers >= 0.
  """
  words = []
  gaps  = [0]
  if len(seq)<1:
    return words, gaps
  
  gapIsOpen=True # current gap size
  for i,v in enumerate(seq):
    if v not in separators:
      if gapIsOpen:
        words.append([])
        gapIsOpen=False
      words[-1].append(v)
    else:
      if not gapIsOpen:
        gaps.append(0)
        gapIsOpen=True
      gaps[-1] += 1
  
  if not gapIsOpen:
    gaps.append(0)
  
  assert len(gaps) == len(words) + 1
  
  if isinstance(seq, basestring):
    for i in xrange(len(words)):
      words[i] = "".join(words[i])
  
  return words, gaps


def reduceTokens(words, gaps, wordcutoffs=0, minwordlength=1, wordValidator=None):
    """reduceTokens(words, gaps, wordcutoffs=0, minwordlength=1, wordValidator=None) : cuts off values from both sides of each token and deletes words that are then below a given length or that do not meet the condition given by the wordValidator(words, gaps, i) function. gap lengths are raised to reflect the changes. wordValidator should return True if the word is to be kept or False if the word should be deleted.
    
    Returns void. The input lists will be modified instead.
    """
    oldlength = sum(gaps)
    i=0
    while i < len(words):
      w = words[i]
      oldlength += len(w)
      if len(w) < (2*wordcutoffs)+minwordlength or (None != wordValidator and not wordValidator(words, gaps, i)):
        # Remove words that are too short
        gaps[i+1] += gaps[i] + len(w)
        del words[i]
        del gaps[i]
        continue
      else:
        # Modify words that are long enough
        words[i] = words[i][wordcutoffs:len(w)-wordcutoffs]
        gaps[i] += wordcutoffs
        gaps[i+1] += wordcutoffs
      i+=1
    
    newlength = sum(gaps)
    for w in words:
      newlength += len(w)
    
    assert newlength == oldlength


def deTokenize(separator, words, gaps):
    """deTokenize(separator, words, gaps) : reverse the work of the function tokenize(.). Returns a single sequence, where gaps are filled using separator.
    
    separator : a single value to be used to fill gaps
    words, gaps : lists of words and gap lengths, as returned by the function tokenize(.)
    """
    assert len(words) + 1 == len(gaps)
    seq=[]
    
    for i,w in enumerate(words):
      for j in xrange(gaps[i]):
        seq.append(separator)
      seq.extend(w)
    for j in xrange(gaps[-1]):
      seq.append(separator)
    
    if len(words) and isinstance(words[0], basestring):
      seq = "".join(seq)
    return seq


def binarySearch(lst, value, low=0, high=None):
    if high == None:
      high = len(lst)
    
    mid = bisect_left(lst, value, low, high)
    
    if mid < len(lst) and lst[mid] == value:
      return mid
    
    return -1 - mid


def splitpath(somepath):
    # e.g.  /path/to/file.txt
    
    path, basename = os.path.split(somepath)
    base, ext = os.path.splitext(basename)
    
    # e.g. "/path/to/", "file", ".txt"
    return (path, base, ext)


def basename_noext(fname):
  return os.path.splitext(os.path.basename(fname))[0]


class ParsingError(RuntimeError):
    pass

class IllegalStateError(RuntimeError):
    pass
IllegalState = IllegalStateError

class DependencyError(RuntimeError):
    pass

class ExecutableDependencyError(DependencyError):
  pass

class DatabaseDependencyError(DependencyError):
  pass

class ArgumentError(ValueError):
    pass

class NotFoundError(IndexError):
    pass


def read_file(fname):
  f = open(fname, "rb")
  try:
    txt = f.read()
  finally:
    f.close()
  return txt

def write_file(fname, txt):
  f = open(fname, "wb")
  try:
    f.write(txt)
  finally:
    f.close()

def read_table(fname, sep="\t", types=None, comment="", line_processor=None, header=False):
  if types:
    if not isinstance(types, dict):
      t = {}
      for key, value in enumerate(types):
        t[key] = value
      types = t
    else:
      types = dict(types)
  
  if "\n" in fname:
    txt = fname
  else:
    txt = read_file(fname)
  data = []
  for line in txt.splitlines():
    if comment and line.startswith(comment):
      continue
    if not line:
      continue
    if header and not data:
      fields = line.split(sep)
      # Enable us to provide a typedict using column headers as keys
      for i, key in enumerate(fields):
        if key in types:
          types[i] = types[key]
          del types[key]
    elif line_processor is not None:
      fields = line_processor(line)
      if not fields:
        continue
    else:
      fields = line.split(sep)
      if types:
        for key in types:
          try:
            fields[key] = types[key](fields[key])
          except:
            print line
            raise
    data.append(fields)
  return data


def _write_table(fout, table, sep="\t", eol="\n", line_processor=None, header=None):
  if line_processor is None:
    line_processor = lambda row: [str(x) for x in row]
  
  if header is not None:
    fout.write(sep.join(line_processor(header)))
    fout.write(eol)
  
  for row in table:
    fout.write(sep.join(line_processor(row)))
    fout.write(eol)
  
def write_table(fout, table, **kwargs):
  if isinstance(fout, basestring):
    fout = open(fout, "wb")
    try:
      _write_table(fout, table, **kwargs)
    finally:
      fout.close()
  else:
    _write_table(fout, table, **kwargs)


def _write_table_from_dict(fout, dictionary, rows=None, cols=None, default=None, rowfilter=None, converter=str, header_converter=str, write_rowheader=True, write_colheader=True):
  if rows is None:
    if isinstance(dictionary, list) or isinstance(dictionary, tuple):
      rows = range(len(dictionary))
    else:
      rows = sorted(dictionary)
  if cols is None:
    cols = sorted(dictionary[rows[0]])
  
  if write_colheader:
    fout.write("#")
    for colkey in cols:
      fout.write("\t"+header_converter(colkey))
    fout.write("\n")
  
  for rowkey in rows:
    row = dictionary[rowkey]
    if rowfilter is not None and not rowfilter(row):
      continue
    
    line = ""
    if write_rowheader:
      line = header_converter(rowkey)
    for colkey in cols:
      try:
        value = row[colkey]
      except KeyError:
        value = default
      line += "\t"+converter(value)
    if not write_rowheader:
      line = line.lstrip("\t")
    fout.write(line+"\n")


def write_table_from_dict(fout, dictionary, **kwargs):
  if isinstance(fout, basestring):
    fout = open(fout, "wb")
    try:
      _write_table_from_dict(fout, dictionary, **kwargs)
    finally:
      fout.close()
  else:
    _write_table_from_dict(fout, dictionary, **kwargs)


def read_table_to_dict(fname, typedict=None, row_processor=None, default_type=None, **kwargs):
  """Read a formatted text file into an OrderedDictionary of dictionaries.
  
  typedict     is a dictionary of types (or converter functions that take one argument and return one argument).
  default_type is the type / converter used for any column not handled by typedict.
  """
  if isinstance(fname, basestring):
    data = read_table(fname, **kwargs)
  else:
    data = fname
  colkeys = data[0]
  datadict = collections.OrderedDict()
  for i in xrange(1, len(data)):
    row = data[i]
    if row_processor is not None:
      row = row_processor(row)
      if not row:
        continue
    rowkey = row[0]
    valdict = {}
    for j in xrange(1, len(colkeys)):
      key = colkeys[j]
      x = row[j]
      if typedict is not None and key in typedict:
        try:
          x = typedict[key](x)
        except:
          print >>sys.stderr, "col key:", key
          print >>sys.stderr, "field value:", x
          print >>sys.stderr, "type / conversion function:", typedict[key]
          raise
      elif default_type is not None:
        x = default_type(x)
      valdict[key] = x
    datadict[rowkey] = valdict
  return datadict


def which(fname):
  path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), fname)
  
  if not path or not os.path.exists(path):
    p = subprocess.Popen(shlex.split("which %s" % (fname)), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    path, errors = p.communicate()
    path = path.strip()
    #if errors.strip():
    #  sys.stderr.write(errors)
    if not path or not os.path.exists(path):
      return None
    
    path = os.path.abspath(path)
  
  return path


def filter_string(inputstring, allow=(), deny=()):
  allowed = ""
  for cat in allow:
    allowed += getattr(string, cat)
  denied = ""
  for cat in deny:
    denied += getattr(string, cat)
  return filter(lambda x:x in allowed and x not in denied, inputstring)


class Data(object):
  def __str__(self):
    output = ""
    for field in dir(self):
      if not field.startswith("_"):
        output += " %s=%s," % (field, str(getattr(self, field)))
    return "<Data:"+output[:-1]+">"

  def __repr__(self):
    output = ""
    for field in dir(self):
      if not field.startswith("_"):
        output += " %s=%s," % (field, repr(getattr(self, field)))
    return "<Data:"+output[:-1]+">"


def get_python_library_root():
    "Get the directory containing the 'prosci' python library"
    return os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
