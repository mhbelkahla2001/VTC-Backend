from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer
from rest_framework import generics, permissions
from .serializers import ReservationSerializer
import stripe
from .models import Payment
from .utils import send_reservation_email
from .models import User
from .utils import send_sms
from .utils import get_coordinates
from .serializers import AbonnementSerializer
from .permissions import IsClient
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.utils import timezone
from django.db.models import Count, Sum
from .models import Abonnement
from rest_framework.permissions import IsAuthenticated
from .models import Reservation
from .serializers import UserSerializer
from .models import Vehicule
from .serializers import VehiculeSerializer
from openai import OpenAI
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from .models import ChatbotLog
import os
from dotenv import load_dotenv
load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data.copy()

        # Force le rôle "client" à l'inscription
        data['role'] = 'client'

        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Utilisateur client créé avec succès."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_chauffeur(request):
    data = request.data.copy()
    data['role'] = 'chauffeur'  # Forcer le rôle
    serializer = UserRegisterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Chauffeur créé avec succès."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework_simplejwt.views import TokenObtainPairView
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsClient]

    def get_queryset(self):
        return Reservation.objects.filter(client=self.request.user)

    def perform_create(self, serializer):
        user: User = self.request.user  # Typage explicite pour l'autocomplétion et éviter les erreurs
        reservation = serializer.save(client=user)
        # Géolocalisation Mapbox
        pickup_lat, pickup_lng = get_coordinates(reservation.pickup_location)
        dest_lat, dest_lng = get_coordinates(reservation.destination)

        reservation.pickup_lat = pickup_lat
        reservation.pickup_lng = pickup_lng
        reservation.destination_lat = dest_lat
        reservation.destination_lng = dest_lng
        reservation.save()
        if user.is_authenticated:
            send_reservation_email(
                to_email=user.email,
                username=user.username,
                pickup=reservation.pickup_location,
                destination=reservation.destination,
                date=reservation.date,
                time=reservation.time
            )
        # Envoi SMS si numéro présent
        if self.request.user.phone:
            sms_message = (
                f"Bonjour {self.request.user.username}, votre trajet vers "
                f"{reservation.destination} est réservé pour le {reservation.date} à {reservation.time}."
            )
            try:
                send_sms(self.request.user.phone, sms_message)
            except Exception as e:
                print("Erreur envoi SMS:", e)



class CreateStripeSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        abonnement_type = request.data.get('type')

        if abonnement_type not in ['mensuel', 'annuel']:
            return Response({'error': 'Type d\'abonnement invalide'}, status=400)

        # Création de la session Stripe
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': f"Abonnement {abonnement_type}",
                    },
                    'unit_amount': 999 if abonnement_type == 'mensuel' else 9999,  # 9.99€ ou 99.99€
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'http://localhost:3000/success',
            cancel_url=f'http://localhost:3000/cancel',
        )

        # Enregistrement du paiement dans la base de données
        Abonnement.objects.create(
            utilisateur=user,
            type=abonnement_type,
            date_fin='2023-12-31',  # Exemple de date
        )

        return Response({'checkout_url': session.url})




