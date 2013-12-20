'''
Check subversion revision of the tree in which this file is contained
and returns that value or the statically set value on failure.
'''

import os
import logging

_default_revision = "3445" ##TAG

# Set up logger for this module.
log = logging.getLogger(__name__)
# Set specific logging level for this module if specified.
try:
  log.setLevel(logging.getLevelName(logging.ONEDRIVE_MODULES[__name__]))
except (KeyError, AttributeError):
  pass


def getSvnRevision(update_static=False):
  '''If update_static then attempt to modify this source file with the current
  svn revision number.
  '''
  rev = _default_revision
  try:
    import pysvn
    here = os.path.abspath(os.path.dirname(__file__))
    cli = pysvn.Client()
    rev = str(cli.info(here).revision.number)
    if update_static and rev != _default_revision:
      #Try to update the static revision number - requires file write permission
      try:
        import codecs
        tf = codecs.open(os.path.abspath(__file__), 'r', 'utf-8')
        content = tf.read()
        tf.close()
        content = content.replace(u'_default_revision="%s" ##TAG' % \
                                    _default_revision,
                                  u'_default_revision="%s" ##TAG' % rev, 1 )
        logging.info("Setting revision in %s to %s" % \
                       (os.path.abspath(__file__), rev) )
        tf = codecs.open(os.path.abspath(__file__), 'w', 'utf-8')
        tf.write(content)
        tf.close()
      except Exception, e:
        logging.exception(e)
  except:
    logging.error("pysvn not available for revision information.")
  return rev


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  ver = getSvnRevision(update_static=True)
  print "svn:%s" % ver
