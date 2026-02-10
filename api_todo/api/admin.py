from django.contrib import admin
from .models import Patient, UsuarioTeste, VaccineSchedule, Immunobiological, VaccinationRecord


@admin.register(UsuarioTeste)
class UsuarioTesteAdmin(admin.ModelAdmin):
    list_display=('name', 'nickname', 'is_alive', 'created_at')
    search_fields = ('name', 'nickname')
    ordering = ('created_at', 'name')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'cns', 'cpf', 'birth_date', 'get_age', 'active')
    
    search_fields = ('name', 'cpf', 'cns')
    
    list_filter = ('active', 'gender', 'created')
    
    ordering = ('name',)

    def get_age(self, obj):
        return f"{obj.age_years} anos"
    get_age.short_description = 'Idade'


@admin.register(VaccineSchedule)
class VaccineScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'dose_description', 'age_group', 'vaccine_id', 'active')
    
    search_fields = ('name', 'vaccine_id')
    
    list_filter = ('age_group', 'active')
    
    ordering = ('min_age_in_days', 'id')


@admin.register(Immunobiological)
class ImmunobiologicalAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch_number', 'manufacturer', 'expiration_date', 'active')
    
    search_fields = ('name', 'batch_number', 'manufacturer')
    list_filter = ('active', 'expiration_date', 'manufacturer')
    
    ordering = ('expiration_date',)


@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'vaccine_schedule', 'application_date', 'get_lote', 'active')
    
    list_filter = ('active', 'application_date', 'vaccine_schedule__age_group')
    
    search_fields = ('patient__name', 'patient__cpf', 'vaccine_schedule__name')
    
    date_hierarchy = 'application_date'
    autocomplete_fields = ['patient', 'vaccine_schedule', 'immunobiological']

    def get_lote(self, obj):
        if obj.immunobiological:
            return obj.immunobiological.batch_number
        return "-"
    get_lote.short_description = 'Lote'