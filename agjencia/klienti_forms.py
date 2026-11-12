
import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import Klienti


class KlientiForm(forms.ModelForm):
    class Meta:
        model = Klienti
        fields = ["emri", "kontakti"]

        widgets = {
            "emri": forms.TextInput(
                attrs={
                    "class": "se-client-input",
                    "placeholder": "Emri dhe mbiemri",
                    "autocomplete": "name",
                }
            ),
            "kontakti": forms.TextInput(
                attrs={
                    "class": "se-client-input",
                    "placeholder": "Numri i telefonit ose email",
                }
            ),
        }

    def clean_emri(self):
        emri = self.cleaned_data["emri"].strip()

        if len(emri) < 2:
            raise forms.ValidationError(
                "Emri duhet të ketë të paktën 2 karaktere."
            )

        return emri

    def clean_kontakti(self):
        kontakti = self.cleaned_data["kontakti"].strip()

        if "@" in kontakti:
            try:
                validate_email(kontakti)
            except ValidationError:
                raise forms.ValidationError(
                    "Shkruani një adresë email të vlefshme."
                )

            return kontakti

        if not re.fullmatch(r"[0-9+().\s-]+", kontakti):
            raise forms.ValidationError(
                "Shkruani një numër telefoni ose email të vlefshëm."
            )

        numri = re.sub(r"\D", "", kontakti)

        if not 6 <= len(numri) <= 15:
            raise forms.ValidationError(
                "Numri i telefonit duhet të ketë nga 6 deri në 15 shifra."
            )

        return kontakti
