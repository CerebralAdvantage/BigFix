#   File: BigFix.py
#   see the file "LICENSE" for the full license
#   The BigFix Python class (and any related external routines)
#   An object class capable of working in mostly-normal numpy.py
#   routines, including libraries buit on top of python and numpy
#   libraries such as Tensorflow and Pytorch.
#   The class objects maintain a fixed-point integer representation
#   of a value, using multi-precision integers native to python and numpy (BigInts)
#   All versions < 1.0 are transitory and offer no guarantees of functionality.
#
#   BigFix v0.0.2
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
from math import sqrt, isqrt

def IntLike(val):
  return type(val) == int or type(val) == np.int64 or type(val) == np.int32 or type(val) == np.int16

def FloatLike(val):
  return type(val) == float or type(val) == np.float64 or type(val) == np.float32 or type(val) == np.float16

def ListLike(val):
  return type(val) == list or type(val) == np.ndarray


class BigFix:

  precision = 100 # 50 1000  # <--- set it here.  period.
  big1 = 10**precision
  big2 = 10**(precision*2) # useful for 'large power' modulo (if we ever need that)
  prec = 10 # for __str__()

  def __init__(self, val):
    if IntLike(val):
      self.fromInt(val)
    if type(val) == float or type(val) == np.float64 or type(val) == np.float32 or type(val) == np.float16:
      self.fromFloat(val)

  def __str__(self):
    ibig = BigRound(self.big) # self.big does not change
    top = ibig // BigFix.big1
    bottom = ibig - (top * BigFix.big1)
    if bottom == 0:
      return str(top)
    p = BigFix.prec + 1
    return str(top) +"."+ (str(bottom + BigFix.big1)[1:p].rstrip('0'))

  def __repr__(self):
    return str(self)

  def __pow__(self, val):
    if val == 0.5:
      bigger = self.big * BigFix.big1
      return Big(isqrt(bigger))
    return BigFix(13)

  def __radd__(self, other):
    return BigFix.__add__(self, other)

  def __add__(self, other):
    if IntLike(other):
      other = BigFix(other)
    return Big(self.big + other.big)

  def __rsub__(self, other):
    return BigFix.__sub__(self, other)

  def __sub__(self, other):
    if IntLike(other):
      other = BigFix(other)
    return Big(self.big - other.big)

  def __rmul__(self, other):
    return BigFix.__mul__(self, other)

  def __mul__(self, other):
    if IntLike(other):
      other = BigFix(other)
    return Big((self.big * other.big) // BigFix.big1)

  def __rfloordiv__(self, other):
    return BigFix.__floordiv__(self, other)

  def __floordiv__(self, other):
    if IntLike(other):
      other = BigFix(other)
    return Big((self.big * BigFix.big1) // other.big)

  def __mod__(self, other):
    if IntLike(other):
      other = BigFix(other)
    result = Big((self.big * BigFix.big1) // other.big)
    chop = Big((result.big // BigFix.big1) * BigFix.big1)
    return self - (other * chop) # all BigFix objects

  def __ifloordiv__(self, other):
    if IntLike(other):
      other = BigFix(other)
    self.big = (self.big * BigFix.big1) // other.big
    return self

  def __itruediv__(self, other):
    if IntLike(other):
      other = BigFix(other)
    self.big = (self.big * BigFix.big1) // other.big
    return self

  def __rtruediv__(self, other):
    return BigFix.__truediv__(self, other)

  def __truediv__(self, other):
    if IntLike(other):
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

  def sqrt(self):
    bigger = self.big * BigFix.big1
    return Big(isqrt(bigger))

  def fromFloat(self, val):
    fstr = str(val)
    fs = fstr.split(".")
    top = int(fs[0]) * BigFFix.big1
    print("top = ",top)
    self.big = top + bottom

  def conjugate(self):  #change this... someday
    return self
    

# Not yet ready for prime time
def BigFloat(vfloat):  #(val1,val2,zeroCount=0):
  top = val1 * BigFix.big1
  bottom = (val2 * BigFix.big1) // BigFix.big1
  # here's what I want to do
  # 290000000000000000000 becomes 290000000 - I want to chop the trailing 0's TO A POINT

def Big(val):
  ret = BigFix(1)
  ret.big = val
  return ret

def BigRnd():
  return Big(random.randint(0, BigFix.big1))

def rFix(mat):
  if IntLike(mat):
    return BigFix(mat)
  if FloatLike(mat):
    return BigFloat(mat)
  if isinstance(mat, BigFix):
    return mat
  if isinstance(mat, str): # make this better (i.e. incl. strs)
    return BigFix(int(mat))
  newmat = []
  for j in mat:
    i = rFix(j)
    newmat.append(i)
  return newmat

def Fix(mat):

  # basically, if it's not a list, convert to BigFix and return
  # ditto on the recursion.  What is needed is a savvy constructor.
  # for instance, if it's already a BigFix, constructor makes a copy

  if IntLike(mat):
    return BigFix(mat)
  if FloatLike(mat):
    return BigFloat(mat)
  if isinstance(mat, BigFix):
    return mat
  if isinstance(mat, str): # make this better (i.e. incl. strs)
    return BigFix(int(mat))
  return rFix(mat)

def BigRound(big):
  ibig = big + 10000000000000 # these three lines
  ibig    //= 100000000000000 # help eliminate
  ibig     *= 100000000000000 # repeating nines (also 1.00000000...000000000341) <-- trailing trash
  return ibig


# **************************************************************************************************
# use these if np.array routines fail
# **************************************************************************************************

def dot(mat1, mat2):
  return vector_sum(Mul(mat1, mat2))
  
def scalar_multiply(c: BigFix, v):
  return [ c * v_i for v_i in v ]

def divide_by_scalar(v, c: BigFix):
  return [ v_i / c for v_i in v ]

def vector_sum(vector):
  finalSum = Big(0)
  for i in range(len(vector)):
    finalSum = finalSum + vector[i]
  return finalSum

def matrix_sum(vectors): # good for a vector of vectors
  num_elements = len(vectors[0])
  sums = [0]*num_elements
  sums = Fix(sums)
  for i in range(len(vectors)):
    for j in range(len(vectors[0])):
      sums[j] = sums[j] + vectors[i][j]
  return sums

def vector_mean(vectors):
  n=len(vectors)
  return divide_by_scalar(vector_sum(vectors), BigFix(n))

def Add(mat1, mat2):
  return Visit(mat1, mat2, lambda a,b: a+b)

def Sub(mat1, mat2):
  return Visit(mat1, mat2, lambda a,b: a-b)

def Mul(mat1, mat2):
  return Visit(mat1, mat2, lambda a,b: a*b)

def Div(mat1, mat2):
  return Visit(mat1, mat2, lambda a,b: a/b)

BadTrip = False

def Visit(mat1, mat2, fn):
  """ visits 2 similar nd arrays and performs function fn on each list item """
  global BadTrip
  if ListLike(mat1) and ListLike(mat2):
    BadTrip = False # Set for rVisit entry
    return rVisit(mat1, mat2, fn)
  else:
    if ListLike(mat1) or ListLike(mat2):
      BadTrip = True # artifact for bug hunting
      print("Can only work with two similar lists!")
      return
    else:
      return fn(mat1, mat2)

def rVisit(mat1, mat2, fn):
  global BadTrip
  if BadTrip == False: # check if it was set recursively
    # This also checks that BOTH mats are type list or BOTH are type np.ndarray
    if (type(mat1) == list and type(mat2) == list) or (type(mat1) == np.ndarray and type(mat2) == np.ndarray):
      if len(mat1) != len(mat2):
        print("Lists are not similar (different shapes)!")
        BadTrip = True # helps kill recursions
        return
      newmat = []
      for j in range(len(mat1)):
        i = rVisit(mat1[j],mat2[j], fn)
        newmat.append(i)
      return newmat # from recursion
    else: # not true that both are lists
      if ListLike(mat1) or ListLike(mat2):
        print("Lists are not similar (different shapes)!")
        BadTrip = True # helps kill recursions
        return
      else: # true that both are not lists
        return fn(mat1, mat2) # process the terminal nodes and return
