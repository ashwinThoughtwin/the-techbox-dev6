from django.contrib import admin
from .models import TechItem, Employee, AllottedItem

# Register your models here.
admin.site.register(TechItem)
admin.site.register(Employee)
admin.site.register(AllottedItem)
