from django.test import TestCase

from datasets.application.download_dataset_for_detection_use_case import DownloadDatasetForDetectionUseCase, \
    DownloadDatasetForDetectionCommand
from datasets.application.tests.dataset_data_mother import DatasetDataMother
from datasets.domain import Dataset


class TestDownloadDatasetForDetection(TestCase):
    def setUp(self):
        DatasetDataMother().create_dataset()

    def test_result_failure_when_dataset_does_not_exists(self):
        use_case = DownloadDatasetForDetectionUseCase()
        result = use_case.execute(DownloadDatasetForDetectionCommand(
           dataset_id=1029
        ))
        assert result.is_failure == True

    def test_result_success_when_dataset_has_images(self):
        use_case = DownloadDatasetForDetectionUseCase()
        result = use_case.execute(DownloadDatasetForDetectionCommand(
            dataset_id=1
        ))
