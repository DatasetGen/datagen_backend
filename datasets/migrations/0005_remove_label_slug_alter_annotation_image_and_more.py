# Generated by Django 4.2.18 on 2025-01-24 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0004_rename_data_annotation_annotation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='label',
            name='slug',
        ),
        migrations.AlterField(
            model_name='annotation',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotations.py', to='datasets.datasetimage'),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotations.py', to='datasets.label'),
        ),
        migrations.AlterField(
            model_name='datasetimage',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='datasets.dataset'),
        ),
        migrations.AlterField(
            model_name='label',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labels', to='datasets.dataset'),
        ),
    ]
