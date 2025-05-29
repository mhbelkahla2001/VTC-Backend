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


---

## ⚙️ Installation locale

### 1. Cloner le dépôt

```bash
git clone https://github.com/mhbelkahla2001/pfe.git
cd vtc_backend


##2.Créer un environnement virtuel et l’activer
python -m venv .venv

# Sous Windows
.venv\Scripts\activate

# Sous macOS / Linux
source .venv/bin/activate

##3. Installer les dépendances
pip install -r requirements.txt

##4. Créer le fichier .env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données PostgreSQL
DB_NAME=vtc_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Twilio
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+216xxxxxxxx

# Stripe
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx

# Mapbox
MAPBOX_ACCESS_TOKEN=pk.xxxxxxxxxxxxxxxxx

##5. Appliquer les migrations
python manage.py migrate

##6. Lancer le serveur local
python manage.py runserver
