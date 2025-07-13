# backend/insurance/models.py

from django.db import models
from django.contrib.auth.models import User

class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    # Dati Veicolo
    car_brand = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=10)
    
    km_per_year = models.CharField(max_length=20) # Es. "5000-10000"
    
    DRIVING_STYLE_CHOICES = [
        ('esclusiva', 'Guida Esclusiva'),
        ('esperta', 'Guida Esperta'),
        ('libera', 'Guida Libera'),
    ]
    driving_style = models.CharField(max_length=10, choices=DRIVING_STYLE_CHOICES, default='esperta')

    # Dati Anagrafici
    birth_date = models.DateField()
    license_year = models.IntegerField()

    # Risultato
    premium_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Preventivo per {self.user.get_full_name()} - €{self.premium_price}"
        return f"Preventivo per {self.first_name} {self.last_name} - €{self.premium_price}"