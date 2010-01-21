#!/usr/bin/env python


def file_to_dict(path):
  """
  Convert a sample MN object to dictionary.
  """
  try:
    f = open(path, 'r')
  except IOError, e:
    logging.error('Internal server error: Could not open: %s:\nException: %s' % [path, e])
    return HttpResponseServerError()

  d = {}

  for line in f:
    m = re.match(r'(.+?):(.+)', f)
    if m:
      d[m.group(1)] = m.group(2)

  f.close()

  return d
