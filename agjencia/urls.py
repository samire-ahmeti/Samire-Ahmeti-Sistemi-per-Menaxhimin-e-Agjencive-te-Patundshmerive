from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PronaViewSet,
    KlientiViewSet,
    KerkesaViewSet,
    VizitaViewSet,
)

router = DefaultRouter()

router.register(r'pronat', PronaViewSet)
router.register(r'klientet', KlientiViewSet)
router.register(r'kerkesat', KerkesaViewSet)
router.register(r'vizitat', VizitaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]