# Generated by Django 3.2 on 2021-09-18 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cnab', '0004_auto_20210918_0501'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='store',
            new_name='title',
        ),
    ]
