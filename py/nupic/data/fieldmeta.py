# ----------------------------------------------------------------------
#  Copyright (C) 2011 Numenta Inc. All rights reserved.
#
#  The information and source code contained herein is the
#  exclusive property of Numenta Inc. No part of this software
#  may be used, reproduced, stored or distributed in any form,
#  without explicit written authorization from Numenta Inc.
# ----------------------------------------------------------------------


# This script defines the structure of meta-data that describes the field name,
# field type, special field attribute, etc. for a field in a dataset


from collections import namedtuple



###############################################################################
FieldMetaInfoBase = namedtuple('FieldMetaInfoBase', ['name', 'type', 'special'])

class FieldMetaInfo(FieldMetaInfoBase):
  """
  This class acts as a container of meta-data for a single field (column) of
  a dataset.

  The layout is backward-compatible with the tuples exposed via the 'fields'
  attribute of the legacy nupic.data.file.File class (in file.py). However, the
  elements may be accessed in a less error-prone and more self-documenting way
  using object attribute notation (e.g., fieldmeta.special instead of
  fieldmeta[2]). Because namedtuple creates a subclass of tuple, the elements
  can also be accessed using list access semantics and operations (i.e.,
  fieldmeta[2])

  Examples:

  1. Access a sub-element from an instance of FieldMetaInfo:
        metainfo.name
        metainfo.type
        metainfo.special

  2. Convert a single element from nupic.data.file.File.fields to FieldMetaInfo
        e = ('pounds', FieldMetaType.float, FieldMetaSpecial.none)
        m = FieldMetaInfo.createFromFileFieldElement(e)

  3.
  """

  @staticmethod
  def createFromFileFieldElement(fieldInfoTuple):
    """ Creates a FieldMetaInfo instance from an element of the File.fields list
    of a nupic.data.file.File class instance.
    """
    return FieldMetaInfo._make(fieldInfoTuple)


  @classmethod
  def createListFromFileFieldList(cls, fields):
    """ Creates a FieldMetaInfo list from the File.fields value of a
    nupic.data.file.File class instance.

    fields: a sequence of field attribute tuples conforming to the format
    of the File.fields attribute of a nupic.data.file.File class instance.

    Returns:  A list of FieldMetaInfo elements corresponding to the given
              'fields' list.
    """
    return map(lambda x: cls.createFromFileFieldElement(x), fields)



class FieldMetaType(object):
  """
  Public values for the field data types
  """
  string = 'string'
  datetime = 'datetime'
  integer = 'int'
  float = 'float'
  boolean = 'bool'


class FieldMetaSpecial(object):
  """
  Public values for the "special" field attribute
  """
  none = ''
  reset = 'R'
  sequence = 'S'
  timestamp = 'T'
  category = 'C'




###############################################################################
def test():
  """
  """
  # Create a single FieldMetaInfo instance from a File field's meta-data tuple
  e = ('pounds', FieldMetaType.float, FieldMetaSpecial.none)
  m = FieldMetaInfo.createFromFileFieldElement(e)
  print "COMPARING %s WITH %s..." % (e, m)
  assert e == m
  print "ok\n"

  # Create a list of FieldMetaInfo instances from a list of File meta-data tuples
  el = [('pounds', FieldMetaType.float, FieldMetaSpecial.none),
        ('price', FieldMetaType.float, FieldMetaSpecial.none),
        ('id', FieldMetaType.string, FieldMetaSpecial.sequence),
        ('date', FieldMetaType.datetime, FieldMetaSpecial.timestamp),
       ]
  ml = FieldMetaInfo.createListFromFileFieldList(el)
  print "COMPARING %s WITH %s..." % (el, ml)
  assert el == ml
  print "ok"

  return


###############################################################################
if __name__ == "__main__":
  test()