class AbonnementCreateView(generics.CreateAPIView):
    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        if request.user.role == 'chauffeur':
            return Response({'error': 'Les chauffeurs ne peuvent pas souscrire à un abonnement.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def get_serializer_context(self):
        return {'request': self.request}

class AbonnementListAdminView(generics.ListAPIView):
    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerializer
    permission_classes = [permissions.IsAdminUser]

class AbonnementStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        latest_abonnement = Abonnement.objects.filter(utilisateur=request.user).order_by('-date_fin').first()
        if latest_abonnement and latest_abonnement.is_actif():
            return Response({'abonne': True, 'date_fin': latest_abonnement.date_fin})
        return Response({'abonne': False})


from .permissions import IsChauffeur


from .permissions import IsAdmin
class AbonnementListAdminView(generics.ListAPIView):
    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerializer
    permission_classes = [IsAdmin]




class TrajetsDisponiblesView(APIView):
    permission_classes = [IsAuthenticated, IsChauffeur]

    def get(self, request):
        trajets_disponibles = Reservation.objects.filter(status='en_attente', chauffeur__isnull=True)
        serializer = ReservationSerializer(trajets_disponibles, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsChauffeur])
def accepter_trajet(request, reservation_id):
    try:
        trajet = Reservation.objects.get(id=reservation_id, status='en_attente', chauffeur__isnull=True)
        trajet.chauffeur = request.user
        trajet.status = 'acceptee'
        trajet.save()
        return Response({'message': 'Trajet accepté.'})
    except Reservation.DoesNotExist:
        return Response({'error': 'Trajet non trouvé ou déjà pris.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsChauffeur])
def mettre_a_jour_statut(request, reservation_id):
    nouveau_statut = request.data.get('status')
    try:
        trajet = Reservation.objects.get(id=reservation_id, chauffeur=request.user)
        if nouveau_statut not in ['acceptee', 'terminee', 'refusee', 'annulee']:
            return Response({'error': 'Statut invalide'}, status=400)
        trajet.status = nouveau_statut
        trajet.save()
        return Response({'message': f'Statut mis à jour : {nouveau_statut}'})
    except Reservation.DoesNotExist:
        return Response({'error': 'Trajet non trouvé ou non autorisé.'}, status=404)

class ChauffeurHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsChauffeur]
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(chauffeur=self.request.user)



class AdminDashboardStats(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Utilisateurs
        total_clients = User.objects.filter(role='client').count()
        total_chauffeurs = User.objects.filter(role='chauffeur').count()

        # Réservations
        total_reservations = Reservation.objects.count()
        reservations_par_statut = Reservation.objects.values('status').annotate(total=Count('id'))

        # Abonnements actifs
        abonnements_actifs = Abonnement.objects.filter(date_fin__gte=timezone.now().date()).count()

        # Paiements réussis
        total_revenus = Payment.objects.filter(status='terminee').aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            'total_clients': total_clients,
            'total_chauffeurs': total_chauffeurs,
            'total_reservations': total_reservations,
            'reservations_par_statut': reservations_par_statut,
            'abonnements_actifs': abonnements_actifs,
            'total_revenus': float(total_revenus),
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsClient])
def annuler_reservation(request, reservation_id):
    try:
        trajet = Reservation.objects.get(id=reservation_id, client=request.user)
        if trajet.status in ['acceptee', 'en_attente']:
            trajet.status = 'annulee'
            trajet.save()
            return Response({'message': 'Réservation annulée avec succès.'})
        return Response({'error': 'Réservation déjà traitée.'}, status=400)
    except Reservation.DoesNotExist:
        return Response({'error': 'Réservation introuvable.'}, status=404)



@api_view(['GET'])
@permission_classes([IsAdminUser])
def lister_utilisateurs(request):
    role = request.query_params.get('role')
    if role in ['client', 'chauffeur']:
        users = User.objects.filter(role=role)
    else:
        users = User.objects.exclude(role='admin')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def supprimer_utilisateur(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if user.role == 'admin':
            return Response({'error': "Impossible de supprimer un admin."}, status=403)
        user.delete()
        return Response({'message': "Utilisateur supprimé avec succès."})
    except User.DoesNotExist:
        return Response({'error': "Utilisateur introuvable."}, status=404)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.save()
    return Response({
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "role": user.role,
    })


    def get_object(self):
        return self.request.user



class VehiculeListCreateView(generics.ListCreateAPIView):
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer
    permission_classes = [IsAdminUser]

class VehiculeUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer
    permission_classes = [IsAdminUser]





@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def chatbot_response(request):
    message = request.data.get("message", "")
    system_prompt = request.data.get("prompt", "Vous êtes un assistant très formel pour un service VTC.")

    if not message:
        return Response({"error": "Message requis"}, status=400)

    # Réponse locale depuis la base si l'utilisateur est connecté
    if request.user.is_authenticated:
        try:
            reponse_locale = traiter_demande_client(message, request.user)
            if "Je n'ai pas compris" not in reponse_locale:
                ChatbotLog.objects.create(
                    user=request.user,
                    message=message,
                    response=reponse_locale
                )
                return Response({"reply": reponse_locale})
        except Exception:
            pass  # Poursuit vers OpenAI en cas d’erreur locale

    # Réponse par OpenAI si pas de réponse locale
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ]
        )
        reply = response.choices[0].message.content

        ChatbotLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            message=message,
            response=reply
        )

        return Response({"reply": reply})
    except Exception as e:
        return Response({"error": str(e)}, status=500)



def traiter_demande_client(message: str, user) -> str:
    message = message.lower()

    # Statut de la dernière réservation
    if "réservation" in message and ("statut" in message or "où" in message or "état" in message):
        reservations = Reservation.objects.filter(client=user).order_by('-created_at')
        if reservations.exists():
            r = reservations.first()
            return f"Votre dernière réservation vers {r.destination} est au statut '{r.status}'."
        else:
            return "Vous n'avez pas encore de réservation enregistrée."

    # Abonnement actif
    elif "abonnement" in message and ("actif" in message or "statut" in message):
        abonnement = Abonnement.objects.filter(utilisateur=user, date_fin__gte=timezone.now().date()).first()
        if abonnement:
            return f"Votre abonnement {abonnement.type} est actif jusqu'au {abonnement.date_fin}."
        else:
            return "Vous ne possédez pas d'abonnement actif pour le moment."

    # Nombre de réservations
    elif "combien" in message and "réservation" in message:
        count = Reservation.objects.filter(client=user).count()
        return f"Vous avez effectué un total de {count} réservations."

    # Paiements terminés
    elif "paiement" in message and ("réussi" in message or "effectué" in message or "terminé" in message):
        total = Payment.objects.filter(user=user, status='terminee').aggregate(Sum('amount'))['amount__sum'] or 0
        return f"Vous avez effectué des paiements pour un total de {total:.2f} €."

    # Prochain trajet prévu
    elif "prochain" in message and ("trajet" in message or "réservation" in message):
        trajet = Reservation.objects.filter(client=user, date__gte=timezone.now().date()).order_by('date').first()
        if trajet:
            return f"Votre prochain trajet est prévu le {trajet.date} à {trajet.time} vers {trajet.destination}."
        else:
            return "Aucun trajet prévu pour les prochains jours."

    # Historique des trajets acceptés pour les chauffeurs
    elif user.role == 'chauffeur' and "trajets" in message and ("accepté" in message or "effectué" in message):
        trajets = Reservation.objects.filter(chauffeur=user).count()
        return f"Vous avez accepté ou effectué {trajets} trajets."

    # Véhicule attribué
    elif user.role == 'chauffeur' and "véhicule" in message:
        vehicule = Vehicule.objects.filter(chauffeur=user).first()
        if vehicule:
            return f"Votre véhicule actuel est une {vehicule.marque} {vehicule.modele} immatriculée {vehicule.plaque}."
        else:
            return "Aucun véhicule ne vous a été attribué pour le moment."

    return "Je n'ai pas compris votre demande. Pourriez-vous la reformuler s'il vous plaît ?"



