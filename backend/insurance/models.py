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

    VEHICLE_TYPE_CHOICES = [
        ('auto', 'Auto'),
        ('moto', 'Moto'),
        ('autocarro', 'Autocarro'),
    ]

    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES, default='auto')

    # Risultato
    premium_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Preventivo per {self.user.get_full_name()} - €{self.premium_price}"
        return f"Preventivo per {self.first_name} {self.last_name} - €{self.premium_price}"
    
class Policy(models.Model):
    # Riferimento obbligatorio all'utente che possiede la polizza.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Riferimento 1-a-1 al preventivo da cui è nata questa polizza.
    # Quando un preventivo diventa una polizza, non può essere riutilizzato.
    quote = models.OneToOneField(Quote, on_delete=models.CASCADE)

    # Stato della polizza per tracciarne il ciclo di vita.
    STATUS_CHOICES = [
        ('active', 'Attiva'),
        ('expired', 'Scaduta'),
        ('cancelled', 'Annullata'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    # Date di validità della polizza.
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Stato del pagamento.
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Non Pagata'),
        ('paid', 'Pagata'),
        ('failed', 'Fallita'),
    ]
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __str__(self):
        return f"Polizza #{self.id} per {self.user.username} - Scadenza: {self.end_date}"