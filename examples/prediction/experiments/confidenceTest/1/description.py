# ----------------------------------------------------------------------
#  Copyright (C) 2010 Numenta Inc. All rights reserved.
#
#  The information and source code contained herein is the
#  exclusive property of Numenta Inc. No part of this software
#  may be used, reproduced, stored or distributed in any form,
#  without explicit written authorization from Numenta Inc.
# ----------------------------------------------------------------------

"""
Tests the following set of sequences:
a-b-c:      (7X)
a-d-e:      (2X)
a-f-g-a-h:  (1X)

We want to insure that when we see 'a', that we predict 'b' with highest
confidence, then 'd', then 'f' and 'h' with equally low confidence. 

We expect the following input prediction scores:
inputPredScore_at1        :  0.7
inputPredScore_at2        :  1.0
inputPredScore_at3        :  1.0
inputPredScore_at4        :  1.0

"""


from nupic.frameworks.prediction.helpers import importBaseDescription

config = dict(
              sensorVerbosity=0,
              spVerbosity=0,
              tpVerbosity=0,
              ppVerbosity=3,
              
              filenameTrain = 'confidence/confidence1.csv',
              filenameTest = 'confidence/confidence1.csv',

              iterationCountTrain=None,
              iterationCountTest=None,
              trainTPRepeats = 3,
              
              trainTP=True,
              )
              
mod = importBaseDescription('../base/description.py', config)
locals().update(mod.__dict__)


