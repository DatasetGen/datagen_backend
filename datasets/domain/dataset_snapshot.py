from django.db import models

from datasets.domain import Dataset


class DatasetSnapshot(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, auto_created=True)
    file = models.FileField(null=True, blank=True)