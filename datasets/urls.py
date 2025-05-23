from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from datasets.representation.views import JobViewSet, BatchViewSet, DatasetSnapshotViewSet
from datasets.representation.views.datasets import DatasetViewSet, LabelViewSet, DatasetImageViewSet, AnnotationViewSet

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')

datasets_router = NestedDefaultRouter(router, r'datasets', lookup='dataset')
datasets_router.register(r'labels', LabelViewSet, basename='dataset-labels')
datasets_router.register(r'images', DatasetImageViewSet, basename='dataset-images')
datasets_router.register(r'jobs', JobViewSet, basename='dataset-jobs')
datasets_router.register(r'batches', BatchViewSet, basename='dataset-job-categories')
datasets_router.register(r'snapshots', DatasetSnapshotViewSet, basename='dataset-snapshots')

images_router = NestedDefaultRouter(datasets_router, r'images', lookup='image')
images_router.register(r'annotations', AnnotationViewSet, basename='dataset-image-annotations')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(datasets_router.urls)),
    path('', include(images_router.urls)),
]
