
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import Prona, Vizita
from .vizita_forms import VizitaForm


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


def vizitat_e_perdoruesit(perdoruesi):
    kontrollo_rolin(perdoruesi)

    if eshte_administrator(perdoruesi):
        return Vizita.objects.all()

    return Vizita.objects.filter(
        prona__agjent=perdoruesi
    )


def pergatit_formen(form, perdoruesi):
    kontrollo_rolin(perdoruesi)

    if not eshte_administrator(perdoruesi):
        form.fields["prona"].queryset = (
            Prona.objects.filter(
                agjent=perdoruesi
            ).order_by("qyteti", "id")
        )

    return form


@login_required(login_url="/hyrja/")
@require_http_methods(["GET"])
def vizitat_page(request):
    kerkimi = request.GET.get("q", "").strip()[:100]

    vizitat = vizitat_e_perdoruesit(
        request.user
    ).select_related(
        "klienti",
        "prona",
        "prona__agjent"
    )

    if kerkimi:
        vizitat = vizitat.filter(
            Q(klienti__emri__icontains=kerkimi)
            | Q(klienti__kontakti__icontains=kerkimi)
            | Q(prona__qyteti__icontains=kerkimi)
        )

    vizitat = vizitat.order_by(
        "-data_vizites",
        "-id"
    )

    return render(
        request,
        "agjencia/vizitat.html",
        {
            "vizitat": vizitat,
            "kerkimi": kerkimi,
            "numri_vizitave": vizitat.count(),
        }
    )


@login_required(login_url="/hyrja/")
@require_http_methods(["GET", "POST"])
def shto_vizite_page(request):
    kontrollo_rolin(request.user)

    if request.method == "POST":
        form = VizitaForm(request.POST)
    else:
        form = VizitaForm()

    form = pergatit_formen(
        form,
        request.user
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Vizita u regjistrua me sukses."
            )

            return redirect("vizitat")

    return render(
        request,
        "agjencia/shto_vizite.html",
        {
            "form": form,
        }
    )


@login_required(login_url="/hyrja/")
@require_http_methods(["GET", "POST"])
def ndrysho_vizite_page(request, vizita_id):
    vizita = get_object_or_404(
        vizitat_e_perdoruesit(request.user),
        pk=vizita_id
    )

    if request.method == "POST":
        form = VizitaForm(
            request.POST,
            instance=vizita
        )
    else:
        form = VizitaForm(
            instance=vizita
        )

    form = pergatit_formen(
        form,
        request.user
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Vizita u përditësua me sukses."
            )

            return redirect("vizitat")

    return render(
        request,
        "agjencia/ndrysho_vizite.html",
        {
            "form": form,
            "vizita": vizita,
        }
    )


@login_required(login_url="/hyrja/")
@require_http_methods(["GET", "POST"])
def fshi_vizite_page(request, vizita_id):
    vizita = get_object_or_404(
        vizitat_e_perdoruesit(request.user),
        pk=vizita_id
    )

    if request.method == "POST":
        vizita.delete()

        messages.success(
            request,
            "Vizita u fshi me sukses."
        )

        return redirect("vizitat")

    return render(
        request,
        "agjencia/fshi_vizite.html",
        {
            "vizita": vizita,
        }
    )
