# backend/insurance/views.py

from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Quote
from .serializers import QuoteSerializer

class QuoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette la creazione e la visualizzazione dei preventivi.
    """
    serializer_class = QuoteSerializer

    def get_permissions(self):
        """
        Permette a chiunque (anche anonimi) di creare un preventivo (azione 'create').
        Richiede l'autenticazione per tutte le altre azioni (es. vedere la lista).
        """
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        """
        Un utente autenticato può vedere solo i propri preventivi
        (quelli associati al suo user ID o alla sua email).
        """
        user = self.request.user
        if user.is_authenticated:
            return Quote.objects.filter(Q(user=user) | Q(email=user.email))
        return Quote.objects.none()

    def perform_create(self, serializer):
        """
        Logica custom eseguita al momento della creazione di un nuovo preventivo.
        """
        # Il nostro super-algoritmo di calcolo del premio!
        prezzo_calcolato = 500.00 

        # Se l'utente che fa la richiesta è autenticato, lo associamo al preventivo.
        if self.request.user.is_authenticated:
            serializer.save(premium_price=prezzo_calcolato, user=self.request.user)
        else:
            # Altrimenti, salviamo il preventivo senza utente associato.
            serializer.save(premium_price=prezzo_calcolato)


class CarBrandsView(APIView):
    """
    Una vista pubblica per ottenere la lista delle marche di auto.
    """
    permission_classes = [permissions.AllowAny] # Tutti possono accedere

    def get(self, request, format=None):
        """
        Restituisce una lista hardcodata di marche di auto.
        """
        car_brands = [
            "ALFA ROMEO", "ALPINA-BMW", "ARIEL", "ASTON MARTIN", "AUDI",
            "BENTLEY", "BMW", "BOXEL", "BREMACH", "CADILLAC", "CATERHAM",
            "CHEVROLET", "CHRYSLER", "CITROEN", "DAEWOO", "DAIHATSU",
            "DE TOMASO", "FERRARI", "FIAT", "FORD", "HONDA", "HYUNDAI",
            "ISUZU", "JAGUAR", "JEEP", "KIA", "LADA", "LAMBORGHINI",
            "LANCIA", "LAND ROVER", "LEXUS", "LOTUS", "MARCOS", "MASERATI",
            "MAZDA", "MAZZIERI", "MERCEDES", "MG", "MINI", "MITSUBISHI",
            "MORGAN", "NISSAN", "OPEL", "PAGANI", "PEUGEOT", "PORSCHE",
            "QVALE", "RENAULT", "RENAULT V.I.", "ROLLS ROYCE", "ROVER",
            "SAAB", "SEAT", "SKODA", "SMART", "SSANGYONG", "SUBARU",
            "SUZUKI", "TATA", "TOYOTA", "TVR", "VENTURI", "VOLKSWAGEN", "VOLVO"
        ]
        return Response(car_brands)