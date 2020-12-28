from import_export import resources
from import_export.instance_loaders import ModelInstanceLoader
from .models import Plan
from django.db.models import F, Q, Sum


class PlanResource(resources.ModelResource):
    class Meta:
        model = Plan

