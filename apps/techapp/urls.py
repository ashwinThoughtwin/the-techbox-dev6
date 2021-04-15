from django.urls import path
from .views import dashboard, error, Loginview ,logout_request

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('', Loginview, name='login'),
    path('logout', logout_request, name='logout'),
    path('err/', error),
]
