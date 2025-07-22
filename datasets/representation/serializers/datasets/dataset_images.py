import os

from rest_framework import serializers

from shared.serializers import Base64ImageField
from datasets.models import DatasetImage
from datasets.representation.serializers.datasets.annotations import AnnotationDetailedSerializer
from datasets.representation.serializers.datasets.labels import LabelSerializer


class DatasetImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)  # Use the custom Base64ImageField for POST
    base_image = Base64ImageField(required=False)  # Use the custom Base64ImageField for POST
    total_weight = serializers.SerializerMethodField()
    extension = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()
    annotations = AnnotationDetailedSerializer(many=True, read_only=True)

    class Meta:
        model = DatasetImage
        exclude = ['dataset']

    def get_total_weight(self, obj):
        total_size_bytes = obj.image.size
        if total_size_bytes >= 1e9:  # Convert bytes to GB
            return f"{total_size_bytes / 1e9:.2f} GB"
        return f"{total_size_bytes / 1e6:.2f} MB"

    def get_extension(self, obj):
        if obj.image and hasattr(obj.image, 'name') and obj.image.name:
            return os.path.splitext(obj.image.name)[-1].lower().replace('.', '')
        return None

    def get_name(self, obj):
        return obj.image.name.split("/")[-1]

    def get_labels(self, obj):
        labels = {annotation.label.id: annotation.label for annotation in obj.annotations.all()}
        return LabelSerializer(labels.values(), many=True).data

