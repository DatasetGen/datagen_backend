import uuid
from django.db import models

from shared.domain.Entity import Entity
from .label import Label
from .dataset_image import DatasetImage


class Annotation(Entity):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    type = models.CharField(max_length=100)
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name='annotations')
    image = models.ForeignKey(DatasetImage, on_delete=models.CASCADE, related_name="annotations")
    is_synthetic = models.BooleanField(default=False)
    data = models.JSONField()
