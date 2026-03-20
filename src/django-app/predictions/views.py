from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Prediction
from .services import fake_prediction

@api_view(["POST"])
def predict(request):
    data = request.data

    required_fields = ["prix_m2", "population", "property_tax", "last_year_property_tax"]

    for field in required_fields:
        if field not in data:
            return Response({"error": f"{field} manquant"}, status=400)

    # fake ML
    result = fake_prediction(data)

    prediction = Prediction.objects.create(
        prix_m2=data["prix_m2"],
        population=data["population"],
        property_tax=data["property_tax"],
        last_year_property_tax=data["last_year_property_tax"],
        result=result
    )

    return Response({
        "id": prediction.id,
        "prediction": result
    })

@api_view(["GET"])
def get_predictions(request):
    predictions = Prediction.objects.all().values()
    return Response(list(predictions))