# ----------------------------------------------------------------------
#  Copyright (C) 2011 Numenta Inc. All rights reserved.
#
#  The information and source code contained herein is the
#  exclusive property of Numenta Inc. No part of this software
#  may be used, reproduced, stored or distributed in any form,
#  without explicit written authorization from Numenta Inc.
# ----------------------------------------------------------------------

# This script is a wrapper for JSON primitives, such as validation.
# Using routines of this module permits us to replace the underlying
# implementaiton with a better one without distrupting client code.
#
# In particular, at the time of this writing, there weren't really great
# json validation packages available for python.  We initially settled
# on validictory, but it has a number of shortcomings, such as:
#   * format error diagnostic message isn't always helpful for diagnosis
#   * doesn't support references
#   * doesn't support application of defaults
#   * doesn't support dependencies
#
# TODO: offer a combined json parsing/validation function that applies
#       defaults from the schema

import math
import os
import json

import validictory


class ValidationError(Exception):
  """ Raised when the given value fails the validate() test
  """


class NaNInvalidator(validictory.SchemaValidator):
  """ validictory.SchemaValidator subclass to not accept NaN values as numbers.

  Usage:

      validate(value, schemaDict, validator_cls=NaNInvalidator)

  """
  def validate_type_number(self, val):
    return not math.isnan(val) \
      and super(NaNInvalidator, self).validate_type_number(val)



###############################################################################
def validate(value, **kwds):
  """ Validate a python value against json schema:
  validate(value, schemaPath)
  validate(value, schemaDict)

  value:          python object to validate against the schema

  The json schema may be specified either as a path of the file containing
  the json schema or as a python dictionary using one of the
  following keywords as arguments:
    schemaPath:     Path of file containing the json schema object.
    schemaDict:     Python dictionary containing the json schema object

  Returns: nothing

  Raises:
          ValidationError when value fails json validation
  """

  assert len(kwds.keys()) >= 1
  assert 'schemaPath' in kwds or 'schemaDict' in kwds

  schemaDict = None
  if 'schemaPath' in kwds:
    schemaPath = kwds.pop('schemaPath')
    schemaDict = loadJsonValueFromFile(schemaPath)
  elif 'schemaDict' in kwds:
    schemaDict = kwds.pop('schemaDict')

  try:
    validictory.validate(value, schemaDict, **kwds)
  except validictory.ValidationError as e:
    raise ValidationError(e)



###############################################################################
def loadJsonValueFromFile(inputFilePath):
  """ Loads a json value from a file and converts it to the corresponding python
  object.

  inputFilePath:
                  Path of the json file;

  Returns:
                  python value that represents the loaded json value

  """
  fileObj = open(inputFilePath)

  value = json.load(fileObj)

  fileObj.close()
  del fileObj

  return value



###############################################################################
def test():
  """
  """
  import sys

  schemaDict = {
    "description":"JSON schema for jsonhelpers.py test code",
    "type":"object",
    "additionalProperties":False,
    "properties":{
      "myBool":{
        "description":"Some boolean property",
        "required":True,
        "type":"boolean"
      }
    }
  }

  d = {
    'myBool': False
  }

  print "Validating schemaDict method in positive test..."
  validate(d, schemaDict=schemaDict)
  print "ok\n"

  print "Validating schemaDict method in negative test..."
  try:
    validate({}, schemaDict=schemaDict)
  except ValidationError:
    print "ok\n"
  else:
    print "FAILED\n"
    sys.exit(1)


  schemaPath = os.path.join(os.path.dirname(__file__), "testSchema.json")
  print "Validating schemaPath method in positive test using %s..." % \
            (os.path.abspath(schemaPath),)
  validate(d, schemaPath=schemaPath)
  print "ok\n"

  print "Validating schemaPath method in negative test using %s..." % \
            (os.path.abspath(schemaPath),)
  try:
    validate({}, schemaPath=schemaPath)
  except ValidationError:
    print "ok\n"
  else:
    print "FAILED\n"
    sys.exit(1)



  return



###############################################################################
if __name__ == "__main__":
  test()