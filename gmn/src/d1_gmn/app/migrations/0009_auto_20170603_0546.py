# Generated by Django 1.11.1 on 2017-06-03 05:46


import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [('app', '0008_chainidtopersistentid')]

    operations = [
        migrations.CreateModel(
            name='ChainIdToSeriesID',
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
                    'head_pid',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='chainidtoseriesid_head_pid',
                        to='app.IdNamespace',
                    ),
                ),
                (
                    'sid',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='chainidtoseriesid_sid',
                        to='app.IdNamespace',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='PersistentIdToChainID',
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
                    'chain',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='app.ChainIdToSeriesID',
                    ),
                ),
                (
                    'pid',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='persistentidtochainid_pid',
                        to='app.IdNamespace',
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(name='ChainIdToPersistentId'),
        migrations.RemoveField(model_name='seriesidtoheadpersistentid', name='pid'),
        migrations.RemoveField(model_name='seriesidtoheadpersistentid', name='sid'),
        migrations.RemoveField(model_name='seriesidtopersistentid', name='pid'),
        migrations.RemoveField(model_name='seriesidtopersistentid', name='sid'),
        migrations.DeleteModel(name='SeriesIdToHeadPersistentId'),
        migrations.DeleteModel(name='SeriesIdToPersistentId'),
    ]
