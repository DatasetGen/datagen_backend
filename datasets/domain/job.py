from django.db import models
from datagen_backend import settings
from shared.domain.Entity import Entity
from .data_batch import DataBatch


class Job(Entity):
    dataset = models.ForeignKey('datasets.Dataset', on_delete=models.CASCADE, related_name='jobs')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owner", null=True,
                              blank=True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignee", null=True,
                                 blank=True)
    batch = models.ForeignKey(DataBatch, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
