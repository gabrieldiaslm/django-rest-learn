from django.urls import path, include
from api.views import VaccineScheduleViewSet, ImmunobiologicalViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'schedules', VaccineScheduleViewSet, basename='schedule')
router.register(r'stock', ImmunobiologicalViewSet, basename='immunobiological')

urlpatterns = [
    # Isso inclui todas as rotas geradas acima na raiz da API
    path('', include(router.urls)),
]