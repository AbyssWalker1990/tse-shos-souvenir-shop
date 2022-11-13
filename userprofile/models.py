from django.db import models
from django.contrib.auth.models import User
from goods.models import *
import uuid
# Create your models here.

from django.db.models.signals import post_save, post_delete

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    second_name = models.CharField(max_length=100, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        if self.username:
            return self.username
        else:
            return self.second_name




# class Bucket(models.Model):
#     owner = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
#     product_wanted = models.ManyToManyField(Product, null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True,
#                           primary_key=True, editable=False)
#
#
# class BucketHistory(models.Model):
#     owner = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
#     product_bought = models.ManyToManyField(Product, null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True,
#                           primary_key=True, editable=False)