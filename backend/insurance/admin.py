# backend/insurance/admin.py

from django.contrib import admin
from .models import Quote # Importiamo i nostri modelli

# Registriamo i modelli per renderli visibili nel pannello di amministrazione
admin.site.register(Quote)