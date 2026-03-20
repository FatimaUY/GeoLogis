from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def trends(request):
    return Response({
        "Lille": "hausse",
        "Paris": "stable",
        "Marseille": "baisse"
    })