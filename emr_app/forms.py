from django import forms
from .models import Patient, DocumentReference

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["full_name", "dob", "sex", "phone", "email", "address"]

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = DocumentReference
        fields = ["title", "category", "file"]
