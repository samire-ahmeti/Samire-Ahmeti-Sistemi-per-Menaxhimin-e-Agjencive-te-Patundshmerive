from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Prona, Klienti, Kerkesa, Vizita
from .serializers import (
    PronaSerializer,
    KlientiSerializer,
    KerkesaSerializer,
    VizitaSerializer,
)


class PronaViewSet(viewsets.ModelViewSet):
    queryset = Prona.objects.all()
    serializer_class = PronaSerializer
    permission_classes = [IsAuthenticated]


class KlientiViewSet(viewsets.ModelViewSet):
    queryset = Klienti.objects.all()
    serializer_class = KlientiSerializer
    permission_classes = [IsAuthenticated]


class KerkesaViewSet(viewsets.ModelViewSet):
    queryset = Kerkesa.objects.all()
    serializer_class = KerkesaSerializer
    permission_classes = [IsAuthenticated]


class VizitaViewSet(viewsets.ModelViewSet):
    queryset = Vizita.objects.all()
    serializer_class = VizitaSerializer
    permission_classes = [IsAuthenticated]