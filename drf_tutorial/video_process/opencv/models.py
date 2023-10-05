from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Video(models.Model):
    """Recorded Video"""

    # Ref: https://docs.djangoproject.com/en/3.1/ref/models/fields/#filefield
    file = models.FileField(upload_to="videos/", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# Create your models here.
class Image(models.Model):
    """Uploaded Image"""

    file = models.FileField(upload_to="images/", blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Frame(models.Model):
    """
    Stores the extracted frame
    """

    width = models.IntegerField()
    height = models.IntegerField()
    channel = models.IntegerField()
    file = models.ImageField(upload_to="frames/", null=True)
    bboxes = ArrayField(ArrayField(models.IntegerField()))
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class Target(models.Model):
    """
    Stores the extracted target
    """

    width = models.IntegerField()
    height = models.IntegerField()
    file = models.ImageField(upload_to="targets/", null=True)
    bboxes = ArrayField(ArrayField(models.IntegerField()))
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
