from django.test import TestCase
from django.contrib.auth import get_user_model

from datasets.application.annotations_by_label_bar_chart_query import SyntheticVsRealAnnotationsBarChartQuery
from datasets.application.synthetic_vs_real_annotations_pie_chart_query import SyntheticVsRealAnnotationsPieChartQuery
from datasets.domain import Dataset, Job, DatasetImage, DataBatch, Label, Annotation


class DatasetBatchJobImageTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="pepe@pepe.com", username="pepe",password="password123")
        self.user_2 = get_user_model().objects.create_user(email="jonay@jonay.com", username="jonay",password="password123")
        self.dataset = Dataset.objects.create(
            user=self.user,
            name="Test Dataset",
            description="A dataset for testing purposes."
        )
        label = Label.objects.create(
            name="Test Label",
            dataset=self.dataset
        )
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
            for i in range(0, 3):
                annotation = Annotation.objects.create(
                    type="bounding_box",
                    label=label,
                    image=img,
                    is_synthetic=False,
                    data={}
                )
                annotation.save()
            for i in range(0, 3):
                annotation = Annotation.objects.create(
                    type="bounding_box",
                    label=label,
                    image=img,
                    is_synthetic=True,
                    data={}
                )
                annotation.save()

    def test_assign_batch_use_case(self):
        query = SyntheticVsRealAnnotationsPieChartQuery()
        result = query.query(dataset_id=self.dataset.id)
        print(result)
        self.assertTrue(result)
        assert result['synthetic'] == 60
        assert result['real'] == 60

    def test_bar_chart(self):
        query = SyntheticVsRealAnnotationsBarChartQuery()
        result = query.query(dataset_id=self.dataset.id)
        print(result)
        self.assertTrue(result)
        assert result[0]['name'] == "Test Label"
        assert result[0]['real'] == 60
        assert result[0]['synthetic'] == 60
