# Generated by Django 2.2 on 2020-08-01 02:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='text',
        ),
    ]
