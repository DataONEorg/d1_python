# {{{ http://code.activestate.com/recipes/146306/ (r1)
# With some of the modifications suggested in the user comments.

import os
import httplib
import mimetypes
import urlparse


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


def get_content_type(filename):
  return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
