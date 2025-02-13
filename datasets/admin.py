from django.contrib import admin

from datasets import models

# Register your models here.
admin.site.register(models.Dataset)
admin.site.register(models.DatasetImage)
admin.site.register(models.Label)
admin.site.register(models.Annotation)
