
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Perdorues


class RegjistrimiAgjentForm(UserCreationForm):
    emri = forms.CharField(
        max_length=100,
        label="Emri dhe mbiemri"
    )

    email = forms.EmailField(
        required=True,
        label="Email-i"
    )

    class Meta:
        model = Perdorues

        fields = [
            "username",
            "emri",
            "email",
            "password1",
            "password2",
        ]

        labels = {
            "username": "Emri i përdoruesit",
            "emri": "Emri dhe mbiemri",
            "email": "Email-i",
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if Perdorues.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "Ky email është regjistruar më parë."
            )

        return email

    def save(self, commit=True):
        perdoruesi = super().save(commit=False)

        perdoruesi.roli = "agjent"
        perdoruesi.is_active = False
        perdoruesi.is_staff = False
        perdoruesi.is_superuser = False

        if commit:
            perdoruesi.save()

        return perdoruesi


class KrijoAdministratorForm(RegjistrimiAgjentForm):

    def save(self, commit=True):
        perdoruesi = super().save(commit=False)

        perdoruesi.roli = "administrator"
        perdoruesi.is_active = True
        perdoruesi.is_staff = False
        perdoruesi.is_superuser = False

        if commit:
            perdoruesi.save()

        return perdoruesi
