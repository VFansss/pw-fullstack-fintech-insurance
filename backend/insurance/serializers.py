# backend/insurance/serializers.py

from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Quote
from rest_framework import serializers

# Questa classe personalizzata eredita dal serializzatore di registrazione
# e aggiunge un campo "finto" che allauth si aspetta.
class CustomRegisterSerializer(RegisterSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._has_phone_field = False  # oppure True se hai un campo phone

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = '__all__'
        read_only_fields = ['premium_price', 'user', 'created_at']

class SimulateQuoteSerializer(serializers.Serializer):
    """
    Valida i dati in input per la simulazione del preventivo.
    Non è legato a un modello, valida solo i dati.
    """
    car_brand = serializers.CharField(max_length=50)
    car_model = serializers.CharField(max_length=50)
    license_plate = serializers.CharField(max_length=10)
    km_per_year = serializers.CharField(max_length=20)
    driving_style = serializers.ChoiceField(choices=Quote.DRIVING_STYLE_CHOICES)
    birth_date = serializers.DateField()
    license_year = serializers.IntegerField()

    class Meta:
        # Questo serializer non ha un modello perché non scrive sul DB
        pass