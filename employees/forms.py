# employees/forms.py
from django import forms
from .models import Designation, Department

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
        }
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#1e2a3a]',
                'placeholder': 'Department Name'
            })
        }
