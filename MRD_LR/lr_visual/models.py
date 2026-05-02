from django.db import models
from django_pandas.managers import DataFrameManager

# Create your models here.

class completeData(models.Model):
    MONTH = models.CharField(max_length=80, null=True)
    YEAR = models.IntegerField()
    CA_NO = models.IntegerField()
    MTR_NO = models.IntegerField()
    ZONE_NAME = models.CharField(max_length=80, null=True)
    REGION = models.CharField(max_length=80, null=True)
    UNIT_CODE = models.CharField(max_length=80, null=True)
    ACC_CLASS = models.CharField(max_length=80, null=True)
    SUB_DIVISION = models.CharField(max_length=80, null=True)
    TAMPER_COUNT = models.IntegerField()
    KWH = models.FloatField()
    PAY_AGAINST_CURR_DMD = models.IntegerField()
    PAY_AGAINST_ARREARS = models.IntegerField()
    PAYMENT_AGAINST_TOTAL = models.IntegerField()
    BUCKETING_DERIVED = models.CharField(max_length=80, null=True)
    BUCKETING_DISPLAY = models.CharField(max_length=80, null=True)
    objects=DataFrameManager()

