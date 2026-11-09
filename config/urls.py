
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from agjencia.views import pronat_page, detajet_prones
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('agjencia.urls')),
    path('', TemplateView.as_view(template_name='agjencia/home.html'), name='home'),
    path("pronat/", pronat_page, name="pronat"),
    path("pronat/<int:prona_id>/", detajet_prones, name="detajet_prones"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
