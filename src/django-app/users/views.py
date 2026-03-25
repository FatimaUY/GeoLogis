from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import CustomUserCreationForm, CustomLoginForm
from predictions.models import Prediction

User = get_user_model()

# --- VUES API (REST) ---

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

# --- VUES CLASSIQUES (WEB) ---

def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user:
                auth_login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Identifiants invalides")
    else:
        form = CustomLoginForm()
    return render(request, "users/login.html", {"form": form})

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
            messages.error(request, "Erreur lors de l'inscription.")   
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})

@login_required
def profile_view(request):
    user = request.user
    
    if request.method == "POST":
        # Récupération des données du formulaire HTML
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        messages.success(request, "Vos informations ont été mises à jour avec succès !")
        # 'profil' correspond au name dans ton urls.py
        return redirect('profil') 

    # Récupération de l'historique lié à l'utilisateur
    history = Prediction.objects.filter(user=user).order_by('-id')
    
    context = {
        'user': user,
        'history': history,
    }
    return render(request, "profil.html", context)