from django.urls import path
from .views import predict, get_predictions

urlpatterns = [
    path("predict/", predict),
    path("", get_predictions),
]