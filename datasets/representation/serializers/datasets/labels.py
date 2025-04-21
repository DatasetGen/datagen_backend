from rest_framework import serializers

from datasets.models import Label


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        exclude=['dataset',]
