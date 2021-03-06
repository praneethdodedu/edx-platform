# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Converted from the original South migration 0002_default_rate_limit_config.py

from django.db import migrations, models


def forwards(apps, schema_editor):
    """Ensure that rate limiting is enabled by default. """
    RateLimitConfiguration = apps.get_model("util", "RateLimitConfiguration")
    objects = RateLimitConfiguration.objects
    if not objects.exists():
        objects.create(enabled=True)


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards)
    ]
