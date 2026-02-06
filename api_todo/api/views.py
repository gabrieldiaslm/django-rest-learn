from rest_framework import viewsets, filters
from api.models import VaccineSchedule, Immunobiological, VaccinationRecord, Patient
from api.serializers import VaccineScheduleSerializer, ImmunobiologicalSerializer, VaccinationRecordSerializer
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
import json


def patient_list_view(request):
    query = request.GET.get('q', '') 
    
    if query:
        patients = Patient.objects.filter(
            Q(name__icontains=query) | 
            Q(cpf__icontains=query) | 
            Q(cns__icontains=query)
        ).filter(active=True).order_by('name')
    else:
        patients = Patient.objects.filter(active=True).order_by('name')[:50]

    return render(request, 'patient_list.html', {
        'patients': patients,
        'query': query
    })


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

def patient_card_view(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    
    # 1. Busca todas as vacinas que existem no calendário
    all_schedules = VaccineSchedule.objects.filter(active=True).order_by('min_age_in_days')
    
    # 2. Busca todas as vacinas que o paciente JÁ TOMOU
    taken_records = VaccinationRecord.objects.filter(patient=patient, active=True)
    
    # Cria um dicionário para acesso rápido: { schedule_id: registro }
    taken_map = {rec.vaccine_schedule_id: rec for rec in taken_records}
    
    # 3. Monta a lista final para o template (Status: OK ou PENDENTE)
    timeline = []
    for schedule in all_schedules:
        record = taken_map.get(schedule.id)
        
        status = 'PENDENTE'
        date_taken = None
        lote = None
        
        if record:
            status = 'OK'
            date_taken = record.application_date
            lote = record.immunobiological.batch_number if record.immunobiological else 'N/A'
            
        timeline.append({
            'schedule': schedule,
            'status': status,
            'record': record,
            'date_taken': date_taken,
            'lote': lote
        })

    return render(request, 'patient_card.html', {
        'patient': patient, 
        'timeline': timeline
    })