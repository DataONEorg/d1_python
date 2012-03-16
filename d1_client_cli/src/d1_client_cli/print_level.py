def print_level(level, msg):
  ''' Print the information in as Unicode safe manner as possible.
  '''
  for l in unicode(msg).split(u'\n'):
    msg = u'%s%s' % (u'{0: <8s}'.format(level), unicode(l))
    print msg.encode('utf-8')


def print_debug(msg):
  print_level(u'DEBUG', unicode(msg))


def print_error(msg):
  print_level(u'ERROR', unicode(msg))


def print_warn(msg):
  print_level(u'WARN', unicode(msg))


def print_info(msg):
  print_level(u'', unicode(msg))
