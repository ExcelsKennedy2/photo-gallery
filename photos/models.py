from django.contrib.auth.models import User
from django.db import models
# from cloudinary.models import CloudinaryField
# import cloudinary.utils

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to the uploader
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False, upload_to='photos/')
    description = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.description