from django.urls import path
from .views import dashboard, error, Loginview, logout_request, item_upload, AddEmployee
from apps.techapp import views

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('add-employee', AddEmployee.as_view(), name='add-employee'),
    path('', Loginview, name='login'),
    path('logout', logout_request, name='logout'),
    path('itemupload', item_upload, name='itemupload'),
    path('delete/<int:id>/', views.delete_item , name="deletedata"),
    path('err/', error, name="error"),
]
