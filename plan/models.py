from django.conf import settings
from django.db import models


# Create your models here.

class Plan(models.Model):
    change_date = models.CharField(max_length=100, null=True, blank=True)
    store_code = models.CharField(max_length=100, null=True, blank=True)
    old_plan_name = models.CharField(max_length=100)
    old_plan_speed = models.IntegerField()
    old_plan_quota = models.IntegerField()
    old_plan_price = models.IntegerField()
    new_plan_name = models.CharField(max_length=100)
    new_plan_speed = models.IntegerField()
    new_plan_quota = models.IntegerField()
    new_plan_price = models.IntegerField()
    number_of_movements = models.IntegerField()

    def __str__(self):
        return self.old_plan_name


class TestUpload(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
