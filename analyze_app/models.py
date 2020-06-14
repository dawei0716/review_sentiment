from django.db import models

# Create your models here.

class AnalysisResults(models.Model):

    review = models.TextField()
    result = models.CharField(max_length=100)
    score = models.FloatField()
