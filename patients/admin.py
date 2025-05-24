from django.contrib import admin
from .models import Patient, MedicalRecord

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'blood_type', 'created_at')
    list_filter = ('gender', 'blood_type', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'diagnosis', 'created_at')
    list_filter = ('doctor', 'created_at')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'diagnosis')
