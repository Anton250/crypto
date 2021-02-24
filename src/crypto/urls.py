from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include

from src.crypto.views import AlgorythmViewSet, AlphabetViewSet

router = DefaultRouter()
router.register(r'alphabet', AlphabetViewSet, basename='Alphabet')
router.register(r'algorythm', AlgorythmViewSet, basename='Algorythm')

urlpatterns = [
    url(r'^', include(router.urls)),
]

