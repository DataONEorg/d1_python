# #!/usr/bin/env python
#
# # This work was created by participants in the DataONE project, and is
# # jointly copyrighted by participating institutions in DataONE. For
# # more information on DataONE, see our web site at http://dataone.org.
# #
# #   Copyright 2009-2017 DataONE
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #   http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
#
# from __future__ import absolute_import
# from __future__ import print_function
#
# import logging
# import os
#
# import d1_onedrive.impl.clients.onedrive_zotero_client as zotero_client
# import pytest
#
# import d1_test.d1_test_case
#
# options = {}
#
# # Zotero authentication. Set environment variables ZOTERO_USER and
# # ZOTERO_API_ACCESS_KEY.
#
# # Check "Allow write access" on the "Edit Key" page on Zotero.org.
#
#
# class TestZoteroClient(d1_test.d1_test_case.D1TestCase):
#   def setup_method(self):
#     self.options = {
#       'zotero_cache_root': '.',
#       'zotero_cache_path': 'zotero.pickle',
#     }
#     self.pickle_path = os.path.join(
#       self.options['zotero_cache_root'], self.options['zotero_cache_path']
#     )
#
#   def _show_object_tree(self, zotero_client):
#     # pprint.pprint(zotero_client.collections())
#     # pprint.pprint(zotero_client.collections_sub(''))
#     # pprint.pprint(arrange_collections_into_tree(zotero_client))
#     pass
#
#   def _arrange_collections_into_tree(self, zotero_client):
#     # Since Python creates references instead of copies when objects are appended
#     # to a list, the tree can be built with a single pass plus a bit of
#     # housekeeping.
#     c = zotero_client.collections()
#     t = dict((e['collectionKey'], e) for e in c)
#     for e in c:
#       e['children'] = []
#     for e in c:
#       if e['parent']:
#         t[e['parent']]['children'].append(e)
#     # Now have many trees. Return the one that starts at root.
#     for e in c:
#       if not e['parent']:
#         return e
#
#   def _copy_object_tree_to_zotero(self, zotero_client):
#     # with object_tree.ObjectTree() as object_tree_client:
#     #   copy_dirs_recursive(zotero_client, object_tree_client, None, [])
#     pass
#
#   def _zotero_create_collection(self, zotero_client, zotero_collection, name):
#     params = {'name': name}
#     if zotero_collection is not None:
#       params['parent'] = zotero_collection['collectionKey']
#     zotero_client.create_collection(params)
#     return zotero_client.collections()[0]
#
#   def _zotero_create_item(self, zotero_client, zotero_collection, pid):
#     template = zotero_client.item_template('book')
#     template['creators'][0]['firstName'] = 'DataONE'
#     template['creators'][0]['lastName'] = ''
#     template['title'] = pid
#     item_with_key = zotero_client.create_items([template])
#     zotero_client.addto_collection(
#       zotero_collection['collectionKey'], item_with_key
#     )
#
#   def _log_zotero_types(self, zotero_client):
#     for i in zotero_client.item_types():
#       logging.debug('')
#       logging.debug(i['localized'])
#       for j in zotero_client.item_type_fields(i['itemType']):
#         logging.debug(' ', j['localized'])
#
#   def _zotero_delete_all(zotero_client):
#     while True:
#       items = zotero_client.items()
#       if not items:
#         break
#       for i in items:
#         logging.debug(i['title'].encode('utf-8'))
#         zotero_client.delete_item(i)
#
#   def test_1000(self):
#     """Create Zotero Cache with defaults, non-existing pickle"""
#     try:
#       os.unlink(self.pickle_path)
#     except OSError as e:
#       if e.errno == 2: # [Errno 2] No such file or directory
#         pass
#     with zotero_client.ZoteroClient(self.options):
#       pass
#
#   #
#   #
#   #def test_110(self):
#   #  """Check that pickle was written to disk"""
#   #  self.assertTrue(os.path.exists(self.pickle_path))
#   #
#   #
#   #def test_120(self):
#   #  """Check that empty pickle object is unpickled correctly"""
#   #  with onedrive_zotero_client.ZoteroClient(self.options) as z:
#   #    self.assertEqual(z._cache['filtered_tree'], {})
#   #    self.assertEqual(z._cache['collections'], None)
#   #    self.assertEqual(z._cache['library_version'], 0)
#   #
#   #
#   #def test_130(self):
#   #  """refresh()"""
#   #  with onedrive_zotero_client.ZoteroClient(self.options) as z:
#   #    self.assertEqual(z._cache['library_version'], 0)
#   #    z.refresh()
#   #    self.assertTrue(z._cache['library_version'] > 0)
#   #
#   #
#   #def test_140(self):
#   #  """get_filtered_sub_tree([])"""
#   #  with onedrive_zotero_client.ZoteroClient(self.options) as z:
#   #    z.get_filtered_sub_tree([])
#   #
#   #
#   #def test_150(self):
#   #  """get_filtered_sub_tree(['c1', 'c3'])"""
#   #  with onedrive_zotero_client.ZoteroClient(self.options) as z:
#   #    z.get_filtered_sub_tree(['c1', 'c3'])
#   #
#   #
#   #def test_160(self):
#   #  """iterate_collection_trees()"""
#   #  with onedrive_zotero_client.ZoteroClient(self.options) as z:
#   #    z.refresh()
#   #    for a, b in z.iterate_collection_trees():
#   #      self.assertTrue(type(a) is dict)
#   #      self.assertTrue(type(b) is list)
#
#   #===============================================================================
