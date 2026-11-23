
from django import forms


class InteresimiForm(forms.Form):
    emri = forms.CharField(
        label="Emri dhe mbiemri",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "se-interest-input",
                "placeholder": "Shkruaj emrin dhe mbiemrin",
                "autocomplete": "name",
            }
        )
    )

    telefoni = forms.CharField(
        label="Numri i telefonit",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "se-interest-input",
                "placeholder": "P.sh. +383 49 123 456",
                "autocomplete": "tel",
            }
        )
    )

    email = forms.EmailField(
        label="Emaili",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "se-interest-input",
                "placeholder": "shembull@gmail.com",
                "autocomplete": "email",
            }
        )
    )

    mesazhi = forms.CharField(
        label="Mesazhi",
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                "class": "se-interest-textarea",
                "placeholder": "Përshkruaj interesimin tënd për këtë pronë...",
                "rows": 4,
            }
        )
    )

    def clean_emri(self):
        emri = self.cleaned_data["emri"].strip()

        if len(emri) < 2:
            raise forms.ValidationError(
                "Shkruaj emrin e plotë."
            )

        return emri

    def clean_telefoni(self):
        telefoni = self.cleaned_data["telefoni"].strip()

        karakteret_e_lejuara = set(
            "0123456789+ -()."
        )

        if any(
            karakter not in karakteret_e_lejuara
            for karakter in telefoni
        ):
            raise forms.ValidationError(
                "Numri i telefonit përmban karaktere të pavlefshme."
            )

        numrat = [
            karakter
            for karakter in telefoni
            if karakter.isdigit()
        ]

        if not 7 <= len(numrat) <= 15:
            raise forms.ValidationError(
                "Shkruaj një numër telefoni të vlefshëm."
            )

        return telefoni

    def clean_mesazhi(self):
        mesazhi = self.cleaned_data["mesazhi"].strip()

        if len(mesazhi) < 5:
            raise forms.ValidationError(
                "Mesazhi duhet të ketë të paktën 5 karaktere."
            )

        return mesazhi
