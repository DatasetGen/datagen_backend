from dataclasses import dataclass
import io
import os
from django.db import transaction
from datasets.domain import Annotation, DatasetSnapshot, Label
from datasets.domain.dataset import Dataset
from shared.result import Result
import zipfile


@dataclass
class DownloadDatasetForDetectionCommand:
    dataset_id: int

class DownloadDatasetForDetectionUseCase:
    @transaction.atomic
    def execute(self, command: DownloadDatasetForDetectionCommand):
        if not Dataset.objects.filter(pk=command.dataset_id).exists():
            return Result.failure({
                "message": "Dataset not found",
                "error_code": 1
            })
        dataset = Dataset.objects.get(pk=command.dataset_id)
        snapshot = DatasetSnapshot(dataset=dataset)
        snapshot.save()
        images = dataset.images.all()
        labels = list(Label.objects.filter(dataset=dataset).order_by("id").values_list("id", flat=True))
        try:
            os.mkdir("media/snapshots")
        except:
            pass
        with zipfile.ZipFile('media/snapshots/dataset_{}__snapshot_{}.zip'.format(dataset.id, snapshot.id), "w") as zip:
            for image in images:
                annotations = Annotation.objects.filter(image=image)
                img = image.image
                img_name = os.path.basename(img.name).split(".")[0]
                zip.write(img.path, "train/images/{}.png".format(img_name))
                annotation_text = ""
                for annotation in annotations:
                    index = labels.index(annotation.label.id)
                    annotation_text += "{} {} {} {} {}\n".format(index, annotation.data["point"][0]+annotation.data["width"]/2, annotation.data["point"][1]+annotation.data["height"]/2, annotation.data["width"], annotation.data["height"])
                zip.writestr( "train/labels/{}.txt".format(img_name), annotation_text)
            zip.close()
        snapshot.file = 'snapshots/dataset_{}__snapshot_{}.zip'.format(dataset.id, snapshot.id)
        snapshot.save()
        return Result.ok({
            "dataset_id": dataset.id,
            "snapshot_id": snapshot.id,
            "snapshot_url": 'media/snapshots/dataset_{}__snapshot_{}.zip'.format(dataset.id, snapshot.id)
        })