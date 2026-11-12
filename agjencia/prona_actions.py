
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import PronaForm
from .views import pronat_e_perdoruesit


@login_required(login_url="/hyrja/")
@require_http_methods(["GET", "POST"])
def ndrysho_prone_page(request, prona_id):
    prona = get_object_or_404(
        pronat_e_perdoruesit(request.user),
        pk=prona_id
    )

    if request.method == "POST":
        form = PronaForm(
            request.POST,
            request.FILES,
            instance=prona
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Prona u përditësua me sukses."
            )

            return redirect(
                "detajet_prones",
                prona_id=prona.id
            )
    else:
        form = PronaForm(instance=prona)

    return render(
        request,
        "agjencia/ndrysho_prone.html",
        {
            "form": form,
            "prona": prona
        }
    )


@login_required(login_url="/hyrja/")
@require_http_methods(["GET", "POST"])
def fshi_prone_page(request, prona_id):
    prona = get_object_or_404(
        pronat_e_perdoruesit(request.user),
        pk=prona_id
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

            return redirect("fshi_prone", prona_id=prona.id)

    return render(
        request,
        "agjencia/fshi_prone.html",
        {"prona": prona}
    )
