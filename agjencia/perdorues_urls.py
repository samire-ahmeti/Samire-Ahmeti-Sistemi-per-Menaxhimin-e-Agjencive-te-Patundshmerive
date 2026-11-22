
from django.urls import path

from .perdorues_views import (
    regjistro_agjent,
    menaxho_perdoruesit,
    mirato_agjentin,
    refuzo_agjentin,
    krijo_administrator,
)


urlpatterns = [
    path(
        "regjistrohu/",
        regjistro_agjent,
        name="regjistro_agjent"
    ),

    path(
        "perdoruesit/",
        menaxho_perdoruesit,
        name="menaxho_perdoruesit"
    ),

    path(
        "perdoruesit/mirato/<int:perdorues_id>/",
        mirato_agjentin,
        name="mirato_agjentin"
    ),

    path(
        "perdoruesit/refuzo/<int:perdorues_id>/",
        refuzo_agjentin,
        name="refuzo_agjentin"
    ),

    path(
        "perdoruesit/krijo-administrator/",
        krijo_administrator,
        name="krijo_administrator"
    ),
]
