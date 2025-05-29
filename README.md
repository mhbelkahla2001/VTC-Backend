# 🚗 VTC App - Backend

Ce dépôt contient la partie **backend** du projet VTC (Voiture de Transport avec Chauffeur), développé avec **Django** et connecté à une base de données **PostgreSQL**.

## ⚙️ Fonctionnalités principales

- 🔐 Authentification et gestion des utilisateurs (clients / chauffeurs / admins)
- 📅 Réservations de trajets
- 📦 Système d’abonnement
- 📬 Notifications par email (via SMTP) et SMS (via Twilio)
- 📍 Intégration Mapbox pour la géolocalisation
- 💳 Paiement en ligne avec Stripe
- 🤖 Support chatbot (OpenAI ou Rasa)

## 🏗️ Technologies utilisées

- Python 3.x
- Django / Django REST Framework
- PostgreSQL
- Twilio
- Stripe
- Mapbox
- Dotenv
- Celery (si utilisé pour les tâches asynchrones)
- Redis (si utilisé)

## 🚀 Lancer le projet en local

```bash
# Créer et activer un environnement virtuel
python -m venv .venv
source .venv/bin/activate   # ou .venv\Scripts\activate sous Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer les migrations
python manage.py migrate

# Lancer le serveur
python manage.py runserver
