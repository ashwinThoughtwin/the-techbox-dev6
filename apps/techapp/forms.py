from django import forms
from django.forms import DateInput, ModelChoiceField

from .models import TechItem, Employee, AllottedItem
from .tasks import send_email_task


class TechItemUpload(forms.ModelForm):
    class Meta:
        model = TechItem
        fields = ('item_name', 'item_image', 'item_description')
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
            'item_description': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
        }


class AddEmp(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': "form-control",
    #     'placeholder': 'Employee Name',
    #     'id': "nameid"
    # }))

    class Meta:
        model = Employee
        fields = ('name', 'email', 'address', 'mobile', 'team')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;', 'id': 'nameid'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;', 'id': 'emailid'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;', 'id': 'addressid'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;', 'id': 'mobileid'}),
            'team': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;', 'id': 'teamid'}),
        }


class UpdateEmp(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('name', 'email', 'address', 'team', 'team')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
            'team': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
            'team': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class AllotItems(forms.ModelForm):
    tech_item = forms.ModelChoiceField(queryset=TechItem.objects.all(), widget=forms.Select(attrs={
        'class': "form-control",
        'style': 'width: 300px',

    }))

    employee_name = forms.ModelChoiceField(queryset=Employee.objects.all(), widget=forms.Select(attrs={
        'class': "form-control",
        'style': 'width: 300px',

    }))
    issue_date = forms.DateTimeField(widget=DateInput(attrs={
        'type': "datetime-local",
        'class': "form-control",
        'placeholder': 'IssueDate',
        'id': "IssueDate",
        'style': 'width: 300px',
    }))

    end_date = forms.DateTimeField(widget=DateInput(attrs={
        'type': "datetime-local",
        'class': "form-control",
        'placeholder': 'EndDate',
        'id': "end date",
        'style': 'width: 300px',
    }))

    class Meta:
        model = AllottedItem
        fields = ('tech_item', 'employee_name', 'issue_date', 'end_date')

    # def send_email(self):
    #     send_email_task.delay(
    #         self.cleaned_data['employee_name'], self.cleaned_data['email'],
    #         self.cleaned_data['tech_item'], self.cleaned_data['end_date'])
