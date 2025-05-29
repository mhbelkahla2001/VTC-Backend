from django.contrib.auth.models import AbstractUser

from django.db import models
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('chauffeur', 'Chauffeur'),
        ('admin', 'Administrateur'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=15, blank=True, null=True)
    disponible = models.BooleanField(default=True)  # Ajout du champ disponibilité

    def __str__(self):
        return f"{self.username} ({self.role})"


class Reservation(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    chauffeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name="courses")

    pickup_location = models.CharField(max_length=255)
    pickup_lat = models.FloatField(null=True, blank=True)
    pickup_lng = models.FloatField(null=True, blank=True)

    destination = models.CharField(max_length=255)
    destination_lat = models.FloatField(null=True, blank=True)
    destination_lng = models.FloatField(null=True, blank=True)

    date = models.DateField()
    time = models.TimeField()

    status_choices = [
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='en_attente')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.username} → {self.destination} ({self.date} {self.time})"

class Payment(models.Model):
    reservation = models.OneToOneField('Reservation', on_delete=models.CASCADE)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_intent_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {self.id} - {self.amount}€"

class Abonnement(models.Model):
    TYPE_CHOICES = [
        ('mensuel', 'Mensuel'),
        ('annuel', 'Annuel'),
    ]

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='abonnements')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date_debut = models.DateField(auto_now_add=True)
    date_fin = models.DateField()

    def __str__(self):
        return f"{self.utilisateur.username} - {self.type} ({self.date_debut} → {self.date_fin})"

    def is_actif(self):
        from django.utils import timezone
        return self.date_fin >= timezone.now().date()

class Vehicule(models.Model):
    MARQUE_CHOICES = [
        ('Renault', 'Renault'),
        ('Peugeot', 'Peugeot'),
        ('Toyota', 'Toyota'),
        ('Mercedes', 'Mercedes'),
        ('Autre', 'Autre'),
    ]

    marque = models.CharField(max_length=50, choices=MARQUE_CHOICES)
    modele = models.CharField(max_length=50)
    immatriculation = models.CharField(max_length=20, unique=True)
    chauffeur = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'role': 'chauffeur'})
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.marque} {self.modele} - {self.immatriculation}"

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatbotLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
