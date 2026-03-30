from django.urls import path
from .views import trends

urlpatterns = [
    path('', trends, name='market_data'),
]
