from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register, name='api_register'),
    path('api/login/', views.login_api, name='api_login'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/register/', views.register_view, name='register'),
]