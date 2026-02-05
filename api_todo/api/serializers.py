from api.models import Todo, VaccineSchedule, Immunobiological, VaccinationRecord
from rest_framework import serializers

class VaccineScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineSchedule
        fields = '__all__'

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'name','done','created_at']

class ImmunobiologicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Immunobiological
        fields = '__all__'

class VaccinationRecordSerializer(serializers.ModelSerializer):
    vaccine_name = serializers.CharField(source='vaccine_schedule.name', read_only=True)
    batch_info = serializers.CharField(source='immunobiological.batch_number', read_only=True)

    class Meta:
        model = VaccinationRecord
        fields = [
            'id', 
            'patient_id', 
            'vaccine_schedule',   # Aqui você envia o ID da regra (ex: 1)
            'immunobiological',   # Aqui você envia o ID do lote (ex: 55)
            'vaccine_name',       # Campo extra apenas para leitura
            'batch_info',         # Campo extra apenas para leitura
            'application_date', 
            'created',
            'active'
        ]