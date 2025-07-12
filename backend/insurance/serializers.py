# backend/insurance/serializers.py

from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

# Questa classe personalizzata eredita dal serializzatore di registrazione
# e aggiunge un campo "finto" che allauth si aspetta.
class CustomRegisterSerializer(RegisterSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._has_phone_field = False  # oppure True se hai un campo phone