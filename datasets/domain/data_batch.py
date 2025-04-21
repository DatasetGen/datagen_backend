from django.db import models

from shared.domain.Entity import Entity


class DataBatch(Entity):
    name = models.CharField(max_length=100)
    dataset = models.ForeignKey('datasets.Dataset', on_delete=models.CASCADE, related_name='job_categories')
    timestamp = models.DateTimeField(auto_now_add=True)
    workbench = models.BooleanField(default=True)

    @property
    def unassigned_images(self):
        """Returns the number of completed jobs (where done=True) in this category."""
        return self.images.filter(job=None).count()


