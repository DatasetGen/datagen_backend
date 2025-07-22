import uuid
from django.db import models

from shared.domain.Entity import Entity
from .dataset import Dataset

class DatasetImage(Entity):
    def upload_to(self, filename):
        ext = filename.split('.')[-1]
        new_filename = f"{uuid.uuid4()}.{ext}"
        return f'datasets/{self.dataset.id}/{new_filename}'

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_to)
    base_image = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='derivatives', null=True, blank=True)
    extra_information = models.JSONField(default=dict)
    prompt = models.TextField(default="")
    negative_prompt = models.TextField(default="")
    generation_type = models.CharField(max_length=100, default="text2image")
    is_synthetic = models.BooleanField(default=False)
    job = models.ForeignKey('datasets.Job', on_delete=models.SET_NULL, related_name='images', null=True, blank=True)
    batch = models.ForeignKey('datasets.DataBatch', on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    done = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
