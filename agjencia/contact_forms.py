
from django import forms

from .models import MesazhKontakti


class MesazhKontaktiForm(forms.ModelForm):
    class Meta:
        model = MesazhKontakti
        fields = ["emri", "email", "subjekti", "mesazhi"]

        widgets = {
            "emri": forms.TextInput(attrs={
                "placeholder": "Emri dhe mbiemri",
                "autocomplete": "name"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "adresa@email.com",
                "autocomplete": "email"
            }),
            "subjekti": forms.TextInput(attrs={
                "placeholder": "Për çfarë dëshironi të na shkruani?"
            }),
            "mesazhi": forms.Textarea(attrs={
                "placeholder": "Shkruani mesazhin tuaj...",
                "rows": 5
            }),
        }

    def clean_emri(self):
        emri = self.cleaned_data["emri"].strip()

        if len(emri) < 2:
            raise forms.ValidationError(
                "Shkruani emrin tuaj të plotë."
            )

        return emri

    def clean_subjekti(self):
        subjekti = self.cleaned_data["subjekti"].strip()

        if len(subjekti) < 3:
            raise forms.ValidationError(
                "Subjekti duhet të ketë të paktën 3 karaktere."
            )

        return subjekti

    def clean_mesazhi(self):
        mesazhi = self.cleaned_data["mesazhi"].strip()

        if len(mesazhi) < 10:
            raise forms.ValidationError(
                "Mesazhi duhet të ketë të paktën 10 karaktere."
            )

        return mesazhi
