from django import forms
from .models import ClassSession
from auth_app.models import StudentProfile, TeacherProfile
import re

class ClassSessionForm(forms.ModelForm):
    class Meta:
        model = ClassSession
        fields = ["schedule_day"]


class StudentProfileEditForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ["course", "year_level"]
        widgets = {
            "course": forms.TextInput(attrs={
                "class": "w-full border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#a2314b]/30"
            }),
            "year_level": forms.NumberInput(attrs={
                "class": "w-full border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#a2314b]/30",
                "min": "1",
                "max": "5",
                "step": "1",
                "inputmode": "numeric",
                "pattern": "[0-9]*"
            }),
        }

    def clean_year_level(self):
        yl = self.cleaned_data.get("year_level")

        if yl in (None, ""):
            return yl

        try:
            yl = int(yl)
        except (TypeError, ValueError):
            raise forms.ValidationError("Year Level must be a number.")

        if yl < 1 or yl > 5:
            raise forms.ValidationError("Year Level must be between 1 and 5.")

        return yl


class TeacherProfileEditForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ["department"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["department"].widget.attrs.update({
            "class": "w-full px-4 py-3 rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-[#a2314b]/30",
            "placeholder": "Enter department",
            "inputmode": "text"
        })

    def clean_department(self):
        dept = (self.cleaned_data.get("department") or "").strip()

        if not dept:
            raise forms.ValidationError("Department is required.")

        if re.search(r"\d", dept):
            raise forms.ValidationError("Department must contain text only (no numbers).")

        if len(dept) < 2:
            raise forms.ValidationError("Department is too short.")

        return dept
