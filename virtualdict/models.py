from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Concepts(models.Model):
    title = models.CharField(max_length=200)
    definition = models.TextField(default="")
    exampleText = models.TextField(null=True, blank=True)
    exampleImg = models.ImageField(null=True, blank=True)
    source = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title + " - " + self.user.username
    
