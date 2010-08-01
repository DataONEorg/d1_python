# {{{ http://code.activestate.com/recipes/146306/ (r1)
# With some of the modifications suggested in the user comments.

import os
import httplib
import mimetypes
import urlparse
import StringIO


def post_multipart_url(url, fields, files):
  urlparts = urlparse.urlsplit(url)
  return post_multipart(urlparts[1], urlparts[2], fields, files)


def post_multipart(host, selector, fields, files):
  '''
  Post fields and files to an http host as multipart/form-data.
  fields is a sequence of (name, value) elements for regular form fields.
  files is a sequence of (name, filename, value) elements for data to be uploaded as files
  Return the server's response page.
  '''
  content_type, body = encode_multipart_formdata(fields, files)
  h = httplib.HTTPConnection(host)
  headers = {'User-Agent': os.path.basename(__file__), 'Content-Type': content_type}
  h.request('POST', selector, body, headers)
  res = h.getresponse()
  return res.status, res.reason, res.read()


def get_content_type(filename):
  return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def encode_multipart_formdata(fields, files):
  '''
  fields is a sequence of (name, value) elements for regular form fields.
  files is a sequence of (name, filename, value) elements for data to be uploaded as files
  Return (content_type, body) ready for httplib.HTTP instance
  '''
  BOUNDARY = '----------6B3C785C-6290-11DF-A355-A6ECDED72085_$'
  CRLF = '\r\n'
  L = []
  for (key, value) in fields:
    L.append('--' + BOUNDARY)
    L.append('Content-Disposition: form-data; name="%s"' % key)
    L.append('')
    L.append(value)
  for (key, filename, value) in files:
    L.append('--' + BOUNDARY)
    L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
    L.append('Content-Type: %s' % get_content_type(filename))
    L.append('')
    L.append(value)
  L.append('--' + BOUNDARY + '--')
  L.append('')
  body = CRLF.join(L)
  content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
  return content_type, body


class multipart_stream(object):
  '''
  Provide file-like object and iterator for a multipart mime object.
  
  fields is a sequence of (name, value) elements for regular form fields.
  files is a sequence of (name, filename, value) elements for data to be uploaded as files
  Return (content_type, body) ready for httplib.HTTP instance

  Create a file iterator that iterates through file-like object using fixed
  size chunks.
  '''

  def __init__(self, fields, files, chunk_size=1024**2):
    self.chunk_size = chunk_size
    self.fields = fields
    self.files = files
    self.file_idx = 0
    self.state = 'body_head'
    self.CRLF = '\r\n'
    self.BOUNDARY = '----------6B3C785C-6290-11DF-A355-A6ECDED72085_$'
    self.io = StringIO.StringIO

  def body_head():
    L = []
    for (key, value) in self.fields:
      L.append('--' + self.BOUNDARY)
      L.append('Content-Disposition: form-data; name="%s"' % key)
      L.append('')
      L.append(value)
    return self.CRLF.join(L)

  def file_head():
    key, filename, value = self.files[file_idx]
    L = []
    L.append('--' + self.BOUNDARY)
    L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
    L.append('Content-Type: %s' % get_content_type(filename))
    L.append('')
    return self.CRLF.join(L)

  def file_chunk():
    key, filename, value = self.files[file_idx]
    return value.read(self.chunk_size)

  def body_foot():
    L.append('--' + self.BOUNDARY + '--')
    L.append('')
    return self.CRLF.join(L)

  def next(self):
    if self.state == 'body_head':
      self.state = 'file_head'
      return body_head()

    if self.state == 'file_head':
      self.state = 'file_chunk'
      return file_head()

    if self.state == 'file_chunk':
      data = file_chunk()
      if data:
        return data
      elif self.file_idx <= len(self.files):
        self.state == 'file_head'
        self.file_idx += 1
      else:
        self.state = 'body_foot'

    if self.state == 'body_foot':
      self.state = 'body_end'
      return foot()

    if self.state == 'body_end':
      raise StopIteration

  def __iter__(self):
    return self

  def read(n):
    try:
      while self.io.tell() < n:
        self.io.write(self.next())
    except StopIteration:
      pass

    buf = self.io.read(n)
    self.io = self.io.read()
    return buf

  def fileno():
    print 'fileno'
    return 0
