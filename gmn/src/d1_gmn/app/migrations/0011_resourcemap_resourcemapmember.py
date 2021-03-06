# Generated by Django 1.11.4 on 2017-08-21 21:04


import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [('app', '0010_auto_20170805_0107')]

    operations = [
        migrations.CreateModel(
            name='ResourceMap',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'pid',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='resourcemap_pid',
                        to='app.IdNamespace',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='ResourceMapMember',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'ResourceMap',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='app.ResourceMap',
                    ),
                ),
                (
                    'did',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='resourcemapmember_did',
                        to='app.IdNamespace',
                    ),
                ),
            ],
        ),
    ]
