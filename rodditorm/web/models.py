from django.db import models

class Queries(models.Model):
    type = models.CharField(max_length=50) # base / advanced / functions
    topic = models.CharField(max_length=50) # 1. JOIN, 3. SELECT
    description = models.CharField(max_length=250)
    query = models.CharField(max_length=5000)

    class Meta:
        ordering = ['topic']
