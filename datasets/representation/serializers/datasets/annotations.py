from rest_framework import serializers
from datasets.models import Annotation
from datasets.representation.serializers.datasets.labels import LabelSerializer


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        exclude=['image',]

class AnnotationDetailedSerializer(serializers.ModelSerializer):
    label = LabelSerializer(read_only=True)

    class Meta:
        model = Annotation
        exclude=['image',]

