from rest_framework import serializers

from datasets.models import Dataset
from datasets.representation.serializers.datasets.dataset_images import DatasetImageSerializer
from datasets.representation.serializers.datasets.labels import LabelSerializer


class DatasetSerializer(serializers.ModelSerializer):
    num_images = serializers.SerializerMethodField()
    num_labels = serializers.SerializerMethodField()
    total_weight = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    labels = LabelSerializer(many=True, read_only=True)

    class Meta:
        model = Dataset
        exclude = ['user']

    def get_num_images(self, obj):
        return obj.images.count()

    def get_num_labels(self, obj):
        return obj.labels.count()

    def get_total_weight(self, obj):
        total_size_bytes = sum(
            image.image.size for image in obj.images.all() if image.image and hasattr(image.image, 'size')
        )
        if total_size_bytes >= 1e9:  # Convert bytes to GB
            return f"{total_size_bytes / 1e9:.2f} GB"
        return f"{total_size_bytes / 1e6:.2f} MB"

    def get_thumbnail(self, obj):
        request = self.context.get("request")  # Get request from context
        first_image = obj.images.last()
        if first_image and first_image.image:
            image_url = first_image.image.url  # Relative URL
            return {
                **DatasetImageSerializer(first_image).data,
                "image": request.build_absolute_uri(image_url)
            }
        return None
