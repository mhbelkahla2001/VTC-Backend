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

```
vtc_backend/
├── core/                 # Réservations, utils, notifications
├── users/                # Inscription, connexion, rôles (client/chauffeur/admin)
├── subscriptions/        # Abonnement et paiements Stripe
├── chatbot/              # Intégration avec Rasa/OpenAI
├── settings.py           # Configuration Django
├── urls.py               # Routes principales
└── .env                  # Clés API (non versionné)
```

---

## ⚙️ Installation locale

### 1. Cloner le dépôt

```bash
git clone https://github.com/mhbelkahla2001/pfe.git
cd vtc_backend
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Créer un fichier `.env`

```env
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
```

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

### 6. Lancer le serveur

```bash
python manage.py runserver
```

---

## 🧪 Tests de l’API

Utilisez **Postman** ou **cURL** pour tester les endpoints REST exposés via `api/`.

---

## 🛡️ Sécurité

> Toutes les **clés API** et **identifiants sensibles** sont stockés dans le fichier `.env` (non versionné).  
> ⚠️ **Ne jamais** les inclure dans un commit Git.

---

## 👨‍💻 Auteur

- **Nom** : Belkahla Mohamed Habib  
- 🎓 Projet de Fin d’Études – EPI Digital School  
- 📫 Email : benkahla.medhabib@hotmail.com

---

## 📝 Licence

Ce projet est destiné à un usage pédagogique et personnel. Pour toute réutilisation commerciale, merci de contacter l’auteur.
