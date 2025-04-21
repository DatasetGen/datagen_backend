from shared.domain.Entity import Entity
from django.db import models


class GenerationTask(Entity):
    name = models.CharField(max_length=255)
    images_to_generate = models.IntegerField(default=0)
