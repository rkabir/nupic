# ----------------------------------------------------------------------
#  Copyright (C) 2006-2008 Numenta Inc. All rights reserved.
#
#  The information and source code contained herein is the
#  exclusive property of Numenta Inc. No part of this software
#  may be used, reproduced, stored or distributed in any form,
#  without explicit written authorization from Numenta Inc.
# ----------------------------------------------------------------------

"""
This file defines RotatePictureExplorer, an explorer for
PictureSensor.
"""

from nupic.regions.PictureSensor import PictureSensor

#+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
# RotatePictureExplorer

class RotatePictureExplorer(PictureSensor.PictureExplorer):

  @classmethod
  def queryRelevantParams(klass):
    """
    Returns a sequence of parameter names that are relevant to
    the operation of the explorer.

    May be extended or overridden by sub-classes as appropriate.
    """
    return super(RotatePictureExplorer, klass).queryRelevantParams() + \
           ( 'radialLength', 'radialStep' )

  def initSequence(self, state, params):
    self._presentNextRotation(state, params)


  def updateSequence(self, state, params):
    self._presentNextRotation(state, params)


  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Internal helper method(s)

  def _presentNextRotation(self, state, params):
    """
    We will visit each grid position. For each grid position,
    we rotate the object in 2D
    """

    # Compute iteration indices
    numRotations = 1 + int((params['maxAngularPosn'] - params['minAngularPosn'])
                           / params['minAngularVelocity'])
    edgeLen = 2 * params['radialLength'] + 1
    numItersPerCat = edgeLen * edgeLen * numRotations
    numCats = self._getNumCategories()
    numIters = numItersPerCat * numCats
    catIndex = self._getIterCount() // numItersPerCat
    index = self._getIterCount() % numItersPerCat
    blockIndex = index / numRotations
    rotationIndex = index % numRotations

    # Compute position within onion block
    posnX = ((blockIndex % edgeLen) - params['radialLength']) * params['radialStep']
    posnY = ((blockIndex // edgeLen) - params['radialLength']) * params['radialStep']

    # Compute rotation angle
    angularPosn = params['maxAngularPosn'] - params['minAngularVelocity'] * rotationIndex

    # Update state
    state['posnX'] = posnX
    state['posnY'] = posnY
    state['velocityX'] = 0
    state['velocityY'] = 0
    state['angularVelocity'] = params['minAngularVelocity']
    state['angularPosn'] = angularPosn
    state['catIndex'] = catIndex