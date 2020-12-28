from django.urls import path, include
from . import views

app_name = 'plan'
urlpatterns = [
    path('', views.home, name='home'),
    path('test/',views.test,name='test'),

    # Upload paths
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    # export paths
    path('export_csv/', views.export_all, name='export_csv'),
    path('export_low_csv/', views.export_low_high, name='export_low_csv'),
    path('export_high_csv/', views.export_high_low, name='export_high_csv'),
    path('export_same_csv/',views.export_same_plan,name='export_same_csv'),
    path('panda/',views.panda_export,name='panda'),

    path('delete_all/', views.delete_all, name='delete_all'),
    path('lower_higher/', views.lower_higher, name='lower_higher'),
    path('same_plan/', views.same_plan, name='same_plan'),
    path('changed_plan/', views.change_plan, name='changed_plan'),
]
