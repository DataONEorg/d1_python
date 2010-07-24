'''
Simple client for DataONE demonstrating a couple of core operations.
'''
import sys
import logging
import datetime
import dateutil.parser
from optparse import OptionParser
import d1common.types.logrecords_serialization
from d1pythonitk.client import DataOneClient
from d1pythonitk.objectlistiterator import ObjectListIterator
from d1pythonitk.logrecorditerator import LogRecordIterator

if __name__ == '__main__':
  yesterday = datetime.datetime.now() - datetime.timedelta(1)
  parser = OptionParser()
  operations = ['list', 'meta', 'get', 'formats', 'log']
  parser.add_option(
    "-t",
    "--target",
    dest="target",
    help="Target Node",
    default="http://dev-dryad-mn.dataone.org/mn"
  )
  parser.add_option(
    "-o",
    "--operation",
    dest="operation",
    help="Operation: %s" % ", ".join(operations),
    default=None
  )
  parser.add_option(
    "-i",
    "--id",
    dest="identifier",
    help="Identifier for meta and get operations",
    default=None
  )
  parser.add_option(
    "-v",
    "--verbosity",
    dest="loglevel",
    help="1=DEBUG, 2=INFO, 3=WARN, 4=ERROR, 5=FATAL",
    default=3,
    type="int"
  )
  parser.add_option(
    "-s",
    "--start",
    dest="startdate",
    help="Starting date, YYYY-MM-DD for log or list.",
    default=yesterday.isoformat()
  )
  (options, args) = parser.parse_args()
  if options.loglevel < 1:
    options.loglevel = 1
  if options.loglevel > 5:
    options.loglevel = 5
  logging.basicConfig(level=options.loglevel * 10)
  op = options.operation
  if op is None or op.lower() not in operations:
    print "Error: operation is required\n"
    parser.print_help()
    sys.exit()
  try:
    startdate = dateutil.parser.parse(options.startdate)
  except:
    logging.warn('"%s" could not be parsed as start date' % options.startdate)
    startdate = None
  op = op.lower()
  client = DataOneClient(options.target)
  if op == 'get':
    res = client.get(options.identifier)
    print res.read()
  elif op == 'meta':
    res = client.getSystemMetadata(options.identifier)
    print res.toxml()
  elif op == 'list':
    logging.info('List objects, startTime=%s' % startdate.isoformat())
    object_list = ObjectListIterator(client, startTime=startdate)
    print "#Found %d entries." % len(object_list)
    print "ID,format,size"
    for obj in object_list:
      print "%s,%s,%s" % (obj.identifier, obj.objectFormat, str(obj.size))
  elif op == 'formats':
    formats = client.enumerateObjectFormats()
    print "count, format"
    for k in formats.keys():
      print "%s, %s" % (str(formats[k]), k)
  elif op == 'log':
    logging.info('Log records, startTime=%s' % startdate.isoformat())
    log_records = LogRecordIterator(client, startTime=startdate)
    for entry in log_records:
      print d1common.types.logrecords_serialization.logEntryToText(entry)
