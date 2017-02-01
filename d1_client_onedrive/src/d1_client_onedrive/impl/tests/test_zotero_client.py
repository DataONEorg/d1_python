#!/usr/bin/env python

# Stdlib
import logging
import os
from pprint import pprint
import shutil
import sys
import unittest

# 3rd party
from pyzotero import zotero

# D1
sys.path.append('../..')
import command_echoer
import impl.clients.onedrive_zotero_client as onedrive_zotero_client
from object_tree_test_sample import object_tree

options = {}

# Zotero authentication. Set environment variables ZOTERO_USER and
# ZOTERO_API_ACCESS_KEY.

# Check "Allow write access" on the "Edit Key" page on Zotero.org.


class TestZoteroClient(unittest.TestCase):
  def _show_object_tree(self, zotero_client):
    #pprint.pprint(zotero_client.collections())
    #pprint.pprint(zotero_client.collections_sub(''))
    pprint.pprint(arrange_collections_into_tree(zotero_client))

  def _arrange_collections_into_tree(self, zotero_client):
    # Since Python creates references instead of copies when objects are appended
    # to a list, the tree can be built with a single pass plus a bit of
    # housekeeping.
    c = zotero_client.collections()
    t = dict((e['collectionKey'], e) for e in c)
    for e in c:
      e['children'] = []
    for e in c:
      if e['parent']:
        t[e['parent']]['children'].append(e)
    # Now have many trees. Return the one that starts at root.
    for e in c:
      if not e['parent']:
        return e

  def _copy_object_tree_to_zotero(self, zotero_client):
    with object_tree.ObjectTree() as object_tree_client:
      copy_dirs_recursive(zotero_client, object_tree_client, None, [])

  def _copy_dirs_recursive(
    self, zotero_client, object_tree_client, zotero_collection, object_tree_path
  ):
    object_tree_folder = object_tree_client.get_folder(object_tree_path)
    print object_tree_folder['name']
    collection = zotero_create_collection(
      zotero_client, zotero_collection, object_tree_folder['name']
    )
    for pid in object_tree_folder['items']:
      zotero_create_item(zotero_client, collection, pid)
    for d in object_tree_folder['dirs']:
      copy_dirs_recursive(
        zotero_client, object_tree_client, collection, object_tree_path + [
          d
        ]
      )

  def _zotero_create_collection(self, zotero_client, zotero_collection, name):
    params = {'name': name}
    if zotero_collection is not None:
      params['parent'] = zotero_collection['collectionKey']
    zotero_client.create_collection(params)
    return zotero_client.collections()[0]

  def _zotero_create_item(self, zotero_client, zotero_collection, pid):
    template = zotero_client.item_template('book')
    template['creators'][0]['firstName'] = 'DataONE'
    template['creators'][0]['lastName'] = ''
    template['title'] = pid
    item_with_key = zotero_client.create_items([template])
    zotero_client.addto_collection(zotero_collection['collectionKey'], item_with_key)

  def _print_zotero_types(self, zotero_client):
    for i in zotero_client.item_types():
      print
      print i['localized']
      for j in zotero_client.item_type_fields(i['itemType']):
        print ' ', j['localized']

  def setUp(self):
    self.options = {'zotero_cache_root': '.', 'zotero_cache_path': 'zotero.pickle', }
    self.pickle_path = os.path.join(
      self.options['zotero_cache_root'], self.options['zotero_cache_path']
    )

  def _zotero_delete_all(zotero_client):
    while True:
      items = zotero_client.items()
      if not items:
        break
      for i in items:
        print i['title'].encode('utf8')
        zotero_client.delete_item(i)

  #def test_100(self):
  #  """Create Zotero Cache with defaults, non-existing pickle"""
  #  try:
  #    os.unlink(self.pickle_path)
  #  except OSError as e:
  #    if e.errno == 2: # [Errno 2] No such file or directory
  #      pass
  #  with onedrive_zotero_client.ZoteroClient(self.options) as z:
  #    pass
  #
  #
  #def test_110(self):
  #  """Check that pickle was written to disk"""
  #  self.assertTrue(os.path.exists(self.pickle_path))
  #
  #
  #def test_120(self):
  #  """Check that empty pickle object is unpickled correctly"""
  #  with onedrive_zotero_client.ZoteroClient(self.options) as z:
  #    self.assertEqual(z._cache['filtered_tree'], {})
  #    self.assertEqual(z._cache['collections'], None)
  #    self.assertEqual(z._cache['library_version'], 0)
  #
  #
  #def test_130(self):
  #  """refresh()"""
  #  with onedrive_zotero_client.ZoteroClient(self.options) as z:
  #    self.assertEqual(z._cache['library_version'], 0)
  #    z.refresh()
  #    self.assertTrue(z._cache['library_version'] > 0)
  #
  #
  #def test_140(self):
  #  """get_filtered_sub_tree([])"""
  #  with onedrive_zotero_client.ZoteroClient(self.options) as z:
  #    z.get_filtered_sub_tree([])
  #
  #
  #def test_150(self):
  #  """get_filtered_sub_tree(['c1', 'c3'])"""
  #  with onedrive_zotero_client.ZoteroClient(self.options) as z:
  #    z.get_filtered_sub_tree(['c1', 'c3'])
  #
  #
  #def test_160(self):
  #  """iterate_collection_trees()"""
  #  with onedrive_zotero_client.ZoteroClient(self.options) as z:
  #    z.refresh()
  #    for a, b in z.iterate_collection_trees():
  #      self.assertTrue(type(a) is dict)
  #      self.assertTrue(type(b) is list)

  #===============================================================================


def log_setup():
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(module)s %(message)s', '%Y-%m-%d %H:%M:%S'
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  import optparse

  log_setup()

  # Command line opts.
  parser = optparse.OptionParser()
  parser.add_option('--debug', action='store_true', default=False, dest='debug')
  parser.add_option(
    '--test', action='store',
    default='',
    dest='test',
    help='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestZoteroClient
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
