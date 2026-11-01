from rest_framework import serializers
from .models import Prona, Klienti, Kerkesa, Vizita




class PronaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prona
        fields = '__all__'
        read_only_fields = ['agjent']

    def validate_cmimi(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Cmimi duhet te jete me i madh se zero."
            )
        return value

    def validate_siperfaqja(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Siperfaqja duhet te jete me e madhe se zero."
            )
        return value



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