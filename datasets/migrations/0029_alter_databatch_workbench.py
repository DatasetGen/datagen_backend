# Generated by Django 4.2.18 on 2025-02-21 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0028_databatch_workbench'),
    ]

    operations = [
        migrations.AlterField(
            model_name='databatch',
            name='workbench',
            field=models.BooleanField(default=True),
        ),
    ]
