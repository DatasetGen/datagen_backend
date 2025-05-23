from django.db import transaction
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from datasets.application.annotations_by_label_bar_chart_query import SyntheticVsRealAnnotationsBarChartQuery
from datasets.domain import DatasetSnapshot
from datasets.application.download_dataset_for_detection_use_case import DownloadDatasetForDetectionUseCase, \
    DownloadDatasetForDetectionCommand
from datasets.application.synthetic_vs_real_annotations_pie_chart_query import SyntheticVsRealAnnotationsPieChartQuery
from datasets.models import Dataset, Label, DatasetImage, Annotation
from datasets.representation.serializers.datasets.annotations import AnnotationDetailedSerializer, AnnotationSerializer
from datasets.representation.serializers.datasets.dataset import DatasetSerializer, DatasetSnapshotSerializer
from datasets.representation.serializers.datasets.dataset_images import DatasetImageSerializer
from datasets.representation.serializers.datasets.labels import LabelSerializer


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all().order_by('-id')
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    @action(detail=True, methods=['get'])
    def image_bar_chart(self, request, pk=None):
        use_case = SyntheticVsRealAnnotationsPieChartQuery()
        res = use_case.query(dataset_id=pk)
        return Response(res, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def generate_snapshot(self, request, pk=None):
        use_case = DownloadDatasetForDetectionUseCase()
        res = use_case.execute(
                DownloadDatasetForDetectionCommand(dataset_id=pk)
           )
        return Response(res.unwrap(), status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def image_pie_chart(self, request, pk=None):
        use_case = SyntheticVsRealAnnotationsPieChartQuery()
        res = use_case.query(dataset_id=pk)
        return Response(res, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def pie_chart(self, request, pk=None):
        use_case = SyntheticVsRealAnnotationsPieChartQuery()
        res = use_case.query(dataset_id=pk)
        return Response(res, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def bar_chart(self, request, pk=None):
        use_case = SyntheticVsRealAnnotationsBarChartQuery()
        res = use_case.query(dataset_id=pk)
        return Response(res, status=status.HTTP_200_OK)


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all().order_by('-id')
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        dataset_id = self.kwargs.get('dataset_pk')
        return super().get_queryset().filter(dataset_id=dataset_id, dataset__user=self.request.user)

    def perform_create(self, serializer):
        dataset_id = self.kwargs.get('dataset_pk')
        serializer.save(dataset_id=dataset_id)

class DatasetImageFilter(FilterSet):
    class Meta:
        model = DatasetImage
        exclude = ['image']  # Exclude the ImageField from filtering


class DatasetSnapshotViewSet(viewsets.ModelViewSet):
    queryset= DatasetSnapshot.objects.all().order_by("-id")
    serializer_class= DatasetSnapshotSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend,]

    def get_queryset(self):
        dataset_id = self.kwargs.get('dataset_pk')
        return super().get_queryset().filter(dataset_id=dataset_id, dataset__user=self.request.user)

class DatasetImageViewSet(viewsets.ModelViewSet):
    queryset = DatasetImage.objects.all().order_by('-id')
    serializer_class = DatasetImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = DatasetImageFilter

    def get_queryset(self):
        dataset_id = self.kwargs.get('dataset_pk')
        return super().get_queryset().filter(dataset_id=dataset_id, dataset__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(dataset_id=self.kwargs.get('dataset_pk'))

class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all().order_by('-id')
    serializer_class = AnnotationDetailedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        dataset_id = self.kwargs.get('dataset_pk')
        image_id = self.kwargs.get('image_pk')
        return super().get_queryset().filter(
            image__dataset_id=dataset_id,
            image_id=image_id,
            image__dataset__user=self.request.user
        )

    def perform_create(self, serializer):
        image_id = self.kwargs.get('image_pk')
        serializer.save(image_id=image_id)

    @action(detail=False, methods=["post"], url_path="batch")
    def batch_create_or_update(self, request, dataset_pk=None, image_pk=None):
        """
        Deletes all existing annotations.py for the given image and recreates them from the provided list.
        """
        data = request.data  # Expecting a list of annotation objects
        if not isinstance(data, list):
            return Response({"error": "Data should be a list of annotations.py."}, status=status.HTTP_400_BAD_REQUEST)

        image = DatasetImage.objects.filter(id=image_pk, dataset_id=dataset_pk, dataset__user=request.user).first()
        if not image:
            return Response({"error": "Invalid image or permission denied."}, status=status.HTTP_403_FORBIDDEN)

        with transaction.atomic():
            # Delete existing annotations.py
            Annotation.objects.filter(image=image).delete()

            created_annotations = []

            for annotation_data in data:
                # Validate Label
                label_id = annotation_data.get("label")
                label = Label.objects.filter(id=label_id, dataset_id=dataset_pk).first()
                if not label:
                    return Response({"error": f"Invalid label ID {label_id}"}, status=status.HTTP_400_BAD_REQUEST)

                # Create new annotation
                annotation = Annotation.objects.create(
                    id=annotation_data.get("id") or None,  # Allow UUID to be auto-generated if missing
                    type=annotation_data["type"],
                    label=label,
                    image=image,
                    data=annotation_data["data"],
                    is_synthetic=annotation_data.get("is_synthetic") or False
                )

                created_annotations.append(annotation)

        return Response(AnnotationSerializer(created_annotations, many=True).data, status=status.HTTP_201_CREATED)


