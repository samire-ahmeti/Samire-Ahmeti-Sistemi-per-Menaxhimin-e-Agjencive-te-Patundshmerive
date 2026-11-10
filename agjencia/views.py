
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from .models import Prona, Klienti, Kerkesa, Vizita
from .serializers import (
    PronaSerializer,
    KlientiSerializer,
    KerkesaSerializer,
    VizitaSerializer,
)


def pronat_e_perdoruesit(perdoruesi):
    if perdoruesi.is_superuser or perdoruesi.roli == "administrator":
        return Prona.objects.all()

    if perdoruesi.roli == "agjent":
        return Prona.objects.filter(agjent=perdoruesi)

    raise PermissionDenied


class LejetEModeleve(DjangoModelPermissions):
    perms_map = {
        **DjangoModelPermissions.perms_map,
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": ["%(app_label)s.view_%(model_name)s"],
    }


class PronaViewSet(viewsets.ModelViewSet):
    queryset = Prona.objects.all()
    serializer_class = PronaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return pronat_e_perdoruesit(self.request.user)

    def perform_create(self, serializer):
        perdoruesi = self.request.user

        if not (
            perdoruesi.is_superuser
            or perdoruesi.roli in ["administrator", "agjent"]
        ):
            raise PermissionDenied

        serializer.save(agjent=perdoruesi)


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


@login_required(login_url="/hyrja/")
def pronat_page(request):
    qyteti = request.GET.get("qyteti", "").strip()
    lloji = request.GET.get("lloji", "").strip()

    pronat = pronat_e_perdoruesit(request.user)

    if qyteti:
        pronat = pronat.filter(qyteti__icontains=qyteti)

    if lloji:
        pronat = pronat.filter(lloji__iexact=lloji)

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


@login_required(login_url="/hyrja/")
def detajet_prones(request, prona_id):
    pronat = pronat_e_perdoruesit(request.user)

    prona = get_object_or_404(
        pronat,
        id=prona_id
    )

    return render(
        request,
        "agjencia/detajet_prones.html",
        {"prona": prona}
    )


@login_required(login_url="/hyrja/")
def paneli_page(request):
    perdoruesi = request.user

    eshte_administrator = (
        perdoruesi.is_superuser
        or perdoruesi.roli == "administrator"
    )

    eshte_agjent = perdoruesi.roli == "agjent"

    if not eshte_administrator and not eshte_agjent:
        raise PermissionDenied

    pronat = pronat_e_perdoruesit(perdoruesi)

    if eshte_administrator:
        numri_klienteve = Klienti.objects.count()
        numri_vizitave = Vizita.objects.count()
    else:
        vizitat = Vizita.objects.filter(
            prona__agjent=perdoruesi
        )

        numri_vizitave = vizitat.count()

        numri_klienteve = Klienti.objects.filter(
            id__in=vizitat.values_list(
                "klienti_id",
                flat=True
            )
        ).count()

    context = {
        "numri_pronave": pronat.count(),
        "numri_klienteve": numri_klienteve,
        "numri_vizitave": numri_vizitave,
        "pronat_e_fundit": pronat.order_by("-id")[:4],
    }

    return render(
        request,
        "agjencia/paneli.html",
        context
    )


def hyrja_page(request):
    if request.user.is_authenticated:
        if (
            request.user.is_superuser
            or request.user.roli in ["administrator", "agjent"]
        ):
            return redirect("paneli")

    context = {
        "next": (
            request.GET.get("next", "")
            if request.method == "GET"
            else request.POST.get("next", "")
        )
    }

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        perdoruesi = authenticate(
            request,
            username=username,
            password=password
        )

        if perdoruesi is not None:
            lejohet_hyrja = (
                perdoruesi.is_superuser
                or perdoruesi.roli in ["administrator", "agjent"]
            )

            if lejohet_hyrja:
                login(request, perdoruesi)

                destinacioni = context["next"]

                if destinacioni and url_has_allowed_host_and_scheme(
                    url=destinacioni,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure()
                ):
                    return redirect(destinacioni)

                return redirect("paneli")

        context["gabimi"] = (
            "Emri i përdoruesit ose fjalëkalimi është i pasaktë, "
            "ose nuk keni leje për të hyrë në sistem."
        )

        context["emri_perdoruesit"] = username

    return render(
        request,
        "agjencia/hyrja.html",
        context
    )
@login_required(login_url="/hyrja/")
@require_POST
def dalja_page(request):
    logout(request)
    return redirect("hyrja")
