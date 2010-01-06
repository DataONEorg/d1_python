from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
  'mn_prototype.mn_service.views',
  (r'^object/(.*)/meta$', 'object_meta'),
  (r'^object/(.*)$', 'object'),
  (r'^update/$', 'update'),
  (r'^log/$', 'log'),
  (r'^admin/doc/', include('django.contrib.admindocs.urls')),
  (r'^admin/', include(admin.site.urls)),
)
