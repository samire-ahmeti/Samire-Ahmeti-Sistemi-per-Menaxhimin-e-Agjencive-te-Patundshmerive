
from django.contrib import admin
from .models import Perdorues, Prona, Klienti, Kerkesa, Vizita, FotoProne

admin.site.register(Perdorues)
admin.site.register(Prona)
admin.site.register(Klienti)
admin.site.register(Kerkesa)
admin.site.register(Vizita)


class FotoProneInline(admin.TabularInline):
    model = FotoProne
    extra = 1


admin.site.unregister(Prona)


@admin.register(Prona)
class PronaAdmin(admin.ModelAdmin):
    list_display = ("id", "lloji", "qyteti", "cmimi", "siperfaqja", "agjent")
    list_filter = ("lloji", "qyteti")
    search_fields = ("qyteti", "lloji")
    inlines = [FotoProneInline]