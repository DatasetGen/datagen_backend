# Generated by Django 4.2.18 on 2025-01-20 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0003_annotation_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='annotation',
            old_name='data',
            new_name='annotation',
        ),
    ]
