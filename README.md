# 🚗 VTC App – Backend (Django)

Ce dépôt contient le **backend de l’application VTC** (Voiture de Transport avec Chauffeur), développé en **Django** et connecté à une base de données **PostgreSQL**.  
Il gère l’ensemble de la logique métier : gestion des utilisateurs, réservations, abonnements, notifications, paiements, géolocalisation, et support.

---

## 🧩 Fonctionnalités principales

- 🔐 Authentification des clients, chauffeurs et administrateurs
- 📅 Réservation de trajets avec détails (lieux, date, heure)
- 💳 Gestion des abonnements avec Stripe
- 📍 Calcul de distance & durée avec Mapbox
- 📬 Notifications :
  - Email via SMTP
  - SMS via Twilio
- 🤖 Chatbot de support (Rasa ou OpenAI)
- 🧾 Historique des trajets & profil utilisateur
- 📈 Tableau de bord Admin

---

## 🛠️ Technologies utilisées

| Catégorie         | Technologie                        |
|-------------------|-------------------------------------|
| Framework Web     | Django, Django REST Framework       |
| Base de données   | PostgreSQL                          |
| Paiement          | Stripe API                          |
| Notifications     | Twilio (SMS), SMTP (email)          |
| Cartographie      | Mapbox API                          |
| Authentification  | Django Auth                         |
| Sécurité          | Python-dotenv, gestion des tokens   |
| Asynchrone *(optionnel)* | Celery + Redis               |

---

## 📁 Structure du projet

vtc_backend/
├── core/ # Réservations, utils, notifications
├── users/ # Inscription, connexion, rôles (client/chauffeur/admin)
├── subscriptions/ # Abonnement et paiements Stripe
├── chatbot/ # Intégration avec Rasa/OpenAI
├── settings.py # Configuration Django
├── urls.py # Routes principales
└── .env # Clés API (non versionné)

#Créer un environnement virtuel
   python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

#Installer les dépendances
pip install -r requirements.txt

 #Créer un fichier .env : 
 
 SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=vtc_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Twilio
TWILIO_ACCOUNT_SID=xxxx
TWILIO_AUTH_TOKEN=xxxx
TWILIO_PHONE_NUMBER=+216xxxxxxx

# Stripe
STRIPE_SECRET_KEY=sk_test_XXXX
STRIPE_WEBHOOK_SECRET=whsec_XXXX

# Mapbox
MAPBOX_ACCESS_TOKEN=pk.XXXX

#Appliquer les migrations
python manage.py migrate

#Lancer le serveur
python manage.py runserver

