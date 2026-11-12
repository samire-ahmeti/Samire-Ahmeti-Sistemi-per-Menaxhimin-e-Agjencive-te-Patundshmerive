
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


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("agjencia.urls")),

    path(
        "",
        TemplateView.as_view(template_name="agjencia/home.html"),
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
        TemplateView.as_view(template_name="agjencia/rreth_nesh.html"),
        name="rreth_nesh",
    ),

    path(
        "sherbimet/",
        TemplateView.as_view(template_name="agjencia/sherbimet.html"),
        name="sherbimet",
    ),

    path("kontakt/", kontakt_page, name="kontakt"),
    path("paneli/", paneli_page, name="paneli"),
    path("hyrja/", hyrja_page, name="hyrja"),
    path("dalja/", dalja_page, name="dalja"),
    path("shto-prone/", shto_prone_page, name="shto_prone"),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
