from django.db import models

# Create your models here.
class Syntelog(models.Model):
    athaliana = models.CharField(max_length=30, db_index=True)
    type = models.CharField(max_length=30)
    description = models.CharField(max_length=300, db_index=True)
    lyrata = models.CharField(max_length=30)
    lyrata_code = models.CharField(max_length=10, db_index=True)
    papaya = models.CharField(max_length=30)
    papaya_code = models.CharField(max_length=10, db_index=True)
    peach = models.CharField(max_length=30)
    peach_code = models.CharField(max_length=10, db_index=True)
    grape = models.CharField(max_length=30)
    grape_code = models.CharField(max_length=10, db_index=True)
    gevo_link = models.CharField(max_length=600)

