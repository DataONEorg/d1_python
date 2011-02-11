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
  (r'^test/?$', 'test'),

  # Status

  # test_get_replication_status (optional pid)
  (r'^test_get_replication_status/?$', 'test_get_replication_status'),
  # test_get_replication_status_xml (optional pid)
  (r'^test_get_replication_status_xml/?$', 'test_get_replication_status_xml'),
  # /test_get_sysmeta/<pid>
  (r'^test_get_sysmeta/(.*)/?$', 'test_get_sysmeta'),

  # Create and Update

  # /test_replicate/<src_node_ref>/<pid>
  (r'^test_replicate/(.*)/(.*)/?$', 'test_replicate'),
  # /test_set_replication_status_put/<status>/<node>/<pid>
  (
    r'^test_set_replication_status_get/(.*)/(.*)/(.*)/?$',
    'test_set_replication_status_get'
  ),

  # Delete

  # Remove Replica entries from SysMeta.
  # test_clear_replication_status/<optional node_ref>/<optional pid>
  (r'^test_clear_replication_status/(.*)/(.*)/?$', 'test_clear_replication_status'),
)
