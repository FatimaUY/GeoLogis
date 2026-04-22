🚀 GeoLogis

Plateforme d’analyse et de prédiction du marché immobilier
GeoLogis est une plateforme complète de data engineering et machine learning dédiée à l’analyse du marché immobilier.
Elle combine un pipeline de données, un service de Machine Learning et une application web Django permettant la visualisation et l’exploitation des prédictions.

🏗️ Architecture globale
GeoLogis est structuré en trois services indépendants :
Service	Technologie	Rôle

📊 Data Pipeline	Python, Pandas, Scikit-learn	Extraction, nettoyage et transformation des données

🤖 ML Service	FastAPI, XGBoost, SQLAlchemy, MLflow	API de prédiction et entraînement des modèles

🌐 Django App	Django, Tailwind CSS	Interface utilisateur et dashboard

📁 Structure du projet
GeoLogis/
├── src/
│   ├── data_pipeline/        # ETL, preprocessing, training
│   ├── django-app/           # Application web Django
│   └── ml_service/           # API ML (FastAPI)
│
├── static/                   # assets (images, css)
├── mlruns/                   # tracking MLflow
├── requirements.txt          # dépendances principales
├── requirements-dev.txt      # tests & dev tools
└── README.md

⚙️ Fonctionnalités

📊 Data Pipeline
Extraction de données immobilières (API, CSV)
Nettoyage et normalisation des datasets
Feature engineering
Préparation des données pour modèles ML
Pipelines reproductibles pour entraînement

🤖 ML Service (FastAPI)
API REST de prédiction
Estimation immobilière
Calcul de taxe foncière
Analyse inflation et données géographiques
Entraînement des modèles ML
Tracking des expériences avec MLflow
Sérialisation des modèles (model.pkl)

🌐 Django App
Interface web utilisateur
Dashboard immobilier interactif
Authentification utilisateurs
Visualisation des prédictions
Intégration avec le service ML via API REST

🔗 Communication entre services
Django agit comme gateway frontend
ML Service expose une API FastAPI
Communication via requêtes HTTP (requests)
Pipeline indépendant pour préparation et training

⚙️ Installation

1. Cloner le projet
git clone https://github.com/FatimaUY/GeoLogis.git
cd GeoLogis

2. Installer les dépendances

🌐 Django App
cd src/django-app
pip install -r requirements.txt

🤖 ML Service
cd ../ml_service
pip install -r requirements.txt

📊 Data Pipeline
cd ../data_pipeline
pip install -r requirements.txt

🍎 Prérequis macOS (IMPORTANT)
Si vous utilisez macOS (Apple Silicon / Intel), installez OpenMP :
brew install libomp
👉 Nécessaire pour le bon fonctionnement de XGBoost

3. Lancer le ML Service
cd src/ml_service
uvicorn app.main:app --reload

4. Lancer Django
cd src/django-app
python manage.py migrate
python manage.py runserver

🧠 Stack technique
Python 3.13
Django
FastAPI
XGBoost
Scikit-learn
Pandas
SQLAlchemy
MLflow
Tailwind CSS
SQLite (dev)

🧪 Tests
pip install -r requirements-dev.txt
pytest

📦 Environnements
Environnement	Fichier
Production	requirements.txt
Développement	requirements-dev.txt

👥 Équipe
Fatima
Hazel
Sarah
Lohan
