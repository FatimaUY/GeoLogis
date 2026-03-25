from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Prediction
from .services import fake_prediction
import folium 
import requests
from django.shortcuts import render

@api_view(["GET", "POST"]) 
def predict(request):
    prediction = None
    map_html = None
    nom_commune = "Zone non définie"

    if request.method == "POST":
        
        data = request.data
        zipcode = request.data.get("zipcode")
        
        
        
        
        
        geo_url = f"https://geo.api.gouv.fr/communes?codePostal={zipcode}&fields=nom,centre,contour,population&format=json&geometry=contour"
        
        try:
            geo_response = requests.get(geo_url)
            geo_data = geo_response.json()

            if geo_data:
                commune = geo_data[0]
                nom_commune = commune.get('nom')
                pop_auto = commune.get('population', 0)
                lon, lat = commune['centre']['coordinates']
                
                result = fake_prediction({
                    "zipcode": zipcode,
                    "population": pop_auto
                })

                
                m = folium.Map(location=[lat, lon], zoom_start=12, tiles="OpenStreetMap")

                
                if 'contour' in commune:
                    folium.GeoJson(
                        commune['contour'],
                        style_function=lambda x: {
                            'fillColor': '#8CA5A5', 
                            'color': '#7A5B3E', 
                            'weight': 2, 
                            'fillOpacity': 0.3
                        }
                    ).add_to(m)

                
                folium.Marker(
                    [lat, lon], 
                    popup=f"Analyse : {nom_commune}",
                    icon=folium.Icon(color='red', icon='home')
                ).add_to(m)

                
                map_html = m._repr_html_()

                prediction = {
                    "result": result,
                    "population": pop_auto,
                    "nom": nom_commune
                }

        except Exception as e:
            print(f"Erreur API Géo/Folium: {e}")

       

    
    return render(request, "prediction/prediction.html", {
        "prediction": prediction,
        "map_html": map_html,
        "nom_commune": nom_commune
    })

@api_view(["GET"])
def get_predictions(request):
    """Vue pour l'historique (utilisée par ton URLconf)"""
    predictions = Prediction.objects.all().order_by('-id').values()
    return Response(list(predictions))        