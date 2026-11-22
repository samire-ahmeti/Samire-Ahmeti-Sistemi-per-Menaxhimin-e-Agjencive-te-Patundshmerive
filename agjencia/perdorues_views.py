
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Perdorues
from .perdorues_forms import (
    RegjistrimiAgjentForm,
    KrijoAdministratorForm,
)


def eshte_administrator(perdoruesi):
    return (
        perdoruesi.is_authenticated
        and perdoruesi.is_active
        and (
            perdoruesi.is_superuser
            or perdoruesi.roli == "administrator"
        )
    )


def regjistro_agjent(request):
    eshte_ajax = (
        request.headers.get("X-Requested-With")
        == "XMLHttpRequest"
    )

    if request.user.is_authenticated:
        if eshte_ajax:
            return JsonResponse(
                {
                    "ok": False,
                    "message": "Tashmë je i kyçur në sistem."
                },
                status=403
            )

        return redirect("paneli")

    if request.method != "POST":
        return redirect("hyrja")

    form = RegjistrimiAgjentForm(request.POST)

    if form.is_valid():
        form.save()

        mesazhi = (
            "Llogaria u krijua me sukses! "
            "Prit miratimin nga administratori "
            "përpara se të hysh në sistem."
        )

        if eshte_ajax:
            return JsonResponse({
                "ok": True,
                "message": mesazhi
            })

        messages.success(request, mesazhi)
        return redirect("hyrja")

    if eshte_ajax:
        gabimet = {
            fusha: list(mesazhet)
            for fusha, mesazhet in form.errors.items()
        }

        return JsonResponse(
            {
                "ok": False,
                "message": "Kontrollo të dhënat e formularit.",
                "errors": gabimet
            },
            status=400
        )

    messages.error(
        request,
        "Regjistrimi nuk u përfundua. "
        "Hape formularin e regjistrimit dhe provo përsëri."
    )

    return redirect("hyrja")


@login_required
def menaxho_perdoruesit(request):
    if not eshte_administrator(request.user):
        raise PermissionDenied

    agjentet_ne_pritje = Perdorues.objects.filter(
        roli="agjent",
        is_active=False
    ).order_by("id")

    perdoruesit_aktiv = Perdorues.objects.filter(
        is_active=True
    ).order_by("username")

    return render(
        request,
        "agjencia/menaxho_perdoruesit.html",
        {
            "agjentet_ne_pritje": agjentet_ne_pritje,
            "perdoruesit_aktiv": perdoruesit_aktiv,
        }
    )


@login_required
@require_POST
def mirato_agjentin(request, perdorues_id):
    if not eshte_administrator(request.user):
        raise PermissionDenied

    with transaction.atomic():
        agjenti = get_object_or_404(
            Perdorues.objects.select_for_update(),
            id=perdorues_id,
            roli="agjent",
            is_active=False
        )

        agjenti.is_active = True
        agjenti.is_staff = False
        agjenti.is_superuser = False

        agjenti.save(
            update_fields=[
                "is_active",
                "is_staff",
                "is_superuser",
            ]
        )

    messages.success(
        request,
        "Agjenti u miratua me sukses."
    )

    return redirect("menaxho_perdoruesit")


@login_required
@require_POST
def refuzo_agjentin(request, perdorues_id):
    if not eshte_administrator(request.user):
        raise PermissionDenied

    agjenti = get_object_or_404(
        Perdorues,
        id=perdorues_id,
        roli="agjent",
        is_active=False
    )

    try:
        agjenti.delete()

        messages.success(
            request,
            "Kërkesa për regjistrim u refuzua."
        )

    except ProtectedError:
        messages.error(
            request,
            "Ky përdorues ka të dhëna të lidhura "
            "dhe nuk mund të fshihet."
        )

    return redirect("menaxho_perdoruesit")


@login_required
def krijo_administrator(request):
    if not eshte_administrator(request.user):
        raise PermissionDenied

    if request.method == "POST":
        form = KrijoAdministratorForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Administratori i ri u krijua me sukses."
            )

            return redirect("menaxho_perdoruesit")
    else:
        form = KrijoAdministratorForm()

    return render(
        request,
        "agjencia/krijo_administrator.html",
        {"form": form}
    )
