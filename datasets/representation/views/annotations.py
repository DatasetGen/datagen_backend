import django_filters
from django.db.models import Q
from django.db.models.aggregates import Count
from django_filters import filters, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from datasets.application.assign_batch_use_case import AssignBatchUseCase, AssignBatchCommand
from datasets.models import Job, DataBatch
from datasets.representation.serializers.annotations import JobSerializer, JobPostSerializer, BatchSerializer


class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = '__all__'  # This automatically enables filtering for all fields

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-id')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]  # Enable filtering
    filterset_class = JobFilter  # Assign the filter class

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return JobSerializer
        return JobPostSerializer

    def get_queryset(self):
        dataset_id = self.kwargs.get('dataset_pk')
        return super().get_queryset().filter(
            dataset_id=dataset_id,
        )

    def perform_create(self, serializer):
        dataset_id = self.kwargs.get('dataset_pk')
        serializer.save(dataset_id=dataset_id, owner=self.request.user)

class BatchFilter(FilterSet):
    unassigned = filters.NumberFilter(method='filter_unassigned')
    unassigned_gt = filters.NumberFilter(method='filter_unassigned_gt')

    def filter_unassigned(self, queryset, name, value):
        return queryset.annotate(
            unassigned_count=Count('images', filter=Q(images__job=None))
        ).filter(unassigned_count=value)

    def filter_unassigned_gt(self, queryset, name, value):
        return queryset.annotate(
            unassigned_count=Count('images', filter=Q(images__job=None))
        ).filter(unassigned_count__gt=value)

    class Meta:
        model = DataBatch
        fields = ['unassigned', 'unassigned_gt']  # Enables filtering by unassigned count

class BatchViewSet(viewsets.ModelViewSet):
    queryset = DataBatch.objects.all().order_by('id')
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BatchFilter

    def get_queryset(self):
        dataset_id = self.kwargs.get('dataset_pk')
        return super().get_queryset().filter(
            dataset_id=dataset_id,
        )

    def perform_create(self, serializer):
        dataset_id = self.kwargs.get('dataset_pk')
        serializer.save(dataset_id=dataset_id)

    @action(detail=True, methods=['post'], url_path='assign')
    def assign(self, request, dataset_pk=None, pk=None):
        try:
            command = AssignBatchCommand(
                batch_id=pk,
                owner_id=self.request.user.id,
                user_ids=request.data['user_ids'],
                images_per_task=request.data['images_per_task'],
            )
            use_case = AssignBatchUseCase()
            res = use_case.execute(command)
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": str(e)
            },status=status.HTTP_400_BAD_REQUEST)

