from django.test import TestCase
from django.contrib.auth import get_user_model

from datasets.application.assign_batch_use_case import AssignBatchUseCase, AssignBatchCommand
from datasets.domain import Dataset, Job, DatasetImage, DataBatch

class DatasetBatchJobImageTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = get_user_model().objects.create_user(email="pepe@pepe.com", username="pepe",password="password123")
        self.user_2 = get_user_model().objects.create_user(email="jonay@jonay.com", username="jonay",password="password123")

        # Create a dataset
        self.dataset = Dataset.objects.create(
            user=self.user,
            name="Test Dataset",
            description="A dataset for testing purposes."
        )

        # Create a batch linked to the dataset
        self.batch = DataBatch.objects.create(
            name="Test Batch",
            dataset=self.dataset
        )

        self.images = []
        for i in range(20):
            img = DatasetImage.objects.create(
                dataset=self.dataset,
                batch=self.batch
            )
            self.images.append(img)

    def test_assign_batch_use_case(self):
        use_case = AssignBatchUseCase()
        command = AssignBatchCommand(
            owner_id=self.user.id,
            batch_id=self.batch.id,
            user_ids=[self.user.id, self.user_2.id],
            images_per_task=5
        )
        use_case.execute(command)
        assert Job.objects.count() == 4
        assert DatasetImage.objects.filter(job=None).count() == 0
        for image in DatasetImage.objects.all():
            assert image.job.owner == self.user
            assert image.job is not None
            assert image.job.assignee is not None

