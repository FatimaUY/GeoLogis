from django.urls import path
from .views import predict, get_predictions

urlpatterns = [
    # Laisse le chemin vide '' car il sera complété par le fichier principal
    path('', predict, name='prediction'), 
    
    # Route pour ton API d'historique si besoin
    path('history/', get_predictions, name='prediction_history'),
]