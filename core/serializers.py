
from .models import Reservation
from .models import Payment
from .models import Abonnement
from datetime import timedelta, date
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'password', 'confirm_password', 'role')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'phone': {'required': True},
            'role': {'default': 'client'}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un compte avec cet email existe déjà.")
        return value



class ReservationSerializer(serializers.ModelSerializer):
    client_username = serializers.CharField(source="client.username", read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['client', 'status', 'created_at']



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['client', 'payment_intent_id', 'status', 'created_at']


class AbonnementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abonnement
        fields = '__all__'
        read_only_fields = ['utilisateur', 'date_debut', 'date_fin']

    def create(self, validated_data):
        user = self.context['request'].user
        abonnement_type = validated_data.get('type')

        # Définir la durée selon le type
        if abonnement_type == 'mensuel':
            date_fin = date.today() + timedelta(days=30)
        else:
            date_fin = date.today() + timedelta(days=365)

        abonnement = Abonnement.objects.create(
            utilisateur=user,
            type=abonnement_type,
            date_fin=date_fin
        )
        return abonnement


from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role']


from .models import Vehicule

class VehiculeSerializer(serializers.ModelSerializer):
    chauffeur_nom = serializers.CharField(source='chauffeur.username', read_only=True)

    class Meta:
        model = Vehicule
        fields = '__all__'
