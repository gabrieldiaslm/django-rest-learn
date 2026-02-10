from datetime import date
from django.db import models

class Todo(models.Model):
    name = models.CharField(max_length=120)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class UsuarioTeste(models.Model):
    name = models.CharField(max_length=120)
    nickname = models.CharField(max_length=120)
    is_alive = models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)


class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    
    name = models.CharField("Nome Completo", max_length=255)
    cpf = models.CharField("CPF", max_length=14, null=True, blank=True)
    cns = models.CharField("Cartão SUS (CNS)", max_length=50, null=True, blank=True)
    birth_date = models.DateField("Data de Nascimento", null=True, blank=True)
    mother_name = models.CharField("Nome da Mãe", max_length=255, null=True, blank=True)
    
    gender = models.CharField("Sexo", max_length=20, null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (CNS: {self.cns})"

    @property
    def age_years(self):
        if not self.birth_date:
            return 0
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

class VaccineSchedule(models.Model):
    id = models.IntegerField(primary_key=True)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField()
    
    active = models.BooleanField(default=True)
    
    vaccine_id = models.CharField(max_length=100) # Ex: "bcg", "hepatite-b-birth"
    name = models.CharField(max_length=255) # Ex: "BCG", "Hepatite B"
    
    # Ex: "Criança", "Adolescente", "Gestantes"
    age_group = models.CharField(max_length=50)
    
    min_age_in_days = models.IntegerField()
    max_age_in_days = models.IntegerField(null=True, blank=True)
    
    dose_number = models.IntegerField()
    dose_description = models.CharField(max_length=255)
    diseases_prevented = models.JSONField(default=list)

    class Meta:
        verbose_name = "Vaccine Schedule"
        verbose_name_plural = "Vaccine Schedules"
        ordering = ['min_age_in_days', 'id']

    def __str__(self):
        return f"{self.name} ({self.dose_description}) - {self.age_group}"

class Immunobiological(models.Model):

    id = models.IntegerField(primary_key=True)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    active = models.BooleanField(default=True)
    
    name = models.CharField(max_length=255) # Ex: "BCG", "Tríplice viral SCR"
    manufacturer = models.CharField(max_length=255) # Ex: "Butantan", "Fiocruz"
    batch_number = models.CharField(max_length=100) # Ex: "lote2025", "234AA"
    expiration_date = models.DateField() # XX/XX/XXXX
    description = models.TextField(null=True, blank=True)
    contraindications = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Immunobiological"
        verbose_name_plural = "Immunobiologicals"
        ordering = ['expiration_date', 'name']

    def __str__(self):
        return f"{self.name} - Lote: {self.batch_number} ({self.manufacturer})"

class VaccinationRecord(models.Model):
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='vaccinations',
        verbose_name="Paciente"
    )
    
    vaccine_schedule = models.ForeignKey('VaccineSchedule', on_delete=models.PROTECT, related_name='records')
    immunobiological = models.ForeignKey('Immunobiological', on_delete=models.PROTECT, null=True, blank=True, related_name='records')
    application_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Registro de Vacinação"
        verbose_name_plural = "Registros de Vacinação"
        ordering = ['-application_date'] 

    def __str__(self):
        return f"{self.patient_id} - {self.vaccine_schedule.name} ({self.application_date.strftime('%d/%m/%Y')})"

