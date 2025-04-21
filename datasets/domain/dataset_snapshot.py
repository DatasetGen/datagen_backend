from django.db import models

from datasets.domain import Dataset


class DatasetSnapshot(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    file = models.FileField(null=True, blank=True)