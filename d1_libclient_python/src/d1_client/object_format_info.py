#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''Module object_format_info
============================

:Synopsis:
  Map DataONE ObjectFormatIDs to mimetype and filename extension.
  The mappings are provided in a CSV file.
:Created: 2012-10-25
:Author: DataONE (Dahl)
'''

# Stdlib.
import csv
import logging
import os
import sys

# App.
import d1baseclient


def make_absolute(p):
  return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)

# Config
MIME_MAPPINGS_CSV_PATH = make_absolute('mime_mappings.csv')


class Singleton(object):
  _instances = {}

  def __new__(class_, *args, **kwargs):
    if class_ not in class_._instances:
      class_._instances[class_] = super(Singleton, class_)\
        .__new__(class_, *args, **kwargs)
    return class_._instances[class_]

#===============================================================================


class ObjectFormatInfo(Singleton):
  def __init__(self, csv_file=None):

    if csv_file is None:
      self.csv_path = MIME_MAPPINGS_CSV_PATH
      self.csv_file = None
    else:
      self.csv_path = None
      self.csv_file = csv_file

    self.reread_csv_file()

  def mimetype_from_format_id(self, format_id):
    return self._get_format_id_entry(format_id)[0]

  def filename_extension_from_format_id(self, format_id):
    return self._get_format_id_entry(format_id)[1]

  def reread_csv_file(self, csv_path=None):
    if csv_path is not None:
      self.csv_path = csv_path
    self.format_id_map = self._create_format_id_map_from_csv_file()

  def _read_format_id_map_from_file(self, file):

    csv_reader = csv.reader(file)

    try:
      return dict((r[0], r[1:]) for r in csv_reader)

    except (csv.Error, Exception) as e:
      raise Exception(
        'Error in CSV file. Line: {1}  Error: {2}'.format(csv_reader.line_num, e)
      )

  def _create_format_id_map_from_csv_file(self):

    if self.csv_path is not None:
      try:
        with open(self.csv_path) as f:
          return self._read_format_id_map_from_file(f)

      except IOError as e:
        raise Exception(
          'Unable to open CSV file: {0}. Error: {1}: {2}'
          .format(self.csv_path, e.errno, e.strerror)
        )

    else:
      try:
        self.csv_file.seek(0)
        return self._read_format_id_map_from_file(self.csv_file)

      except IOError as e:
        raise Exception(
          'Unable to read from file object: Error: {1}: {2}'.format(e.errno, e.strerror)
        )

  def _get_format_id_entry(self, format_id):
    return self.format_id_map[format_id]
