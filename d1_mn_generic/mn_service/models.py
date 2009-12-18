from django.db import models


class repository_object_class(models.Model):
  # "id" serial NOT NULL PRIMARY KEY (created automatically)
  name = models.CharField(max_length=10)


class repository_object(models.Model):
  # "id" serial NOT NULL PRIMARY KEY (created automatically)
  guid = models.CharField(max_length=200, unique=True)
  repository_object_class = models.ForeignKey(repository_object_class)
  hash = models.CharField(max_length=100)
  mtime = models.DateTimeField()
  size = models.PositiveIntegerField()
