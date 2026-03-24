from django.views.generic import ListView
from .models import Article

class ListeArticlesView(ListView):
    model = Article
    template_name = 'GeoLogis/acceuil.html'
    context_object_name = 'articles'
    
 
