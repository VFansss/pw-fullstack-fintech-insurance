# backend/insurance/serializers.py

from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Quote, Policy
from rest_framework import serializers

# Questa classe personalizzata eredita dal serializzatore di registrazione
# e aggiunge i campi first_name e last_name
class CustomRegisterSerializer(RegisterSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._has_phone_field = False  # oppure True se hai un campo phone
        
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        return data
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        return user

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

class NestedQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        # Specifichiamo ESATTAMENTE i campi che vogliamo vedere.
        fields = ['car_brand', 'car_model', 'license_plate', 'vehicle_type','driving_style', 'premium_price']

class PolicySerializer(serializers.ModelSerializer):
    # Diciamo a DRF di usare il nostro nuovo
    # serializer "leggero" per rappresentare il campo 'quote'.
    # `read_only=True` assicura che questo campo sia solo per la lettura.
    quote = NestedQuoteSerializer(read_only=True)

    class Meta:
        model = Policy
        fields = '__all__' # Mostriamo tutti i campi della polizza, più il 'quote' annidato.

