# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-08 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TripBuddy', '0002_trip_itemslist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='invoice',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='link',
            field=models.URLField(default='https://www.facebook.com/'),
        ),
    ]
