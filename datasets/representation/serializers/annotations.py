from django.utils import timezone

from datasets.models import DataBatch, Job, DatasetImage
from users.serializers import CustomUserSerializer
from rest_framework import serializers

class BatchSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    unassigned = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()

    class Meta:
        model = DataBatch
        exclude = ['dataset']

    def get_total(self, obj):
        """Returns the total number of jobs in this category."""
        return obj.job_set.count()

    def get_unassigned(self, obj):
        """Returns the number of completed jobs (where done=True) in this category."""
        return obj.images.filter(job=None).count()

    def get_completed(self, obj):
        """Returns the number of completed jobs (where done=True) in this category."""
        return obj.job_set.filter(done=True).count()


class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ['dataset']

class JobSerializer(serializers.ModelSerializer):
    frames = serializers.SerializerMethodField()
    done_frames = serializers.SerializerMethodField()
    reviewed_frames = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    range = serializers.SerializerMethodField()
    owner = CustomUserSerializer(read_only=True)
    assignee = CustomUserSerializer(read_only=True)
    start_range = serializers.SerializerMethodField()
    end_range = serializers.SerializerMethodField()
    current_image = serializers.SerializerMethodField()
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Job
        exclude=['dataset',]

    def get_done_frames(self, obj):
        return DatasetImage.objects.filter(job=obj, done=True).count()

    def get_reviewed_frames(self, obj):
        return DatasetImage.objects.filter(job=obj, reviewed=True).count()

    def get_frames(self, obj):
        """Returns the number of completed jobs (where done=True) in this category."""
        return DatasetImage.objects.filter(job=obj).count()

    def get_duration(self, obj):
        return (timezone.now()-obj.timestamp).days

    def get_start_range(self, obj):
        images = DatasetImage.objects.filter(job=obj)
        if(images.first() == None): return None
        first_id=images.first().id
        return first_id

    def get_end_range(self, obj):
        images = DatasetImage.objects.filter(job=obj)
        if(images.last() == None): return None
        first_id=images.last().id
        return first_id

    def get_current_image(self, obj):
        images = DatasetImage.objects.filter(job=obj, done=False).first()
        if(images == None): return None
        return images.id

    def get_range(self, obj):
        images = DatasetImage.objects.filter(job=obj)
        if(images.count() < 1): return "No images"
        first_id=images.first().id
        last_id=images.last().id
        return '{}-{}'.format(first_id, last_id)


