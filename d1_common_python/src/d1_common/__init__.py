#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Shared code for DataONE Python libraries
'''

__version__ = "0.5"

__all__ = [
  'const',
  'exceptions',
  'upload',
  'xmlrunner',
  'types.checksum_serialization',
  'types.identifier_serialization',
  'types.logrecords_serialization',
  'types.monitorlist_serialization',
  'types.nodelist_serialization',
  'types.objectlist_serialization',
  'types.objectlocationlist_serialization',
  'types.statusresponselist_serialization',
  'types.systemmetadata',
  'types.generated.dataoneTypes',
  'ext.mimeparser',
]

MIMETYPES = {'xml': 'text/xml', 'json': 'application/json', 'csv': 'text/csv', }
