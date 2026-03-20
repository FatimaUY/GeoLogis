from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(["POST"])
def register(request):
    user = User.objects.create_user(
        username=request.data["username"],
        password=request.data["password"]
    )
    return Response({"message": "user created"})


@api_view(["POST"])
def login(request):
    user = authenticate(
        username=request.data["username"],
        password=request.data["password"]
    )

    if user:
        return Response({"message": "login success"})
    return Response({"error": "invalid credentials"}, status=401)