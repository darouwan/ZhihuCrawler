# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidates',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=10)),
                ('followers', models.IntegerField(default=0)),
                ('upvotes', models.IntegerField(default=0)),
                ('thanks', models.IntegerField(default=0)),
                ('time', models.DateTimeField(verbose_name='collected date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
