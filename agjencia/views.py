
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.permissions import SAFE_METHODS

from .models import Prona, Klienti, Kerkesa, Vizita
from .serializers import (
    PronaSerializer,
    KlientiSerializer,
    KerkesaSerializer,
    VizitaSerializer,
)

class LejetEModeleve(DjangoModelPermissions):
    perms_map = {
        **DjangoModelPermissions.perms_map,
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
    }

class PronaViewSet(viewsets.ModelViewSet):
    queryset = Prona.objects.all()
    serializer_class = PronaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        perdoruesi = self.request.user

        if perdoruesi.is_superuser or perdoruesi.roli == 'administrator':
            return Prona.objects.all()

        return Prona.objects.filter(agjent=perdoruesi)

    def perform_create(self, serializer):
        serializer.save(agjent=self.request.user)



class KlientiViewSet(viewsets.ModelViewSet):
    queryset = Klienti.objects.all()
    serializer_class = KlientiSerializer
    permission_classes = [LejetEModeleve]


class KerkesaViewSet(viewsets.ModelViewSet):
    queryset = Kerkesa.objects.all()
    serializer_class = KerkesaSerializer
    permission_classes = [LejetEModeleve]


class VizitaViewSet(viewsets.ModelViewSet):
    queryset = Vizita.objects.all()
    serializer_class = VizitaSerializer
    permission_classes = [LejetEModeleve]
