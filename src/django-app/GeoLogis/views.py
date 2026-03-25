from django.views.generic import ListView
from .models import Article
from django.shortcuts import render

class ListeArticlesView(ListView):
    model = Article
    template_name = 'GeoLogis/acceuil.html'
    context_object_name = 'articles'

def info_view(request):
    return render(request, 'info.html')

    
 
