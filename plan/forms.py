from django import forms
from .models import Plan
import csv, io


class UploadFile(forms.Form):
    file_path = forms.FileField()
