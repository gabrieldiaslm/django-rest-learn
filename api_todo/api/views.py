from rest_framework import viewsets, filters
from api.models import VaccineSchedule, Immunobiological, VaccinationRecord
from api.serializers import VaccineScheduleSerializer, ImmunobiologicalSerializer, VaccinationRecordSerializer
from django.shortcuts import render
from django.db.models import Count
import json

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

# DASHBOARD TESTE 
def dashboard_view(request):
    total_vacinas_schedule = VaccineSchedule.objects.count()
    total_lotes_estoque = Immunobiological.objects.count()
    
    dados_faixa_etaria = VaccineSchedule.objects.values('age_group').annotate(total=Count('id'))

    labels_grafico = [item['age_group'] for item in dados_faixa_etaria]
    data_grafico = [item['total'] for item in dados_faixa_etaria]

    context = {
        'total_schedule': total_vacinas_schedule,
        'total_stock': total_lotes_estoque,
        'chart_labels': json.dumps(labels_grafico),
        'chart_data': json.dumps(data_grafico),
    }

    return render(request, 'dashboard.html', context)

#Calendário Vacinal
def calendar_view(request):
    schedules = VaccineSchedule.objects.filter(active=True).order_by('min_age_in_days')
    age_groups = sorted(list(set(s.age_group for s in schedules)))
    order = ['Criança', 'Adolescente', 'Adulto', 'Gestantes', 'Idoso']
    age_groups.sort(key=lambda x: order.index(x) if x in order else 99)

    return render(request, 'calendar.html', {
        'schedules': schedules,
        'age_groups': age_groups
    })

def records_list_view(request):
    records = VaccinationRecord.objects.select_related(
        'vaccine_schedule', 
        'immunobiological'
    ).order_by('-application_date')

    return render(request, 'records_list.html', {'records': records})

class VaccinationRecordViewSet(viewsets.ModelViewSet):
    queryset = VaccinationRecord.objects.all()
    serializer_class = VaccinationRecordSerializer
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient_id', 'vaccine_schedule__name']
    ordering_fields = ['application_date', 'created']