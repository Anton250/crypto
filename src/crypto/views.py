from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from src.crypto.serializers import AlgorythmSerializer, AlphabetSerializer, ActionSerializer
from src.crypto.models import Algorythm, Alphabet

from src.algorythms import algos


class AlphabetViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AlphabetSerializer
    queryset = Alphabet.objects.all()


class AlgorythmViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = AlgorythmSerializer
    queryset = Algorythm.objects.all()

    @action(detail=False, methods=['post'])
    def action(self, request):
        data = ActionSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data = data.validated_data
        if data.get('alphabet'):
            alphabet = Alphabet.objects.get(id=data['alphabet']).value
        else:
            alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        algorythm = getattr(algos, Algorythm.objects.get(id=data['algorythm']).class_name)(keys=data['keys'], alph=alphabet)
        if (data['action'] == ActionSerializer.ENCRYPT):
            result = algorythm.encrypt(data['text'])
        else:
            result = algorythm.decrypt(data['text'])

        response = {}
        if isinstance(result, str):
            response = {'result': result}
        else:
            response = {
                'result': result['result'],
                'info': result['info'],
            }

        return Response(response)
