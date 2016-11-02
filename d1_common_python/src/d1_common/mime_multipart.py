#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
'''
Module d1_common.mime_multipart
===============================

:Synopsis:
  MIME Multipart document generator. The multipart object is instantiated with
  any number of fields and files, after which the object can be iterated to
  yield the contents as a MIME Multipart document without buffering.
:Created: 2010-09-07
:Author: DataONE (Dahl, Vieglais)
'''

# Stdlib.
import mimetypes
import os
import StringIO

# D1.
import d1_common.const


class MultipartIterator(object):
  '''Generate a MIME Multipart document based on a set of files and fields.

  The document can either be automatically posted to a web server with HTTP
  POST, retrieved in chunks using iteration or retrieved in chunks using the
  read interface.
  '''

  def __init__(self, fields, files, chunk_size=8192):
    '''Constructor for MIME Multipart document generator.
    :param fields: sequence of (name, value) elements for regular form fields
    :type fields: [(string, string), ]
    :param files: sequence of (name, filename, value) elements for data to be
    uploaded as files.
    :type files: [(string, string, file-like object | string), ]
    :param chunk_size: Max number of bytes to return in a single iteration.
    If chunk_size is set lower than a few hundred bytes, chunks that include
    MMP headers and boundaries may exceed this number.
    :type chunk_size: integer
    :returns: None
    '''
    self.chunk_size = chunk_size
    self.fields = fields
    self.files = files
    self.file_idx = 0
    self.state = 'form_fields'
    self.CRLF = '\r\n'
    self.BOUNDARY = '----------6B3C785C-6290-11DF-A355-A6ECDED72085_$'
    self.io = StringIO.StringIO()

  def get_content_length(self):
    '''Get the length, in bytes, of the MIME Multipart document that will be
    generated.

    :returns: length
    :returns type: integer
    '''
    m = MultipartIterator(self.fields, [(f[0], f[1], '') for f in self.files])
    content_length = len(m.read())
    for f in self.files:
      content_length += self._get_len(f)
    self.reset()
    return content_length

  def reset(self):
    '''Reset the mime_multipart object to its initial state.

    This allows the MIME Multipart document to be regenerated from the data with
    which the multipart object was instantiated.

    :returns: None
    '''
    self.file_idx = 0
    self.state = 'form_fields'
    self.io = StringIO.StringIO()

    for f in self.files:
      try:
        f[2].seek(0)
      except (AttributeError, TypeError):
        pass

  def read(self, n=None):
    '''Read a chunk of the generated MIME Multipart document.

    The returned number of bytes will be equal to n for all chunks but the last
    one, which will most likely be smaller. When the method returns an empty
    string, there is no more data to be retrieved.

    If n is None, the entire MIME Multipart document is returned.

    :param n: Minimum number of bytes to read.
    :type n: integer
    :returns: The bytes that were read.
    :returns type: string
    '''
    if n is None:
      # Return everything at once.
      for s in self:
        self.io.write(s)
      return self.io.getvalue()
    else:
      # Return in chunks.

      # "top up" FLO.
      try:
        while True:
          self.io.seek(0, os.SEEK_END)
          if self.io.tell() >= n:
            break
          self.io.write(self.next())
      except StopIteration:
        pass

      # Get n bytes from front of FLO.
      self.io.seek(0)
      ret = self.io.read(n)

      # Remove n bytes from front of FLO.
      self.io = StringIO.StringIO(self.io.read())

    return ret

  def next(self):
    '''Iterate over the multipart object and return the next chunk of MIME
    Multipart data.

    The returned number of bytes will match the chunk_size with which the
    multipart object was instantiated when chunks of files are returned. When
    parts of the MIME Multipart structure is returned, the number of bytes
    returned will be between zero and a few hundred.

    :returns: The next chunk of MIME Multipart data.
    :returns type: string
    '''

    if self.state == 'form_fields':
      if len(self.files) > 0:
        self.state = 'file_head'
      else:
        self.state = 'body_foot'
      return self._form_fields()

    elif self.state == 'file_head':
      self.state = 'select'
      return self._file_head()

    elif self.state == 'select':
      key, filename, val = self.files[self.file_idx]
      if isinstance(val, str):
        self.state = 'str_val'
      else:
        self.state = 'file_chunk'
      return ''

    elif self.state == 'str_val':
      self.state = 'file_foot'
      return self._str_val()

    elif self.state == 'file_chunk':
      data = self._file_chunk()
      if len(data) > 0:
        return data
      self.state = 'file_foot'
      return ''

    elif self.state == 'file_foot':
      self.state = 'next_file'
      return self._file_foot()

    elif self.state == 'next_file':
      self.file_idx += 1
      if self.file_idx < len(self.files):
        self.state = 'file_head'
        return ''
      else:
        self.state = 'body_foot'
        return ''

    elif self.state == 'body_foot':
      self.state = 'body_end'
      return self._body_foot()

    elif self.state == 'body_end':
      raise StopIteration

    else:
      raise Exception('Invalid state in {0}: {1}'.format(__file__, self.state))

  def _get_len(self, file):
    '''Get the length of a file or FLO.

    :param file: File of which to get the length.
    :type file: file object | file-like object
    '''
    try:
      pos = file[2].tell()
      file[2].seek(0, os.SEEK_END)
      size = file[2].tell()
      file[2].seek(pos)
      return size
    except AttributeError:
      return len(file[2])

  def get_content_type_header(self):
    '''Get the contents for the Content-Type header.
    '''
    return 'multipart/form-data; boundary={0}'.format(self.BOUNDARY)

  def _guess_mime_type(self, filename):
    '''Internal method that attempts to map a filename extension to a
    Content-Type.

    :param filename: The name of a file, including extension.
    :type filename: string
    :returns: Mimetype.
    :returns type: string
    '''
    return mimetypes.guess_type(filename)[0] or d1_common.const.CONTENT_TYPE_OCTETSTREAM

  def _form_fields(self):
    '''Generate the MIME Multipart form fields.
    '''
    L = []
    for (key, val) in self.fields:
      L.append('--' + self.BOUNDARY)
      L.append('Content-Disposition: form-data; name="%s"' % key)
      L.append('')
      L.append(val)
    return self.CRLF.join(L) + self.CRLF

  def _file_head(self):
    '''Generate the MIME Multipart header for a file.
    '''
    key, filename, val = self.files[self.file_idx]
    L = []
    L.append('--' + self.BOUNDARY)
    L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
    L.append('Content-Type: %s' % self._guess_mime_type(filename))
    L.append('')
    L.append('')
    return self.CRLF.join(L)

  def _file_chunk(self):
    '''Get a chunk of the file currently being iterated.
    '''
    key, filename, val = self.files[self.file_idx]
    return val.read(self.chunk_size)

  def _file_foot(self):
    '''Get the footer used to designate the end of a file.
    '''
    return self.CRLF

  def _str_val(self):
    '''Get information about the file currently being iterated. Used when the
    file is represented as a string.
    '''
    key, filename, val = self.files[self.file_idx]
    return val

  def _body_foot(self):
    '''Get the footer used to designate the end of the MIME Multipart
    document.
    '''
    L = []
    L.append('--' + self.BOUNDARY + '--')
    L.append('')
    return self.CRLF.join(L)

  def __iter__(self):
    '''Start the iteration. This automatically resets the object so that
    the object can be iterated multiple times and the result is the same
    each time.
    '''
    self.reset()
    return self
