""":mod:`models` -- Models
==========================

:module: models
:platform: Linux
:synopsis: Models

.. moduleauthor:: Roger Dahl
"""

from django.db import models

# Django creates automatically:
# "id" serial NOT NULL PRIMARY KEY


class status(models.Model):
  """Status of the most recent database update attempt"""

  mtime = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=100)


class repository_object_class(models.Model):
  """Object class of objects"""

  name = models.CharField(max_length=10)


class repository_object(models.Model):
  """Hold MN objects"""

  guid = models.CharField(max_length=200, unique=True)
  path = models.CharField(max_length=1000, unique=True)
  repository_object_class = models.ForeignKey(repository_object_class)
  hash = models.CharField(max_length=100)
  object_mtime = models.DateTimeField()
  db_mtime = models.DateTimeField(auto_now=True)
  size = models.PositiveIntegerField()


# TODO: Set up a unique index for the from_object / to_object combination.
class associations(models.Model):
  """Associations between MN objects"""

  from_object = models.ForeignKey(repository_object, related_name='associations_from')
  to_object = models.ForeignKey(repository_object, related_name='associations_to')


class sync(models.Model):
  """Synchronization status for MN objects"""

  repository_object = models.ForeignKey(repository_object, related_name='sync')
  mtime = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=100)
