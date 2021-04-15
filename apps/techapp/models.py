from django.db import models


# Create your models here.
class TechItem(models.Model):
    item_name = models.CharField(max_length=100)
    item_image = models.ImageField(upload_to=None, height_field=None, width_field=None, )
    item_description = models.CharField(max_length=200)

    def __str__(self):
        return self.item_name


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=150)
    mobile_number = models.CharField(blank=True, max_length=20)
    employee_team = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AllottedItem(models.Model):
    tech_item = models.ForeignKey(TechItem, on_delete=models.CASCADE)
    employee_name = models.ForeignKey(Employee, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.tech_item
