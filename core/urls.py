from django.urls import path
from .views import update_profile

from .views import RegisterView, annuler_reservation, ChauffeurHistoryView, create_chauffeur, lister_utilisateurs, \
    supprimer_utilisateur, VehiculeListCreateView, VehiculeUpdateDeleteView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ReservationListCreateView
from .views import CreateStripeSessionView
from .views import AbonnementCreateView, AbonnementListAdminView, AbonnementStatusView
from .views import TrajetsDisponiblesView, accepter_trajet, mettre_a_jour_statut
from .views import AdminDashboardStats
from .views import get_current_user
from .views import chatbot_response

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('admin/create-chauffeur/', create_chauffeur),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('abonnements/stripe-session/', CreateStripeSessionView.as_view(), name='stripe-session'),    path('reservations/', ReservationListCreateView.as_view(), name='reservations'),
    path('abonnements/create/', AbonnementCreateView.as_view(), name='abonnement-create'),
    path('abonnements/', AbonnementListAdminView.as_view(), name='abonnement-list'),
    path('abonnement/status/', AbonnementStatusView.as_view(), name='abonnement-status'),
    path('chauffeur/accepter/<int:reservation_id>/', accepter_trajet),
    path('chauffeur/trajets/', TrajetsDisponiblesView.as_view(), name='chauffeur-trajets'),
    path('chauffeur/statut/<int:reservation_id>/', mettre_a_jour_statut, name='mettre-a-jour-statut'),
    path('chauffeur/historique/', ChauffeurHistoryView.as_view(), name='chauffeur-history'),
    path('admin/stats/', AdminDashboardStats.as_view(), name='admin-dashboard-stats'),
    path('me/', get_current_user, name='get-current-user'),
    path('client/annuler/<int:reservation_id>/', annuler_reservation, name='annuler-reservation'),
    path('profile/', get_current_user, name='profile'),
    path('admin/utilisateurs/', lister_utilisateurs),
    path('admin/utilisateurs/<int:user_id>/', supprimer_utilisateur),
    path('admin/vehicules/', VehiculeListCreateView.as_view()),
    path('admin/vehicules/<int:pk>/', VehiculeUpdateDeleteView.as_view()),
    path('profile/update/', update_profile, name='update-profile'),

    path('chatbot/', chatbot_response, name='chatbot_response'),

]
