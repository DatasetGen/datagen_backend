from PIL import Image
from django.contrib.auth import get_user_model

from datasets.domain import Dataset, Label, DataBatch, DatasetImage, Annotation


class DatasetDataMother:
   def create_dataset(self):
       self.user = get_user_model().objects.create_user(email="pepe@pepe.com", username="pepe", password="password123")
       self.user_2 = get_user_model().objects.create_user(email="jonay@jonay.com", username="jonay",
                                                          password="password123")
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
           img = Image.new("RGB", (100, 100))
           img.save("media/tests/test_{}.png".format(i))

           img = DatasetImage.objects.create(
               dataset=self.dataset,
               batch=self.batch,
               image="tests/test_{}.png".format(i)
           )
           self.images.append(img)
           for i in range(0, 3):
               annotation = Annotation.objects.create(
                   type="bounding_box",
                   label=label,
                   image=img,
                   is_synthetic=False,
                   data={
                       "point": [
                           0.3298192703310984,
                           0.39477998041771606
                       ],
                       "width": 0.4668674629226507,
                       "height": 0.35809950833667425
                   }
               )
               annotation.save()
           for i in range(0, 3):
               annotation = Annotation.objects.create(
                   type="bounding_box",
                   label=label,
                   image=img,
                   is_synthetic=True,
                   data={
                       "point": [
                           0.3298192703310984,
                           0.39477998041771606
                       ],
                       "width": 0.4668674629226507,
                       "height": 0.35809950833667425
                   }
               )
               annotation.save()
