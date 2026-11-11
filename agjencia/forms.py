
from django import forms
from .models import Prona


class PronaForm(forms.ModelForm):
    class Meta:
        model = Prona
        fields = [
            "lloji",
            "qyteti",
            "cmimi",
            "siperfaqja",
            "foto",
        ]

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

        if foto:
            if foto.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "Fotografia nuk duhet të jetë më e madhe se 5 MB."
                )

        return foto
