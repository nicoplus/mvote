# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 15:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_poll_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uerid', models.PositiveIntegerField()),
                ('pollid', models.PositiveIntegerField()),
                ('vote_date', models.DateField()),
            ],
        ),
    ]
