import math
from dataclasses import dataclass
from typing import List
from datasets.domain import DataBatch, DatasetImage, Job
from users.models import CustomUser


@dataclass
class AssignBatchCommand:
    batch_id: int
    owner_id: int
    user_ids : List[int]
    images_per_task : int

class AssignBatchUseCase:
    def execute(self, command: AssignBatchCommand):
        batch = DataBatch.objects.get(pk=command.batch_id)
        images = list(DatasetImage.objects.filter(batch=batch, job=None))
        owner = CustomUser.objects.get(pk=command.owner_id)
        users = list(CustomUser.objects.filter(pk__in=command.user_ids))
        total_jobs = math.ceil(len(images) / command.images_per_task)
        jobs = [Job(dataset=batch.dataset, owner=owner, batch=batch) for _ in range(total_jobs)]
        Job.objects.bulk_create(jobs)
        image_chunks = []
        for i in range(0, len(images), command.images_per_task):
            image_chunks.append(images[i:i + command.images_per_task])
        for job, chunk in zip(jobs, image_chunks):
            for image in chunk:
                image.job = job
        DatasetImage.objects.bulk_update(images, ["job"])
        for i, job in enumerate(jobs):
            job.assignee = users[i % len(users)]
        Job.objects.bulk_update(jobs, ["assignee"])
        return {
            "assigned_jobs": True
        }
