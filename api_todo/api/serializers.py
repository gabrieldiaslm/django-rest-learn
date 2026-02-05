from api.models import Todo, VaccineSchedule, Immunobiological
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