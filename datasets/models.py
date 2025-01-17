import uuid

from django.db import models

# Create your models here.
class Dataset(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Label(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class DatasetImage(models.Model):
    def upload_to(self, filename):
        ext = filename.split('.')[-1]
        new_filename = f"{uuid.uuid4()}.{ext}"
        return f'media/datasets/{self.dataset.id}/{new_filename}'

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to)



class Annotation(models.Model):
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    image = models.ForeignKey(DatasetImage, on_delete=models.CASCADE)


class BoundingBoxAnnotation(models.Model):
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
    x_0 = models.FloatField()
    y_0 = models.FloatField()
    x_1 = models.FloatField()
    y_1 = models.FloatField()


class SegmentationAnnotation(models.Model):
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)

class SegmentationPoints(models.Model):
    segmentation = models.ForeignKey(SegmentationAnnotation, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()

