
from django.contrib import admin

from .models import (
    Perdorues,
    Prona,
    Klienti,
    Kerkesa,
    Vizita,
    FotoProne,
    MesazhKontakti,
)


admin.site.register(Perdorues)
admin.site.register(Klienti)
admin.site.register(Kerkesa)
admin.site.register(Vizita)


class FotoProneInline(admin.TabularInline):
    model = FotoProne
    extra = 1


@admin.register(Prona)
class PronaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "lloji",
        "qyteti",
        "cmimi",
        "siperfaqja",
        "agjent",
    )
    list_filter = ("lloji", "qyteti")
    search_fields = ("qyteti", "lloji")
    inlines = [FotoProneInline]


@admin.register(MesazhKontakti)
class MesazhKontaktiAdmin(admin.ModelAdmin):
    list_display = (
        "emri",
        "email",
        "subjekti",
        "data_dergimit",
        "lexuar",
    )
    list_filter = ("lexuar", "data_dergimit")
    search_fields = ("emri", "email", "subjekti")
    readonly_fields = ("data_dergimit",)
    ordering = ("-data_dergimit",)
