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
  'types.logrecords_serialization',
  'types.monitorlist_serialization',
  'types.nodelist_serialization',
  'types.objectlist_serialization',
  'types.objectlocationlist_serialization',
  'types.statusresponselist_serialization',
  'types.systemmetadata',
  'types.generated._common',
  'types.generated.logging',
  'types.generated.monitorlist',
  'types.generated.nodelist',
  'types.generated.noderegistry',
  'types.generated.objectlist',
  'types.generated.objectlocationlist',
  'types.generated.statusresponselist',
  'types.generated.systemmetadata',
  'ext.mimeparser',
]

MIMETYPES = {'xml': 'text/xml', 'json': 'application/json', 'csv': 'text/csv', }
