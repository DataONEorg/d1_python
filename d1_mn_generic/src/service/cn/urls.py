from django.conf.urls.defaults import *

urlpatterns = patterns(
  'service.cn.views',
  (r'^resolve/(.+)$', 'resolve'),
  (r'^node/?$', 'node'),
  (r'^setreplicationstatus/(.*)/(.*)/?$', 'set_replication_status'),
)
