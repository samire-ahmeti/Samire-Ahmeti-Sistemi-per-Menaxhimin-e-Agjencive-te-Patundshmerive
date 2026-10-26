from django.db import models
from django.contrib.auth.models import AbstractUser


class Perdorues(AbstractUser):
    ROLET = [
        ('administrator', 'Administrator'),
        ('agjent', 'Agjent'),
    ]

    emri = models.CharField(max_length=100)
    roli = models.CharField(
        max_length=20,
        choices=ROLET,
        default='agjent'
    )

    def __str__(self):
        return self.username


class Prona(models.Model):
    LLOJET = [
        ('banese', 'Banesë'),
        ('shtepi', 'Shtëpi'),
        ('lokal', 'Lokal'),
        ('toke', 'Tokë'),
    ]

    agjent = models.ForeignKey(
        Perdorues,
        on_delete=models.PROTECT,
        related_name='pronat'
    )
    lloji = models.CharField(max_length=20, choices=LLOJET)
    qyteti = models.CharField(max_length=100)
    cmimi = models.DecimalField(max_digits=12, decimal_places=2)
    siperfaqja = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.get_lloji_display()} - {self.qyteti}'



class Klienti(models.Model):
    emri = models.CharField(max_length=100)
    kontakti = models.CharField(max_length=100)

    def __str__(self):
        return self.emri




class Kerkesa(models.Model):
    prona = models.ForeignKey(
        Prona,
        on_delete=models.PROTECT,
        related_name='kerkesat'
    )
    klienti = models.ForeignKey(
        Klienti,
        on_delete=models.PROTECT,
        related_name='kerkesat'
    )

    def __str__(self):
        return f'Kerkesa e {self.klienti.emri} per {self.prona}'



class Vizita(models.Model):
    prona = models.ForeignKey(
        Prona,
        on_delete=models.PROTECT,
        related_name='vizitat'
    )
    klienti = models.ForeignKey(
        Klienti,
        on_delete=models.PROTECT,
        related_name='vizitat'
    )
    data_vizites = models.DateTimeField()

    def __str__(self):
        return f'Vizita e {self.klienti.emri} - {self.prona}'
