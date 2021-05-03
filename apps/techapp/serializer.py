from .models import TechItem, AllottedItem ,Employee
from rest_framework import serializers


class TechItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechItem
        fields = ['id', 'item_name', 'item_image', 'item_description', ]


class AssignItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllottedItem
        fields = ['id', 'tech_item', 'employee_name', 'issue_date', 'end_date']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'address', 'mobile', 'team']