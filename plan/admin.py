from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Plan,TestUpload


# Register your models here.
@admin.register(Plan)
class PlanAdmin(ImportExportModelAdmin):
    list_display = ("change_date","store_code","old_plan_name","old_plan_speed",
                    "old_plan_quota","old_plan_price","new_plan_name","new_plan_speed",
                    "new_plan_quota","new_plan_price","number_of_movements")
    pass


admin.site.register(TestUpload)
