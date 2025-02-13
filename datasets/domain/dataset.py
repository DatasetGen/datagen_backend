from django.db import models
from datagen_backend import settings
from shared.domain.Entity import Entity


class Dataset(Entity):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
