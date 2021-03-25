from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from src.crypto.serializers import AlgorythmSerializer, AlphabetSerializer, ActionSerializer
from src.crypto.models import Algorythm, Alphabet

from src.utils import do_action
from django.http.response import HttpResponse
import io


class AlphabetViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AlphabetSerializer
    queryset = Alphabet.objects.all()


class AlgorythmViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = AlgorythmSerializer
    queryset = Algorythm.objects.all().order_by('name')

    @action(detail=False, methods=['post'])
    def action(self, request):
        data = ActionSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data = data.validated_data
        if data.get('f'):
            data['text'] = data['f'].file.read().decode('utf-8')
        result = do_action(data)

        if data['return_file']:
            f = io.StringIO(result['result'])
            response = HttpResponse(f.getvalue(), content_type='application/txt')
            response['Content-Disposition'] = 'attachment; filename="%s"' % 'result.txt'
        else:
            response = Response(result)
        return response
