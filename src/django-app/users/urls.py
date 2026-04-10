from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('api/register/', views.register, name='api_register'),
    path('api/login/', views.login_api, name='api_login'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/register/', views.register_view, name='register'),
    path('profil/', views.profile_view, name='profil'),
    

path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html',
        success_url='/profil/' # Redirige vers ton URL 'profil' après succès
    ), name='password_change'),

path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'
    ), name='password_change_done'),

]

