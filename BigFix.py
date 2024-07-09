#   File: BigFix.py
#   see the file "LICENSE" for the full license
#   The BigFix Python class (and any related external routines)
#   An object class capable of working in mostly-normal numpy.py
#   routines, including libraries buit on top of python and numpy
#   libraries such as Tensorflow and Pytorch.
#   The class objects maintain a fixed-point integer representation
#   of a value, using multi-precision integers native to python and numpy (BigInts)
#   All versions < 1.0 are transitory and offer no guarantees of functionality.
#   BigFix v0.0.1
#   Copyright 2024 James Richard Huddle
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import random
import numpy as np

# dia of universe in nanometers =  837000000000000000000000000000000000 (est.)
#                         10^36 = 1000000000000000000000000000000000000

class BigFix:
  precision = 36 # 100 50 1000  # <--- set it here.  period.
  big1 = 10**precision
  big2 = 10**(precision*2)
  
  def __init__(self, val):
    self.fromInt(val)

  def __str__(self):
    ibig = BigRound(self.big) # self.big does not change
    top = ibig // BigFix.big1
    bottom = ibig - (top * BigFix.big1)
    if bottom == 0:
      return str(top)
    return str(top) +"."+ (str(bottom + BigFix.big1)[1:22].rstrip('0'))

  def __repr__(self):
    return str(self)

  def __add__(self, other):
    return Big(self.big + other.big)

  def __sub__(self, other):
    return Big(self.big - other.big)

  def __mul__(self, other):
    if isinstance(other, np.ndarray):
      return other * self
    return Big((self.big * other.big) // BigFix.big1)

  def __floordiv__(self, other):
    if isinstance(other, int):
      other = BigFix(other)
    return Big((self.big * BigFix.big1) // other.big)

  def __truediv__(self, other):
    if isinstance(other, int):
      other = BigFix(other)
    return Big((self.big * BigFix.big1) // other.big)

  def trunc(self):
    return Big((self.big // BigFix.big1) * BigFix.big1)

  def fromInt(self, val):
    self.big = val * BigFix.big1

  def fromBig(self, val):
    self.big = val

  def full(self):
    top = self.big // BigFix.big1
    bottom = self.big - (top * BigFix.big1)
    if bottom == 0:
      return str(top)
    return str(top) +"."+ (str(bottom + BigFix.big1)[1:].rstrip('0'))

def Big(val):
  ret = BigFix(1)
  ret.big = val
  return ret

def BigRnd():
  return Big(random.randint(0, BigFix.big1))

def rFix(mat):
  if isinstance(mat, int):
    return BigFix(mat)
  if isinstance(mat, BigFix):
    return mat
  if isinstance(mat, float): # fix this
    return mat
  if isinstance(mat, str): # make this better (i.e. incl. strs)
    return BigFix(int(mat))
  newmat = []
  for j in mat:
    i = rFix(j)
    newmat.append(i)
  return np.array(newmat)

def Fix(mat):
  if isinstance(mat, int):
    return BigFix(mat)
  if isinstance(mat, BigFix):
    return mat
  if isinstance(mat, float): # fix this
    return mat
  if isinstance(mat, str): # make this better (i.e. incl. strs)
    return BigFix(int(mat))
  return rFix(mat)

def BigRound(big):
  ibig = big + 10000000000000 # these three lines
  ibig    //= 100000000000000 # help eliminate
  ibig     *= 100000000000000 # repeating nines (also 1.00000000...000000000341) <-- trailing trash
  return ibig

# Not yet ready for prime time
def BigFloat(val1,val2,zeroCount=0):
  top = val1 * BigFix.big1
  bottom = (val2 * BigFix.big1) // BigFix.big1
  # here's what I want to do
  # 290000000000000000000 becomes 290000000 - I want to chop the trailing 0's TO A POINT
