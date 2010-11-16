from django.conf.urls.defaults import *

urlpatterns = patterns(
  'service.fake_cn.views',
  (r'^resolve/(.+)$', 'resolve'),
  (r'^node/?$', 'node'),
)
