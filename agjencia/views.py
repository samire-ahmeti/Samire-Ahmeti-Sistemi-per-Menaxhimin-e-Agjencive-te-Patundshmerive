
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.permissions import SAFE_METHODS
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

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

@login_required(login_url="/admin/login/")
def pronat_page(request):

    qyteti = request.GET.get("qyteti", "").strip()
    lloji = request.GET.get("lloji", "").strip()

    perdoruesi = request.user

    if perdoruesi.is_superuser or perdoruesi.roli == "administrator":
        pronat = Prona.objects.all()

    else:

        pronat = Prona.objects.filter(
            agjent=perdoruesi
        )


    if qyteti:
        pronat = pronat.filter(
            qyteti__icontains=qyteti
        )


    if lloji:
        pronat = pronat.filter(
            lloji__iexact=lloji
        )


    pronat = pronat.order_by("-id")

    context = {
        "pronat": pronat,
        "qyteti": qyteti,
        "lloji": lloji,
    }

    return render(
        request,
        "agjencia/pronat.html",
        context
    )


@login_required(login_url="/admin/login/")
def detajet_prones(request, prona_id):
    perdoruesi = request.user

    if perdoruesi.is_superuser or perdoruesi.roli == "administrator":
        pronat = Prona.objects.all()
    else:
        pronat = Prona.objects.filter(agjent=perdoruesi)

    prona = get_object_or_404(pronat, id=prona_id)

    return render(
        request,
        "agjencia/detajet_prones.html",
        {"prona": prona}
    )


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Prona, Klienti, Vizita


@login_required(login_url="/admin/login/")
def paneli_page(request):
    perdoruesi = request.user

    if perdoruesi.is_superuser or perdoruesi.roli == "administrator":
        pronat = Prona.objects.all()
        numri_klienteve = Klienti.objects.count()
        numri_vizitave = Vizita.objects.count()
    else:
        pronat = Prona.objects.filter(agjent=perdoruesi)
        vizitat = Vizita.objects.filter(prona__agjent=perdoruesi)

        numri_vizitave = vizitat.count()
        numri_klienteve = Klienti.objects.filter(
            id__in=vizitat.values_list("klienti_id", flat=True)
        ).count()

    context = {
        "numri_pronave": pronat.count(),
        "numri_klienteve": numri_klienteve,
        "numri_vizitave": numri_vizitave,
        "pronat_e_fundit": pronat.order_by("-id")[:4],
    }

    return render(request, "agjencia/paneli.html", context)
