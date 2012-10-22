#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
''':mod:`filename_extensions`
=============================

:Synopsis:
 - Map DataONE ObjectFormatIDs to standard filename extensions.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging

# Set up logger for this module.
log = logging.getLogger(__name__)

EXTENSION_FOR_UNKNOWN_OBJECT_FORMAT = 'bin'

object_format_to_filename_extension_map = {
  'eml://ecoinformatics.org/eml-2.0.0': 'xml',
  'eml://ecoinformatics.org/eml-2.0.1': 'xml',
  'eml://ecoinformatics.org/eml-2.1.0': 'xml',
  'FGDC-STD-001.1-1999': 'xml',
  'eml://ecoinformatics.org/eml-2.1.1': 'xml',
  'FGDC-STD-001-1998': 'xml',
  'INCITS 453-2009': 'xml',
  'http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2': 'xml',
  'CF-1.0': 'xml',
  'CF-1.1': 'xml',
  'CF-1.2': 'xml',
  'CF-1.3': 'xml',
  'CF-1.4': 'xml',
  'http://www.cuahsi.org/waterML/1.0/': 'xml',
  'http://www.cuahsi.org/waterML/1.1/': 'xml',
  'http://www.loc.gov/METS/': 'xml',
  'netCDF-3': 'cd3',
  'netCDF-4': 'cd4',
  'text/plain': 'txt',
  'text/csv': 'csv',
  'image/bmp': 'bmp',
  'image/gif': 'gif',
  'image/jp2': 'jp2',
  'image/jpeg': 'jpg',
  'image/png': 'png',
  'image/svg+xml': 'svg',
  'image/tiff': 'tif',
  'http://rs.tdwg.org/dwc/xsd/simpledarwincore/': 'xml',
  'http://digir.net/schema/conceptual/darwin/2003/1.0/darwin2.xsd': 'xml',
  'application/octet-stream': 'bin',
}


def map_object_format_to_filename_extension(object_format_id):
  try:
    return '.' + object_format_to_filename_extension_map[object_format_id]
  except KeyError:
    pass
  return '.' + EXTENSION_FOR_UNKNOWN_OBJECT_FORMAT
