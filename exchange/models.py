from django.db import models


# Create your models here.


class Rate(models.Model):
    currency_from = models.CharField(max_length=3)
    currency_to = models.CharField(max_length=3)

    sell = models.DecimalField(decimal_places=4, max_digits=10)
    buy = models.DecimalField(decimal_places=4, max_digits=10)
    provider = models.CharField(max_length=50)

    date = models.DateField()
