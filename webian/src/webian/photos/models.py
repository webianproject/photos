from django.db import models

class Photo(models.Model):
    uri = models.CharField(max_length=256)
    caption = models.CharField(max_length=256)
