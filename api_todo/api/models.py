from django.db import models
class Todo(models.Model):
    name = models.CharField(max_length=120)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
class VaccineSchedule(models.Model):
    id = models.IntegerField(primary_key=True)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
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
    
    # colocar auto_now_add e auto_now depois
    created = models.DateTimeField()
    modified = models.DateTimeField()
    
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