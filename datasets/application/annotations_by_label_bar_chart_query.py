from datasets.domain import Annotation, Label


class SyntheticVsRealAnnotationsBarChartQuery:
    def query(self, dataset_id: int):
        labels = Label.objects.filter(dataset_id=dataset_id)
        result = []
        for x in labels:
            synthetic_annotations = Annotation.objects.filter(
                image__dataset_id=dataset_id,
                label_id=x.id,
                is_synthetic=True).count()
            non_synthetic_annotations = Annotation.objects.filter(
                image__dataset_id=dataset_id,
                label_id=x.id,
                is_synthetic=False).count()
            result.append({
                "name" : x.name,
                "real" : non_synthetic_annotations,
                "synthetic": synthetic_annotations
            })
        return result
