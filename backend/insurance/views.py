# backend/insurance/views.py

from itertools import count
from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date, timedelta
from .models import Policy, Quote
from django.db.models import Count
from .serializers import QuoteSerializer, SimulateQuoteSerializer, PolicySerializer

from rest_framework.decorators import action

class QuoteViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Un utente può vedere solo i propri preventivi
        E SOLO quelli che non sono ancora stati convertiti in polizze.
        """
        user = self.request.user
        
        # --- ECCO LA MODIFICA ---
        # Aggiungiamo .filter(policy__isnull=True) per escludere
        # i preventivi che hanno una polizza collegata.
        return Quote.objects.filter(
            Q(user=user) | Q(email=user.email),
            policy__isnull=True
        )

    def perform_create(self, serializer):
        """
        Salva un preventivo associandolo all'utente loggato.
        Il prezzo viene ricalcolato per sicurezza.
        """
        # Ricalcoliamo il prezzo anche qui per non fidarci di quello
        # che potrebbe arrivare dal frontend.
        driving_style = serializer.validated_data.get('driving_style')
        vehicle_type = serializer.validated_data.get('vehicle_type')
        car_brand = serializer.validated_data.get('car_brand')
        license_year = serializer.validated_data.get('license_year')
        
        prezzo_calcolato = 500.00
        if driving_style == 'libera':
            prezzo_calcolato += 150.00
        if car_brand == 'FERRARI':
            prezzo_calcolato += 1000.00
        if (2025 - license_year) < 5:  # Neopatentato fittizio
            prezzo_calcolato += 200.00
        
        # Aggiungiamo logica per il tipo di veicolo
        if vehicle_type == 'moto':
            prezzo_calcolato += 100.00  # Le moto hanno un piccolo sovrapprezzo
        elif vehicle_type == 'autocarro':
            prezzo_calcolato += 300.00  # Gli autocarri hanno un sovrapprezzo maggiore
        
        # Salviamo il preventivo, associandolo FORZATAMENTE all'utente della richiesta.
        serializer.save(user=self.request.user, premium_price=prezzo_calcolato)

    @action(detail=False, methods=['delete'], url_path='clear-all')
    def clear_all(self, request):
        """
        Cancella tutti i preventivi dell'utente che non sono
        stati convertiti in polizze.
        """
        user = request.user
        
        # Selezioniamo solo i preventivi dell'utente che NON hanno una polizza associata.
        quotes_to_delete = Quote.objects.filter(user=user, policy__isnull=True)
        
        count = quotes_to_delete.count()
        quotes_to_delete.delete()
        
        # Restituiamo una risposta 204 No Content, che è lo standard per
        # una cancellazione avvenuta con successo.
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    

class SimulateQuoteView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        # Validiamo i dati in input con il nostro nuovo serializer
        serializer = SimulateQuoteSerializer(data=request.data)
        if serializer.is_valid():
            # Se i dati sono validi, li usiamo per il calcolo
            valid_data = serializer.validated_data
            
            # --- IL NOSTRO ALGORITMO ORA USA DATI VALIDATI ---
            prezzo_calcolato = 500.00
            
            if valid_data['driving_style'] == 'libera':
                prezzo_calcolato += 150.00
            if valid_data['car_brand'] == 'FERRARI':
                prezzo_calcolato += 1000.00
            if (2025 - valid_data['license_year']) < 5: # Neopatentato fittizio
                prezzo_calcolato += 200.00
            
            # Aggiungiamo logica per il tipo di veicolo
            if valid_data['vehicle_type'] == 'moto':
                prezzo_calcolato += 100.00  # Le moto hanno un piccolo sovrapprezzo
            elif valid_data['vehicle_type'] == 'autocarro':
                prezzo_calcolato += 300.00  # Gli autocarri hanno un sovrapprezzo maggiore
            # -----------------------------------------------

            return Response({'premium_price': prezzo_calcolato})
        
        # Se i dati non sono validi, DRF restituisce un errore 400 con i dettagli
        return Response(serializer.errors, status=400)
    
class PolicyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint di sola lettura per le polizze.
    Un utente può vedere solo le proprie polizze.
    Le polizze vengono create tramite un'azione separata (es. 'pagamento').
    """
    serializer_class = PolicySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Policy.objects.filter(user=self.request.user)
    
class PolicyStatsView(APIView):
    """
    Restituisce statistiche aggregate sulle polizze di un utente.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Calcola il numero di polizze attive per tipo di veicolo.
        """
        stats = Policy.objects.filter(
            user=request.user, 
            status='active'
        ).values(
            'quote__vehicle_type'
        ).annotate(
            # Invece di contare l'ID generico, contiamo le occorrenze
            # del campo per cui stiamo raggruppando. È più robusto.
            count=Count('quote__vehicle_type') 
        ).order_by('quote__vehicle_type')
        
        return Response(stats)


class CreatePolicyFromQuoteView(APIView):
    """
    Crea una nuova polizza a partire da un preventivo esistente.
    Simula il completamento di un pagamento.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        quote_id = request.data.get('quote_id')
        if not quote_id:
            return Response({'error': 'quote_id mancante'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quote = Quote.objects.get(id=quote_id, user=request.user)
        except Quote.DoesNotExist:
            return Response({'error': 'Preventivo non trovato o non autorizzato'}, status=status.HTTP_404_NOT_FOUND)

        # Controlla se esiste già una polizza per questo preventivo
        if Policy.objects.filter(quote=quote).exists():
            return Response({'error': 'Questo preventivo è già stato convertito in polizza'}, status=status.HTTP_409_CONFLICT)

        # Crea la polizza
        new_policy = Policy.objects.create(
            user=request.user,
            quote=quote,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            status='active',
            payment_status='paid' # Il pagamento è andato a buon fine!
        )

        serializer = PolicySerializer(new_policy)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class GlobalStatsView(APIView):
    """
    Restituisce statistiche globali, non legate a un singolo utente.
    Endpoint pubblico.
    """
    permission_classes = [permissions.AllowAny] # Chiunque può vederlo

    def get(self, request, format=None):
        total_policies_count = Policy.objects.count()
        return Response({'total_policies': total_policies_count})