# employees/forms.py
from django import forms
from .models import Designation

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
        }
