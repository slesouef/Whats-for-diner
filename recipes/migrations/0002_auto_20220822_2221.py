# Generated by Django 3.2.15 on 2022-08-22 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='creationDate',
            new_name='creation_date',
        ),
        migrations.RenameField(
            model_name='content',
            old_name='modificationDate',
            new_name='modification_date',
        ),
        migrations.RenameField(
            model_name='ingredients',
            old_name='creationDate',
            new_name='creation_date',
        ),
        migrations.RenameField(
            model_name='ingredients',
            old_name='modificationDate',
            new_name='modification_date',
        ),
        migrations.RenameField(
            model_name='recipes',
            old_name='creationDate',
            new_name='creation_date',
        ),
        migrations.RenameField(
            model_name='recipes',
            old_name='modificationDate',
            new_name='modification_date',
        ),
    ]