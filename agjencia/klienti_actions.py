
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .klienti_forms import KlientiForm
from .models import Klienti


def eshte_administrator(perdoruesi):
    return (
        perdoruesi.is_superuser
        or perdoruesi.roli == "administrator"
    )


def kontrollo_rolin(perdoruesi):
    if not (
        eshte_administrator(perdoruesi)
        or perdoruesi.roli == "agjent"
    ):
        raise PermissionDenied


def kontrollo_menaxhimin(perdoruesi):
    if not eshte_administrator(perdoruesi):
        raise PermissionDenied


def klientet_e_perdoruesit(perdoruesi):
    kontrollo_rolin(perdoruesi)

    if eshte_administrator(perdoruesi):
        return Klienti.objects.all()

    return Klienti.objects.filter(
        Q(kerkesat__prona__agjent=perdoruesi)
        | Q(vizitat__prona__agjent=perdoruesi)
    ).distinct()


@login_required(login_url="/hyrja/")
@require_http_methods(["GET"])
def klientet_page(request):
    kerkimi = request.GET.get("q", "").strip()[:100]

    klientet = klientet_e_perdoruesit(request.user)

    if kerkimi:
        klientet = klientet.filter(
            Q(emri__icontains=kerkimi)
            | Q(kontakti__icontains=kerkimi)
        )

    klientet = klientet.order_by("emri", "id")

    return render(
        request,
        "agjencia/klientet.html",
        {
            "klientet": klientet,
            "kerkimi": kerkimi,
            "mund_te_menaxhoje": eshte_administrator(request.user),
        }
    )


@login_required(login_url="/hyrja/")
@require_http_methods(["GET", "POST"])
def shto_klient_page(request):
    kontrollo_menaxhimin(request.user)

    if request.method == "POST":
        form = KlientiForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Klienti u regjistrua me sukses."
            )

            return redirect("klientet")
    else:
        form = KlientiForm()

    return render(
        request,
        "agjencia/shto_klient.html",
        {"form": form}
    )


@login_required(login_url="/hyrja/")
@require_http_methods(["GET", "POST"])
def ndrysho_klient_page(request, klienti_id):
    kontrollo_menaxhimin(request.user)

    klienti = get_object_or_404(
        Klienti,
        pk=klienti_id
    )

    if request.method == "POST":
        form = KlientiForm(
            request.POST,
            instance=klienti
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Të dhënat e klientit u përditësuan me sukses."
            )

            return redirect("klientet")
    else:
        form = KlientiForm(instance=klienti)

    return render(
        request,
        "agjencia/ndrysho_klient.html",
        {
            "form": form,
            "klienti": klienti,
        }
    )


@login_required(login_url="/hyrja/")
@require_http_methods(["GET", "POST"])
def fshi_klient_page(request, klienti_id):
    kontrollo_menaxhimin(request.user)

    klienti = get_object_or_404(
        Klienti,
        pk=klienti_id
    )

    if request.method == "POST":
        try:
            klienti.delete()

            messages.success(
                request,
                "Klienti u fshi me sukses."
            )

            return redirect("klientet")

        except ProtectedError:
            messages.error(
                request,
                "Klienti nuk mund të fshihet sepse "
                "ka kërkesa ose vizita të lidhura me të."
            )

            return redirect(
                "fshi_klient",
                klienti_id=klienti.id
            )

    return render(
        request,
        "agjencia/fshi_klient.html",
        {"klienti": klienti}
    )
