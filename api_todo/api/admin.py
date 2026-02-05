from django.contrib import admin
from .models import VaccinationRecord, VaccineSchedule, Immunobiological

@admin.register(VaccineSchedule)
class VaccineScheduleAdmin(admin.ModelAdmin):
    # Colunas que aparecem na lista
    list_display = ('id', 'name', 'dose_description', 'age_group', 'active', 'vaccine_id')
    
    # Filtros laterais
    list_filter = ('age_group', 'active', 'created')
    
    # Barra de busca (pesquisa por nome, ID da vacina ou descrição da dose)
    search_fields = ('name', 'vaccine_id', 'dose_description')
    
    # Ordenação padrão
    ordering = ('min_age_in_days', 'id')

@admin.register(Immunobiological)
class ImmunobiologicalAdmin(admin.ModelAdmin):
    # Colunas que aparecem na lista
    list_display = ('id', 'name', 'manufacturer', 'batch_number', 'expiration_date', 'active')
    
    # Filtros laterais (útil para ver o que está vencido ou inativo)
    list_filter = ('manufacturer', 'active', 'expiration_date')
    
    # Barra de busca
    search_fields = ('name', 'batch_number', 'manufacturer')
    
    # Ordenação (do que vence mais cedo para o mais tarde)
    ordering = ('expiration_date',)

@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'vaccine_schedule','immunobiological', 'application_date', 'created', 'modified')