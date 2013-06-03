# ----------------------------------------------------------------------
#  Copyright (C) 2006-2008 Numenta Inc. All rights reserved.
#
#  The information and source code contained herein is the
#  exclusive property of Numenta Inc. No part of this software
#  may be used, reproduced, stored or distributed in any form,
#  without explicit written authorization from Numenta Inc.
# ----------------------------------------------------------------------

from nupic.regions.ImageSensorExplorers.BaseExplorer import BaseExplorer


class OnionBlock(BaseExplorer):

  """
  This explorer deterministically presents each image at every possible
  position within a N-radius block centered at the centroid of the image.
  """

  def __init__(self, radius=4, *args, **kwargs):
    """
    @param radius: the distance from the center, in pixels, at which the
                   sweeps start;
    @param numRepetitions: number of times to present each inward sweep.
    """
    BaseExplorer.__init__(self, *args, **kwargs)
    # Parameter checking
    if type(radius) is not int or radius < 1:
      raise RuntimeError("'radius' should be a positive integer")
    # Parameters
    self._radius = radius
    # Internal state
    self._itersDone = 0


  def _computeNextPosn(self, iteration=None):
    """
    Helper method that deterministically computes the next
    inward sweep position.
    """

    radius = self._radius
    if iteration is None:
      iteration = self._itersDone

    # Compute iteration indices
    edgeLen = 2 * radius + 1
    numBlocksPerCat = edgeLen * edgeLen
    catIndex = iteration // numBlocksPerCat
    blockCatIndex = iteration % numBlocksPerCat
    # Compute position within onion block
    posnX = (blockCatIndex % edgeLen) - radius
    posnY = (blockCatIndex // edgeLen) - radius

    self.position['reset'] = True
    self.position['image'] = catIndex
    self.position['offset'] = [posnX, posnY]

    # Debugging output to console
    if False:
      print "[%04d] %d: (%d, %d) %s" % ( \
            self._itersDone,
            self.position['image'],
            self.position['offset'][0],
            self.position['offset'][1],
            "RESET" if self.position['reset'] else "")

    # Update iteration count
    self._itersDone = iteration + 1



  def seek(self, iteration=None, position=None):
    """
    Seek to the specified position or iteration.

    iteration -- Target iteration number (or None).
    position -- Target position (or None).

    ImageSensor checks validity of inputs, checks that one (but not both) of
    position and iteration are None, and checks that if position is not None,
    at least one of its values is not None.

    Updates value of position.
    """
    self._computeNextPosn(iteration=iteration)


  def first(self):
    """
    Set up the position.

    BaseExplorer picks image 0, offset (0,0), etc., but explorers that wish
    to set a different first position should extend this method. Such explorers
    may wish to call BaseExplorer.first(center=False), which initializes the
    position tuple but does not call centerImage() (which could cause
    unnecessary filtering to occur).
    """
    BaseExplorer.first(self, center=False)
    self._computeNextPosn(iteration=0)


  def next(self, seeking=False):
    """
    Go to the next position (next iteration).

    seeking -- Boolean that indicates whether the explorer is calling next()
      from seek(). If True, the explorer should avoid unnecessary computation
      that would not affect the seek command. The last call to next() from
      seek() will be with seeking=False.
    """
    BaseExplorer.next(self)
    self._computeNextPosn()