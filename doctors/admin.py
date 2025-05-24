from django.contrib import admin
from .models import Doctor, DoctorSchedule

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'license_number', 'experience_years', 'is_available')
    list_filter = ('specialty', 'is_available', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'license_number')

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'weekday', 'start_time', 'end_time', 'is_active')
    list_filter = ('weekday', 'is_active')
    search_fields = ('doctor__user__first_name', 'doctor__user__last_name')
