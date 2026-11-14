
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from agjencia.views import (
    pronat_page,
    detajet_prones,
    paneli_page,
    hyrja_page,
    dalja_page,
    shto_prone_page,
)

from agjencia.contact_views import kontakt_page

from agjencia.prona_actions import (
    ndrysho_prone_page,
    fshi_prone_page,
)

from agjencia.klienti_actions import (
    klientet_page,
    shto_klient_page,
    ndrysho_klient_page,
    fshi_klient_page,
)

from agjencia.kerkesa_actions import (
    kerkesat_page,
    shto_kerkese_page,
    ndrysho_kerkese_page,
    fshi_kerkese_page,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("agjencia.urls")),

    path(
        "",
        TemplateView.as_view(
            template_name="agjencia/home.html"
        ),
        name="home",
    ),

    path("pronat/", pronat_page, name="pronat"),

    path(
        "pronat/<int:prona_id>/",
        detajet_prones,
        name="detajet_prones",
    ),

    path(
        "rreth-nesh/",
        TemplateView.as_view(
            template_name="agjencia/rreth_nesh.html"
        ),
        name="rreth_nesh",
    ),

    path(
        "sherbimet/",
        TemplateView.as_view(
            template_name="agjencia/sherbimet.html"
        ),
        name="sherbimet",
    ),

    path("kontakt/", kontakt_page, name="kontakt"),

    path("paneli/", paneli_page, name="paneli"),
    path("hyrja/", hyrja_page, name="hyrja"),
    path("dalja/", dalja_page, name="dalja"),

    path(
        "shto-prone/",
        shto_prone_page,
        name="shto_prone",
    ),

    path(
        "ndrysho-prone/<int:prona_id>/",
        ndrysho_prone_page,
        name="ndrysho_prone",
    ),

    path(
        "fshi-prone/<int:prona_id>/",
        fshi_prone_page,
        name="fshi_prone",
    ),

    path(
        "klientet/",
        klientet_page,
        name="klientet",
    ),

    path(
        "shto-klient/",
        shto_klient_page,
        name="shto_klient",
    ),

    path(
        "ndrysho-klient/<int:klienti_id>/",
        ndrysho_klient_page,
        name="ndrysho_klient",
    ),

    path(
        "fshi-klient/<int:klienti_id>/",
        fshi_klient_page,
        name="fshi_klient",
    ),

    path(
        "kerkesat/",
        kerkesat_page,
        name="kerkesat",
    ),

    path(
        "shto-kerkese/",
        shto_kerkese_page,
        name="shto_kerkese",
    ),

    path(
        "ndrysho-kerkese/<int:kerkesa_id>/",
        ndrysho_kerkese_page,
        name="ndrysho_kerkese",
    ),

    path(
        "fshi-kerkese/<int:kerkesa_id>/",
        fshi_kerkese_page,
        name="fshi_kerkese",
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
