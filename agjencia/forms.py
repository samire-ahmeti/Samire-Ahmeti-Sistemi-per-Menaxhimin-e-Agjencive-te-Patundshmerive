
from django import forms

from .models import Prona, Perdorues


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    widget = MultipleImageInput

    def clean(self, data, initial=None):
        if not data:
            return []

        if not isinstance(data, (list, tuple)):
            data = [data]

        pastro_foton = super().clean

        return [
            pastro_foton(foto, initial)
            for foto in data
        ]


class PronaForm(forms.ModelForm):
    fotot_shtese = MultipleImageField(
        required=False,
        label="Fotografitë shtesë",
        widget=MultipleImageInput(
            attrs={
                "class": "add-property-file",
                "accept": "image/jpeg,image/png,image/webp",
            }
        ),
        help_text="Mund të zgjidhni deri në 8 fotografi shtesë.",
    )

    class Meta:
        model = Prona

        fields = [
            "lloji",
            "qyteti",
            "cmimi",
            "siperfaqja",
            "foto",
        ]

        labels = {
            "foto": "Fotografia kryesore",
        }

        widgets = {
            "lloji": forms.Select(
                attrs={
                    "class": "add-property-input",
                }
            ),
            "qyteti": forms.TextInput(
                attrs={
                    "class": "add-property-input",
                    "placeholder": "P.sh. Prizren",
                }
            ),
            "cmimi": forms.NumberInput(
                attrs={
                    "class": "add-property-input",
                    "placeholder": "P.sh. 85000",
                    "min": "0.01",
                    "step": "0.01",
                }
            ),
            "siperfaqja": forms.NumberInput(
                attrs={
                    "class": "add-property-input",
                    "placeholder": "P.sh. 120",
                    "min": "0.01",
                    "step": "0.01",
                }
            ),
            "foto": forms.ClearableFileInput(
                attrs={
                    "class": "add-property-file",
                    "accept": "image/jpeg,image/png,image/webp",
                }
            ),
        }

    def clean_qyteti(self):
        qyteti = self.cleaned_data["qyteti"].strip()

        if len(qyteti) < 2:
            raise forms.ValidationError(
                "Shkruaj emrin e saktë të qytetit."
            )

        return qyteti

    def clean_cmimi(self):
        cmimi = self.cleaned_data["cmimi"]

        if cmimi <= 0:
            raise forms.ValidationError(
                "Çmimi duhet të jetë më i madh se zero."
            )

        return cmimi

    def clean_siperfaqja(self):
        siperfaqja = self.cleaned_data["siperfaqja"]

        if siperfaqja <= 0:
            raise forms.ValidationError(
                "Sipërfaqja duhet të jetë më e madhe se zero."
            )

        return siperfaqja

    def clean_foto(self):
        foto = self.cleaned_data.get("foto")

        if foto and foto.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "Fotografia nuk duhet të jetë më e madhe se 5 MB."
            )

        return foto

    def clean_fotot_shtese(self):
        fotot = self.cleaned_data.get("fotot_shtese") or []

        for foto in fotot:
            if foto.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "Secila fotografi duhet të jetë maksimumi 5 MB."
                )

        ids_per_largim = (
            self.data.getlist("hiq_fotot")
            if self.is_bound
            else []
        )

        try:
            ids = {int(vlera) for vlera in ids_per_largim}
        except (ValueError, TypeError):
            raise forms.ValidationError(
                "Përzgjedhja e fotografive për largim është e pavlefshme."
            )

        if len(ids) != len(ids_per_largim):
            raise forms.ValidationError(
                "Përzgjedhja e fotografive për largim është e pavlefshme."
            )

        numri_ekzistues = 0
        numri_per_largim = 0

        if self.instance.pk:
            numri_ekzistues = self.instance.fotot.count()

            numri_per_largim = self.instance.fotot.filter(
                pk__in=ids
            ).count()

        if numri_per_largim != len(ids):
            raise forms.ValidationError(
                "Një ose më shumë fotografi nuk i përkasin kësaj prone."
            )

        numri_perfundimtar = (
            numri_ekzistues
            - numri_per_largim
            + len(fotot)
        )

        if numri_perfundimtar > 8:
            raise forms.ValidationError(
                "Prona mund të ketë maksimumi 8 fotografi shtesë. "
                "Largo disa fotografi ekzistuese ose zgjidh më pak të reja."
            )

        return fotot


class PronaAdministratoriForm(PronaForm):
    class Meta(PronaForm.Meta):
        fields = [
            "lloji",
            "qyteti",
            "cmimi",
            "siperfaqja",
            "foto",
            "agjent",
        ]

        labels = {
            **PronaForm.Meta.labels,
            "agjent": "Përgjegjësi i pronës",
        }

        widgets = {
            **PronaForm.Meta.widgets,
            "agjent": forms.Select(
                attrs={
                    "class": "add-property-input",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["agjent"].queryset = (
            Perdorues.objects.filter(
                is_active=True,
                roli__in=["administrator", "agjent"]
            ).order_by("username")
        )

        self.fields["agjent"].empty_label = (
            "Zgjidh përgjegjësin e pronës"
        )
