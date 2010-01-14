from django.db import models

# Django creates automatically:
# "id" serial NOT NULL PRIMARY KEY


class status(models.Model):
  mtime = models.DateTimeField()
  status = models.CharField(max_length=100)


class repository_object_class(models.Model):
  name = models.CharField(max_length=10)


class repository_object(models.Model):
  guid = models.CharField(max_length=200, unique=True)
  path = models.CharField(max_length=1000, unique=True)
  repository_object_class = models.ForeignKey(repository_object_class)
  hash = models.CharField(max_length=100)
  mtime = models.DateTimeField()
  size = models.PositiveIntegerField()


# TODO: Set up a unique index for the from_object / to_object combination.
class associations(models.Model):
  from_object = models.ForeignKey(repository_object, related_name='associations_from')
  to_object = models.ForeignKey(repository_object, related_name='associations_to')
