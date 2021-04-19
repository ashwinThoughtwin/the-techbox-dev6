from django import forms
from django.forms import DateInput

from .models import TechItem, Employee, AllottedItem


class TechItemUpload(forms.ModelForm):
    class Meta:
        model = TechItem
        fields = ('item_name', 'item_image', 'item_description')


class AddEmp(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('name', 'email', 'address', 'mobile_number', 'employee_team')


class DateInput(forms.DateInput):
    input_type = 'date'


class AllotItems(forms.ModelForm):
    issue_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())

    class Meta:
        model = AllottedItem
        fields = ('tech_item', 'employee_name', 'issue_date', 'end_date')

