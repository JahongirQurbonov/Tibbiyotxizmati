from django.db import models
from django.conf import settings
from django.utils import timezone
from doctors.models import Doctor
from patients.models import Patient

class Appointment(models.Model):
    """Qabulga yozilish modeli"""
    STATUS_CHOICES = [
        ('scheduled', 'Rejalashtirilgan'),
        ('confirmed', 'Tasdiqlangan'),
        ('completed', 'Tugallangan'),
        ('cancelled', 'Bekor qilingan'),
        ('no_show', 'Kelmagan'),
    ]
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name="Bemor"
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name="Shifokor"
    )
    appointment_date = models.DateField(verbose_name="Qabul sanasi")
    appointment_time = models.TimeField(verbose_name="Qabul vaqti")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        verbose_name="Holati"
    )
    reason = models.TextField(
        blank=True,
        verbose_name="Murojaat sababi"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Izohlar"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqti"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan vaqti"
    )
    
    class Meta:
        verbose_name = "Qabulga yozilish"
        verbose_name_plural = "Qabulga yozilishlar"
        ordering = ['-appointment_date', '-appointment_time']
    
    def __str__(self):
        return f"{self.patient} - {self.doctor} ({self.appointment_date})"
    
    @property
    def is_past(self):
        """Qabul o'tgan vaqtmi?"""
        now = timezone.now()
        appointment_datetime = timezone.datetime.combine(
            self.appointment_date, 
            self.appointment_time
        )
        appointment_datetime = timezone.make_aware(appointment_datetime)
        return appointment_datetime < now
