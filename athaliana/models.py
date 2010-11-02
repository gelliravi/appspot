from django.db import models

# Create your models here.
class Syntelog(models.Model):
    athaliana = models.CharField(max_length=40, db_index=True)
    type = models.CharField(max_length=40)
    description = models.CharField(max_length=600)
    gene_family = models.CharField(max_length=60, db_index=True)

    lyrata1 = models.CharField(max_length=40)
    papaya1 = models.CharField(max_length=40)
    poplar1 = models.CharField(max_length=40)
    poplar2 = models.CharField(max_length=40)
    grape1 = models.CharField(max_length=40)

    lyrata_code = models.CharField(max_length=5, db_index=True)
    papaya_code = models.CharField(max_length=5, db_index=True)
    poplar_code = models.CharField(max_length=5, db_index=True)
    grape_code = models.CharField(max_length=5, db_index=True)
    gevo_link = models.CharField(max_length=600)

