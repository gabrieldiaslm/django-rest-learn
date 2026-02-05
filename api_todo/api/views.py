from rest_framework import viewsets, filters
from api.models import VaccineSchedule, Immunobiological
from api.serializers import VaccineScheduleSerializer, ImmunobiologicalSerializer

# Calendário de vacinas
class VaccineScheduleViewSet(viewsets.ModelViewSet):
    queryset = VaccineSchedule.objects.all()
    serializer_class = VaccineScheduleSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'vaccine_id', 'age_group', 'diseases_prevented']
    ordering_fields = ['min_age_in_days', 'created', 'id']

# VACINAS
class ImmunobiologicalViewSet(viewsets.ModelViewSet):
    queryset = Immunobiological.objects.all()
    serializer_class = ImmunobiologicalSerializer
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'manufacturer', 'batch_number']
    ordering_fields = ['expiration_date', 'created', 'name']