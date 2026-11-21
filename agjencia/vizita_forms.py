
from django import forms
from django.utils import timezone

from .models import Vizita, Klienti, Prona


class VizitaForm(forms.ModelForm):
    data_vizites = forms.DateTimeField(
        label="Data dhe ora e vizitës",
        input_formats=[
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%dT%H:%M:%S",
        ],
        widget=forms.DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={
                "type": "datetime-local",
                "class": "se-client-input",
            },
        ),
    )

    class Meta:
        model = Vizita
        fields = ["klienti", "prona", "data_vizites"]

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
            Klienti.objects.all().order_by("emri", "id")
        )

        self.fields["prona"].queryset = (
            Prona.objects.all().order_by("qyteti", "id")
        )

        self.fields["klienti"].empty_label = "Zgjidh klientin"
        self.fields["prona"].empty_label = "Zgjidh pronën"

    def clean_data_vizites(self):
        data = self.cleaned_data["data_vizites"]

        if (
            data < timezone.now()
            and (
                not self.instance.pk
                or "data_vizites" in self.changed_data
            )
        ):
            raise forms.ValidationError(
                "Data e vizitës nuk mund të jetë në të kaluarën."
            )

        return data

    def clean(self):
        cleaned_data = super().clean()

        klienti = cleaned_data.get("klienti")
        prona = cleaned_data.get("prona")
        data_vizites = cleaned_data.get("data_vizites")

        if klienti and prona and data_vizites:
            vizita_ekzistuese = Vizita.objects.filter(
                klienti=klienti,
                prona=prona,
                data_vizites=data_vizites,
            )

            if self.instance.pk:
                vizita_ekzistuese = vizita_ekzistuese.exclude(
                    pk=self.instance.pk
                )

            if vizita_ekzistuese.exists():
                raise forms.ValidationError(
                    "Ky klient ka tashmë një vizitë "
                    "për këtë pronë në këtë datë dhe orë."
                )

        return cleaned_data
