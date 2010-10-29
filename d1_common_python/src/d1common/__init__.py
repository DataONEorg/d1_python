#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Shared code for DataONE Python libraries
'''

__version__ = "0.1"
__all__ = [
  'exceptions', 'upload', 'xmlrunner', 'types.generated.logging',
  'types.generated.noderegistry', 'types.generated.objectlist',
  'types.generated.systemmetadata'
]

MIMETYPES = {'xml': 'text/xml', 'json': 'application/json', 'csv': 'text/csv', }
