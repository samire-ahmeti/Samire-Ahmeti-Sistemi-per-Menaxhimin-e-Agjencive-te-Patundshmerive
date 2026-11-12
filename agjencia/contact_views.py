
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .contact_forms import MesazhKontaktiForm


@require_http_methods(["GET", "POST"])
def kontakt_page(request):
    if request.method == "POST":
        form = MesazhKontaktiForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Mesazhi juaj u dërgua me sukses. Faleminderit!"
            )

            return redirect("kontakt")
    else:
        form = MesazhKontaktiForm()

    return render(
        request,
        "agjencia/kontakt.html",
        {"form": form}
    )
