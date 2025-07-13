"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include, reverse_lazy
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from insurance import views
from insurance.views import VehicleDataView

# Inizializza il router
router = DefaultRouter()
# Registra la nostra QuoteViewSet sotto il percorso 'quotes'
router.register(r'quotes', views.QuoteViewSet, basename='quote')

urlpatterns = [
    # URL per l'admin di Django
    path('admin/', admin.site.urls),

    # Quando si visita la radice (''), reindirizza a swagger-ui
    path('', RedirectView.as_view(url=reverse_lazy('swagger-ui'), permanent=False), name='index'),

    # URL per le API di autenticazione
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    # Download del file OpenAPI schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Estendi le URL del router per le quote
    path('api/', include(router.urls)),

    # Public API
    path('api/vehicle-data/<str:vehicle_type>/<str:data_type>/', VehicleDataView.as_view(), name='vehicle-data'),

]
