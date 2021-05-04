from django.urls import path, include
from .views import logout_request
from apps.techapp import views
from apps.techapp.api import AssignItemApi, TechitemList, TechItemDetail, EmployeeCreate

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.Loginview.as_view(), name='login'),
    path('dashboard', views.DashBoardView.as_view(), name='dashboard'),
    path('add-employee', views.AddEmployee.as_view(), name='add-employee'),
    path('employee/', views.EmployeeTable.as_view(), name='employee_table'),
    path('logout', logout_request, name='logout'),
    path('itemupload', views.ItemUpload.as_view(), name='itemupload'),
    path('allot-items', views.AllotItem.as_view(), name='allot-items'),
    path('allot-delete', views.AllottedItemsDelete.as_view(), name='allot-delete'),
    path('delete/', views.DeleteItem.as_view(), name="deletedata"),
    path('employee-delete/', views.DeleteEmployee.as_view(), name="employee-delete"),
    path('updateemployee/<int:id>/', views.UpdateEmployee.as_view(), name='updateemployee'),
    path('charge/', views.Charge.as_view(), name='charge'),
    path('success/<str:args>/', views.Success.as_view(), name='success'),
    path('donation/', views.DonationPage.as_view(), name='donation'),


    # Api's
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/api-techitem/', TechitemList.as_view(), name="add-techitem"),
    path('api/api-techitem/<int:pk>/', TechItemDetail.as_view(), name="delete-techitem"),
    path('api/assign-techitem/', AssignItemApi.as_view(), name="assign-techitem"),

    # Generic Apl's
    path('api/add-employee/', EmployeeCreate.as_view(), name="add-techitem"),
    # path('api/add-techitem/', TechItemCreate.as_view(), name="add-techitem"),
    # path('api/update-techitem/<int:pk>/', TechItemUpdate.as_view(), name="update-techitem"),
    # path('api/list-techitem/', TechItemList.as_view(), name="list-techitem"),
    # path('api/delete-techitem/<int:pk>/', TechItemDelete.as_view(), name="delete-techitem"),

]
