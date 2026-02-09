import django_filters
from api.models import VaccineSchedule

class AgeVaccineFilter(django_filters.FilterSet):
    class Meta:
        model = VaccineSchedule
        fields = ['id',]