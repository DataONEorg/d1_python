'''Shared code for DataONE Python libraries
'''

__version__ = "0.1"
__all__ = [
  'exceptions', 'upload', 'xmlrunner', 'types.logging', 'types.noderegistry',
  'types.objectlist', 'types.systemmetadata'
]

MIMETYPES = {'xml': 'text/xml', 'json': 'application/json', 'csv': 'text/csv', }
