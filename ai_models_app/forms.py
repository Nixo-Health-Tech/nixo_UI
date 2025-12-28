from django import forms
from .models import ModelRun

class ImagingRunForm(forms.ModelForm):
    patient_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = ModelRun
        fields = ["image"]  # فقط فایل تصویر
