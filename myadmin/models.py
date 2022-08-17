from unicodedata import name
from django.db import models

# Create your models here.
class Mydata(models.Model):
    name = models.CharField(max_length=5)
    age = models.CharField(max_length=5)


class Banner(models.Model):
    banner = models.CharField(max_length=2500,null = True)
    title = models.CharField(max_length=500,null=True)
    description= models.CharField(max_length=500,null=True)
    url =models.CharField(max_length=500,null=True)
    is_selected = models.BooleanField(default=False)