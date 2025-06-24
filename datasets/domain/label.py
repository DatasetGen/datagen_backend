from django.db import models

from shared.domain.Entity import Entity
from .dataset import Dataset

class Label(Entity):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='labels')
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    prompt = models.TextField(default="")
    negative_prompt = models.TextField(default="")
    color = models.CharField(max_length=100)

    def __str__(self):
        return self.name
