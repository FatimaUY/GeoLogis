from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.ListeArticlesView.as_view(), name='articles'),
]