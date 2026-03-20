from django.shortcuts import render
from .models import Article

def liste_articles(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'GeoLogis/liste_articles.html', context) 
# Create your views here.
