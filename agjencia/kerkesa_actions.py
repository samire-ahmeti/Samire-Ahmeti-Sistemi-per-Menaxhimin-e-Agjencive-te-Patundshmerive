
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .kerkesa_forms import KerkesaForm
from .models import Kerkesa, Prona


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


def kerkesat_e_perdoruesit(perdoruesi):
    kontrollo_rolin(perdoruesi)

    if eshte_administrator(perdoruesi):
        return Kerkesa.objects.all()

    return Kerkesa.objects.filter(
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
def kerkesat_page(request):
    kerkimi = request.GET.get("q", "").strip()[:100]

    kerkesat = kerkesat_e_perdoruesit(
        request.user
    ).select_related(
        "klienti",
        "prona",
        "prona__agjent"
    )

    if kerkimi:
        kerkesat = kerkesat.filter(
            Q(klienti__emri__icontains=kerkimi)
            | Q(klienti__kontakti__icontains=kerkimi)
            | Q(prona__qyteti__icontains=kerkimi)
        )

    kerkesat = kerkesat.order_by("-id")

    return render(
        request,
        "agjencia/kerkesat.html",
        {
            "kerkesat": kerkesat,
            "kerkimi": kerkimi,
            "numri_kerkesave": kerkesat.count(),
        }
    )


@login_required(login_url="/hyrja/")
@require_http_methods(["GET", "POST"])
def shto_kerkese_page(request):
    kontrollo_rolin(request.user)

    if request.method == "POST":
        form = KerkesaForm(request.POST)
    else:
        form = KerkesaForm()

    form = pergatit_formen(
        form,
        request.user
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Kërkesa u regjistrua me sukses."
            )

            return redirect("kerkesat")

    return render(
        request,
        "agjencia/shto_kerkese.html",
        {
            "form": form,
        }
    )


@login_required(login_url="/hyrja/")
@require_http_methods(["GET", "POST"])
def ndrysho_kerkese_page(request, kerkesa_id):
    kerkesa = get_object_or_404(
        kerkesat_e_perdoruesit(request.user),
        pk=kerkesa_id
    )

    if request.method == "POST":
        form = KerkesaForm(
            request.POST,
            instance=kerkesa
        )
    else:
        form = KerkesaForm(
            instance=kerkesa
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
                "Kërkesa u përditësua me sukses."
            )

            return redirect("kerkesat")

    return render(
        request,
        "agjencia/ndrysho_kerkese.html",
        {
            "form": form,
            "kerkesa": kerkesa,
        }
    )


@login_required(login_url="/hyrja/")
@require_http_methods(["GET", "POST"])
def fshi_kerkese_page(request, kerkesa_id):
    kerkesa = get_object_or_404(
        kerkesat_e_perdoruesit(request.user),
        pk=kerkesa_id
    )

    if request.method == "POST":
        kerkesa.delete()

        messages.success(
            request,
            "Kërkesa u fshi me sukses."
        )

        return redirect("kerkesat")

    return render(
        request,
        "agjencia/fshi_kerkese.html",
        {
            "kerkesa": kerkesa,
        }
    )
