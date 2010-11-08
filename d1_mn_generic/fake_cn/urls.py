from django.conf.urls.defaults import *

urlpatterns = patterns(
  'mn_prototype.fake_cn.views',
  (r'^resolve/(.+)$', 'resolve'),
  (r'^node/?$', 'node'),
)
