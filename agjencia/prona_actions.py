
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Max
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import PronaForm, PronaAdministratoriForm
from .models import Prona, FotoProne


def eshte_administrator(perdoruesi):
    return (
        perdoruesi.is_authenticated
        and (
            perdoruesi.is_superuser
            or perdoruesi.roli == "administrator"
        )
    )


def gjej_pronen_per_menaxhim(perdoruesi, prona_id):
    if eshte_administrator(perdoruesi):
        pronat = Prona.objects.all()

    elif perdoruesi.roli == "agjent":
        pronat = Prona.objects.filter(
            agjent=perdoruesi
        )

    else:
        raise PermissionDenied

    return get_object_or_404(
        pronat,
        pk=prona_id
    )


@login_required(login_url="/hyrja/")
@require_http_methods(["GET", "POST"])
def ndrysho_prone_page(request, prona_id):
    prona = gjej_pronen_per_menaxhim(
        request.user,
        prona_id
    )

    administratori = eshte_administrator(
        request.user
    )

    if administratori:
        formulari = PronaAdministratoriForm
    else:
        formulari = PronaForm

    if request.method == "POST":
        form = formulari(
            request.POST,
            request.FILES,
            instance=prona
        )

        if form.is_valid():
            fotot_e_reja = form.cleaned_data.get(
                "fotot_shtese",
                []
            )

            ids_per_largim = [
                int(foto_id)
                for foto_id in request.POST.getlist(
                    "hiq_fotot"
                )
            ]

            with transaction.atomic():
                prona_e_perditesuar = form.save(
                    commit=False
                )

                if not administratori:
                    prona_e_perditesuar.agjent = request.user

                prona_e_perditesuar.save()
                form.save_m2m()

                fotografite_per_largim = list(
                    prona.fotot.filter(
                        id__in=ids_per_largim
                    )
                )

                for fotografia in fotografite_per_largim:
                    emri_skedarit = fotografia.foto.name
                    ruajtja = fotografia.foto.storage

                    fotografia.delete()

                    if emri_skedarit:
                        transaction.on_commit(
                            lambda storage=ruajtja, name=emri_skedarit:
                            storage.delete(name),
                            robust=True
                        )

                renditja_e_fundit = (
                    prona.fotot.aggregate(
                        maksimumi=Max("renditja")
                    )["maksimumi"] or 0
                )

                for foto in fotot_e_reja:
                    renditja_e_fundit += 1

                    FotoProne.objects.create(
                        prona=prona,
                        foto=foto,
                        renditja=renditja_e_fundit
                    )

            messages.success(
                request,
                "Prona dhe fotografitë u përditësuan me sukses."
            )

            return redirect(
                "detajet_prones",
                prona_id=prona.id
            )

    else:
        form = formulari(
            instance=prona
        )

    return render(
        request,
        "agjencia/ndrysho_prone.html",
        {
            "form": form,
            "prona": prona,
            "administratori": administratori,
        }
    )


@login_required(login_url="/hyrja/")
@require_http_methods(["GET", "POST"])
def fshi_prone_page(request, prona_id):
    prona = gjej_pronen_per_menaxhim(
        request.user,
        prona_id
    )

    if request.method == "POST":
        try:
            prona.delete()

            messages.success(
                request,
                "Prona u fshi me sukses."
            )

            return redirect("paneli")

        except ProtectedError:
            messages.error(
                request,
                "Kjo pronë nuk mund të fshihet sepse "
                "ka kërkesa ose vizita të lidhura me të."
            )

            return redirect(
                "fshi_prone",
                prona_id=prona.id
            )

    return render(
        request,
        "agjencia/fshi_prone.html",
        {
            "prona": prona
        }
    )
