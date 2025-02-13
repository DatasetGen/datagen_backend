from datasets.domain import Annotation


class SyntheticVsRealAnnotationsPieChartQuery:
    def query(self, dataset_id: int):
        synthetic_annotations = Annotation.objects.filter(image__dataset_id=dataset_id, is_synthetic=True).count()
        non_synthetic_annotations = Annotation.objects.filter(image__dataset_id=dataset_id, is_synthetic=False).count()
        return [
            {
                "name" : "synthetic",
                "value" : synthetic_annotations,
                "color": "#111411"
            },
            {
                "name": "real",
                "value" : non_synthetic_annotations,
                "color" :  "#905ef8"
            }
        ]
