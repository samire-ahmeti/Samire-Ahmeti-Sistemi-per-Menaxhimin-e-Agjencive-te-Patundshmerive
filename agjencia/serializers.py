from rest_framework import serializers
from .models import Prona, Klienti, Kerkesa, Vizita


class PronaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prona
        fields = '__all__'


class KlientiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klienti
        fields = '__all__'


class KerkesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kerkesa
        fields = '__all__'


class VizitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vizita
        fields = '__all__'