from django.urls import path
from .views import logout_request, AddEmployee
from apps.techapp import views

urlpatterns = [
    path('', views.Loginview.as_view(), name='login'),
    path('dashboard', views.DashBoardView.as_view(), name='dashboard'),
    path('add-employee', AddEmployee.as_view(), name='add-employee'),
    path('employee/', views.EmployeeTable.as_view(), name='employee_table'),
    path('logout', logout_request, name='logout'),
    path('itemupload', views.ItemUpload.as_view(), name='itemupload'),
    path('allot-items', views.AllotItem.as_view(), name='allot-items'),
    path('delete/<int:id>/', views.delete_item, name="deletedata"),

    # path('err/', error, name="error"),
]
