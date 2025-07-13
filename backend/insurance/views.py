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

BRANDS_DATA = {
    'auto': [
            "ALFA ROMEO", "ALPINA-BMW", "ARIEL", "ASTON MARTIN", "AUDI",
            "BENTLEY", "BMW", "BOXEL", "BREMACH", "CADILLAC", "CATERHAM",
            "CHEVROLET", "CHRYSLER", "CITROEN", "DAEWOO", "DAIHATSU",
            "DE TOMASO", "FERRARI", "FIAT", "FORD", "HONDA", "HYUNDAI",
            "ISUZU", "JAGUAR", "JEEP", "KIA", "LADA", "LAMBORGHINI",
            "LANCIA", "LAND ROVER", "LEXUS", "LOTUS", "MARCOS", "MASERATI",
            "MAZDA", "MAZZIERI", "MERCEDES", "MG", "MINI", "MITSUBISHI",
            "MORGAN", "NISSAN", "OPEL", "PEUGEOT", "PORSCHE",
            "QVALE", "RENAULT", "RENAULT V.I.", "ROLLS ROYCE", "ROVER",
            "SAAB", "SEAT", "SKODA", "SMART", "SSANGYONG", "SUBARU",
            "TATA", "TOYOTA", "TVR", "VENTURI", "VOLKSWAGEN", "VOLVO"
    ],
    'moto': [
        "APRILIA", "BMW", "DUCATI", "HARLEY-DAVIDSON", "HONDA", "KAWASAKI",
        "KTM", "MOTO GUZZI", "MV AGUSTA", "PIAGGIO", "SUZUKI", "TRIUMPH", "YAMAHA"
    ],
    'autocarro': [
        "IVECO", "MAN", "MERCEDES-BENZ TRUCKS", "RENAULT TRUCKS", 
        "SCANIA", "VOLVO TRUCKS"
    ]
}

class VehicleDataView(APIView):
    """
    Vista pubblica per ottenere dati specifici per tipo di veicolo.
    Esempio: /api/vehicle-data/auto/brands/
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, vehicle_type, data_type, format=None):
        """
        Restituisce dati specifici (es. 'brands') per un tipo di veicolo.
        """
        if data_type == 'brands':
            # Controlla se il tipo di veicolo esiste nei nostri dati
            if vehicle_type in BRANDS_DATA:
                return Response(BRANDS_DATA[vehicle_type])
            else:
                # Se il tipo non esiste, restituisci un 404 Not Found
                return Response({"error": f"Tipo di veicolo '{vehicle_type}' non trovato."}, status=404)
        
        # In futuro, potremmo avere altri tipi di dati, es. /models/
        return Response({"error": f"Tipo di dati '{data_type}' non supportato."}, status=400)