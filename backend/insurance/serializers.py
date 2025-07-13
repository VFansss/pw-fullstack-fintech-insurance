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
        # Elenchiamo tutti i campi del nostro modello Quote
        fields = '__all__' 
        # Diciamo a DRF che alcuni campi sono calcolati dal server
        # e non devono essere forniti dal client durante la creazione.
        read_only_fields = ['premium_price', 'user', 'created_at']