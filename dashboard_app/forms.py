from django import forms
from .models import ClassSession
from auth_app.models import StudentProfile, TeacherProfile  # if TeacherProfile is in auth_app

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
            "year_level": forms.TextInput(attrs={
                "class": "w-full border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#a2314b]/30"
            }),
        }

class TeacherProfileEditForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ["department"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["department"].widget.attrs.update({
            "class": "w-full px-4 py-3 rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-rose-200",
            "placeholder": "Enter department"
        })
