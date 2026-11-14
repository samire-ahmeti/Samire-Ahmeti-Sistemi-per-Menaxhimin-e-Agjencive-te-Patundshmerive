
from django import forms

from .models import Kerkesa, Klienti, Prona


class KerkesaForm(forms.ModelForm):
    class Meta:
        model = Kerkesa
        fields = ["klienti", "prona"]

        labels = {
            "klienti": "Zgjidh klientin",
            "prona": "Zgjidh pronën",
        }

        widgets = {
            "klienti": forms.Select(
                attrs={"class": "se-client-input"}
            ),
            "prona": forms.Select(
                attrs={"class": "se-client-input"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["klienti"].queryset = (
            Klienti.objects.all().order_by("emri")
        )

        self.fields["prona"].queryset = (
            Prona.objects.all().order_by("qyteti", "id")
        )

        self.fields["klienti"].empty_label = "Zgjidh klientin"
        self.fields["prona"].empty_label = "Zgjidh pronën"

    def clean(self):
        cleaned_data = super().clean()

        klienti = cleaned_data.get("klienti")
        prona = cleaned_data.get("prona")

        if klienti and prona:
            kerkesa_ekzistuese = Kerkesa.objects.filter(
                klienti=klienti,
                prona=prona
            )

            if self.instance.pk:
                kerkesa_ekzistuese = kerkesa_ekzistuese.exclude(
                    pk=self.instance.pk
                )

            if kerkesa_ekzistuese.exists():
                raise forms.ValidationError(
                    "Ky klient ka tashmë një kërkesë për këtë pronë."
                )

        return cleaned_data
