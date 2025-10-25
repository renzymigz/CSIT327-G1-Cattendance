from django import forms
from .models import ClassSession

class ClassSessionForm(forms.ModelForm):
    class Meta:
        model = ClassSession
        fields = ["schedule_day"]