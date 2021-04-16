from django import forms
from .models import TechItem, Employee


class TechItemUpload(forms.ModelForm):
    class Meta:
        model = TechItem
        fields = ('item_name', 'item_image', 'item_description')


class AddEmp(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('name', 'email', 'address', 'mobile_number', 'employee_team')
