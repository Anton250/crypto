from rest_framework import serializers
from src.crypto.models import Algorythm, Alphabet


class AlgorythmSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    def get_options(self, instance):
        return instance.options

    class Meta:
        model = Algorythm
        fields = '__all__'


class AlphabetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alphabet
        fields = '__all__'


class ActionSerializer(serializers.Serializer):
    ENCRYPT = 'E'
    DECRYPT = 'D'

    ACTIONS = (
        (ENCRYPT, 'Зашифровать'),
        (DECRYPT, 'Расшифровать'),
    )

    action = serializers.ChoiceField(choices=ACTIONS)
    keys = serializers.JSONField(required=False)
    text = serializers.CharField()
    alphabet = serializers.IntegerField()
    algorythm = serializers.IntegerField()
