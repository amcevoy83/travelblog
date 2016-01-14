# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(null=True, blank=True)),
                ('views', models.IntegerField(default=0)),
                ('tag', models.CharField(max_length=30, null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'images', blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Suggestions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.CharField(max_length=255)),
                ('post_title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(null=True, blank=True)),
                ('views', models.IntegerField(default=0)),
                ('tag', models.CharField(max_length=30, null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'images', blank=True)),
            ],
        ),
    ]
