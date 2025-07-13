# backend/insurance/models.py

from django.db import models
from django.contrib.auth.models import User

class Quote(models.Model):
    # L'utente associato. Può essere nullo per i preventivi anonimi.
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Dati anagrafici, ORA OPZIONALI.
    # Saranno compilati SOLO se l'utente non è loggato.
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True) # Anche l'email è opzionale qui

    # Dati del veicolo (questi sono sempre necessari)
    car_brand = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=10)
    birth_date = models.DateField()
    license_year = models.IntegerField()

    # Risultato
    premium_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Logica per mostrare il nome corretto
        if self.user:
            return f"Preventivo per {self.user.get_full_name()} - €{self.premium_price}"
        return f"Preventivo per {self.first_name} {self.last_name} - €{self.premium_price}"