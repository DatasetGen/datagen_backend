# Generated by Django 4.2.18 on 2025-01-17 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SegmentationAnnotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.annotation')),
            ],
        ),
        migrations.CreateModel(
            name='SegmentationPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('segmentation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.segmentationannotation')),
            ],
        ),
        migrations.CreateModel(
            name='Labels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.dataset')),
            ],
        ),
        migrations.CreateModel(
            name='DatasetImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.dataset')),
            ],
        ),
        migrations.CreateModel(
            name='BoundingBoxAnnotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_0', models.FloatField()),
                ('y_0', models.FloatField()),
                ('x_1', models.FloatField()),
                ('y_1', models.FloatField()),
                ('annotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.annotation')),
            ],
        ),
        migrations.AddField(
            model_name='annotation',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.datasetimage'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.labels'),
        ),
    ]
