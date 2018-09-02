import django.db.migrations
import django.db.models
import d1_gmn.app.models
import d1_gmn.app.sciobj_store

def abs_to_relative_file_url(apps, schema_editor):
  d1_gmn.app.models.ScienceObject.objects.update(
    url=django.db.models.Func(
      django.db.models.F('url'),
      django.db.models.Value('file:///'),
      django.db.models.Value(
        'file://{}/'.format(d1_gmn.app.sciobj_store.RELATIVE_PATH_MAGIC_HOST_STR)
      ),
      function='replace',
    )
  )


class Migration(django.db.migrations.Migration):
  dependencies = [
    ('app', '0016_auto_20180518_1539'),
  ]

  operations = [
    # django.db.migrations.RunPython(
    #   abs_to_relative_file_url, reverse_code=django.db.migrations.RunPython.noop
    # ),
  ]
