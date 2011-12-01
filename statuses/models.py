from django.db import models

class Status(models.Model):
    original_id = models.CharField(mex_length=60)
    text = models.CharField(max_length=140)
    authors_id = models.IntegerField()
    authors_name = models.CharField(max_length=140, blank=True)
    authors_time_zone = models.CharField(max_length=140, blank=True)
