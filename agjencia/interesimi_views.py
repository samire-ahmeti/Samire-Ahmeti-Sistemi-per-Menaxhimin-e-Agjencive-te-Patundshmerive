
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .interesimi_forms import InteresimiForm
from .models import Prona, Klienti, Kerkesa


@require_POST
def dergo_interesimin(request, prona_id):
    prona = get_object_or_404(
        Prona,
        pk=prona_id
    )

    form = InteresimiForm(request.POST)

    if form.is_valid():
        with transaction.atomic():
            klienti = Klienti.objects.create(
                emri=form.cleaned_data["emri"],
                kontakti=form.cleaned_data["telefoni"]
            )

            Kerkesa.objects.create(
                prona=prona,
                klienti=klienti,
                email=form.cleaned_data["email"],
                mesazhi=form.cleaned_data["mesazhi"]
            )

        messages.success(
            request,
            "Interesimi juaj u dërgua me sukses. "
            "Agjencia do t'ju kontaktojë."
        )

        return redirect(
            "detajet_prones",
            prona_id=prona.id
        )

    return render(
        request,
        "agjencia/detajet_prones.html",
        {
            "prona": prona,
            "interesimi_form": form,
            "hap_interesimin": True,
        }
    )
