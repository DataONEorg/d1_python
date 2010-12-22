from django.conf.urls.defaults import *

urlpatterns = patterns(
  'service.cn.views',
  (r'^resolve/(.+)$', 'resolve'),
  (r'^node/?$', 'node'),
  (r'^setreplicationstatus/(.*)/(.*)/(.*)/?$',
   'set_replication_status'), # status, node, pid

  #
  # Testing.
  #
  (
    r'^test_set_replication_status_put/(.*)/(.*)/(.*)/?$',
    'test_set_replication_status_put'
  ), # status, node, pid
  (r'^test_get_sysmeta/(.*)/?$', 'test_get_sysmeta'), # pid
  (r'^test_get_replication_status/(.*)/?$', 'test_get_replication_status'), # optional pid
  (r'^test_get_replication_status_xml/(.*)/?$',
   'test_get_replication_status_xml'), # optional pid

  # Remove Replica entries from SysMeta.
  # Params: optional node_ref, optional pid
  (r'^test_clear_replication_status/(.*)/(.*)/?$', 'test_clear_replication_status'),
)
