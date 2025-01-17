from django.contrib import admin

from datasets import models as models

# Register your models here.
admin.site.register(models.Dataset)
admin.site.register(models.DatasetImage)
admin.site.register(models.Label)
admin.site.register(models.Annotation)
admin.site.register(models.SegmentationAnnotation)
admin.site.register(models.BoundingBoxAnnotation)
admin.site.register(models.SegmentationPoints)
