from rest_framework import viewsets, filters
from api.models import VaccineSchedule, Immunobiological, VaccinationRecord, Patient, UsuarioTeste
from api.serializers import VaccineScheduleSerializer, ImmunobiologicalSerializer, VaccinationRecordSerializer
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
import json

def usertest_list_view(request):
    query = request.GET.get('q', '')
    
    if query:
        # Filtra pelo nome (ou outro campo que você queira)
        # 'icontains' faz busca insensível a maiúsculas/minúsculas
        usertest = UsuarioTeste.objects.filter(name__icontains=query) 
    else:
        usertest = UsuarioTeste.objects.all()
    
    # O primeiro argumento TEM que ser 'request'
    return render(request, 'usertest.html', {
        'usertest': usertest,
        'query': query
    })


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
    
    # Busca otimizada com select_related
    all_schedules = VaccineSchedule.objects.filter(active=True).order_by('min_age_in_days')
    taken_records = VaccinationRecord.objects.filter(
        patient=patient, active=True
    ).select_related('immunobiological')

    # Dicionário mapeando ID da vacina ao registro
    taken_map = {rec.vaccine_schedule_id: rec for rec in taken_records}
    
    timeline = []
    for schedule in all_schedules:
        record = taken_map.get(schedule.id)
        timeline.append({
            'schedule': schedule,
            'status': 'OK' if record else 'PENDENTE',
            'date_taken': record.application_date if record else None,
            'lote': record.immunobiological.batch_number if record and record.immunobiological else 'N/A'
        })

    return render(request, 'patient_card.html', {'patient': patient, 'timeline': timeline})