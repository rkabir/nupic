# ----------------------------------------------------------------------
#  Copyright (C) 2006,2007 Numenta Inc. All rights reserved.
#
#  The information and source code contained herein is the
#  exclusive property of Numenta Inc. No part of this software
#  may be used, reproduced, stored or distributed in any form,
#  without explicit written authorization from Numenta Inc.
# ----------------------------------------------------------------------


__all__ = ["cross_list", "cross", "combinations"]

def cross_list(*sequences):
  """
  From: http://book.opensourceproject.org.cn/lamp/python/pythoncook2/opensource/0596007973/pythoncook2-chp-19-sect-9.html
  """
  result = [[ ]]
  for seq in sequences:
    result = [sublist+[item] for sublist in result for item in seq]
  return result

def cross(*sequences):
  """
  From: http://book.opensourceproject.org.cn/lamp/python/pythoncook2/opensource/0596007973/pythoncook2-chp-19-sect-9.html
  """
  # visualize an odometer, with "wheels" displaying "digits"...:
  wheels = map(iter, sequences)
  digits = [it.next( ) for it in wheels]
  while True:
    yield tuple(digits)
    for i in range(len(digits)-1, -1, -1):
      try:
        digits[i] = wheels[i].next( )
        break
      except StopIteration:
        wheels[i] = iter(sequences[i])
        digits[i] = wheels[i].next( )
    else:
      break

def dcross(**keywords):
  """
  Similar to cross(), but generates output dictionaries instead of tuples.
  """
  keys = keywords.keys()
  # Could use keywords.values(), but unsure whether the order
  # the values come out in is guaranteed to be the same as that of keys
  # (appears to be anecdotally true).
  sequences = [keywords[key] for key in keys]

  wheels = map(iter, sequences)
  digits = [it.next( ) for it in wheels]
  while True:
    yield dict(zip(keys, digits))
    for i in range(len(digits)-1, -1, -1):
      try:
        digits[i] = wheels[i].next( )
        break
      except StopIteration:
        wheels[i] = iter(sequences[i])
        digits[i] = wheels[i].next( )
    else:
      break

def combinations(n, c):
  m = n - 1
  positions = range(c)
  while True:
    yield tuple(positions)
    success = False
    lastPi = m
    for i in xrange(c-1, -1, -1):
      pi = positions[i]
      if pi < lastPi:
        pi += 1
        for j in xrange(i, c):
          positions[j] = pi
          pi += 1
        success = True
        break
      lastPi = pi-1
    if not success: break # Done.

def permutations(x):
  if len(x) > 1:
    for permutation in permutations(x[1:]):
      # Stick the first digit in every position.
      for i in xrange(len(permutation)+1):
        yield permutation[:i] + x[0:1] + permutation[i:]
  else: yield x