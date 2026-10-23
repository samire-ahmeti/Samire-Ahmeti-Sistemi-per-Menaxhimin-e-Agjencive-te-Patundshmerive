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
