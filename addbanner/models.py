from django.db import models


def add_image_folder(instance, filename):
    return '/'.join(['add_banner_images', str(instance.title), filename])


class AddModel(models.Model):
    title = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    image = models.ImageField(null=True, upload_to=add_image_folder)

