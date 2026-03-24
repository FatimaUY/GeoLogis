from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from django.contrib import messages

User = get_user_model()

@api_view(["POST"])
def register(request):
    user = User.objects.create_user(
        email=request.data["email"],
        password=request.data["password"]
    )
    return Response({"message": "user created"})


@api_view(["POST"])
def login_api(request):
    user = authenticate(
        email=request.data["email"],
        password=request.data["password"]
    )

    if user:
        return Response({"message": "login success"})
    return Response({"error": "invalid credentials"}, status=401)

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            auth_login(request, user)
            return redirect("home")
        else:
            return render(request, "users/login.html", {"error": "Identifiants invalides"})
    return render(request, "users/login.html")

def logout_view(request):
    auth_logout(request)
    return redirect("home")

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
            return redirect("login")
        else:
            messages.error(request, "Erreur lors de l'inscription. Veuillez vérifier les informations fournies.")   
            
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})
       