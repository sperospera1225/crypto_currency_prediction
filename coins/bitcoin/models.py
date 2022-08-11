from django.db import models

# Create your models here.

class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at= models.DateTimeField()
    sentimentResult=models.IntegerField()