""":mod:`models` -- URLs
========================

:module: urls
:platform: Linux
:synopsis: URLs

.. moduleauthor:: Roger Dahl
"""

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
  '',
  # Example:
  (r'^mn/', include('mn_prototype.mn_service.urls')),
  (
    r'^accounts/login/$', 'django.contrib.auth.views.login'
  ),

  # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
  # to INSTALLED_APPS to enable admin documentation:
  # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
  # (r'^admin/', include(admin.site.urls)),
)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
# Create system metadata object.
#register_object_create_sysmeta(item, object_tree, object_contents)

#  
#  # Create sysmeta for object.
#  sysmeta_guid = str(uuid.uuid4())
#  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
#  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
#  if not res:
#    util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' % object_path)
# 
#  # Create db entry for sysmeta object.
#  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
#
#  # Create association between sysmeta and regular object.
#  mn_service.util.insert_association(object_guid, sysmeta_guid)
