from django.db import models
from django.conf import settings
from core.models import Specialty

class Doctor(models.Model):
    """Shifokor modeli"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name="Foydalanuvchi"
    )
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.CASCADE,
        verbose_name="Mutaxassislik",
        null=True,
        blank=True
    )
    license_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Litsenziya raqami",
        null=True,
        blank=True
    )
    experience_years = models.PositiveIntegerField(
        default=0,
        verbose_name="Tajriba (yil)"
    )
    education = models.TextField(
        blank=True,
        verbose_name="Ta'lim"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Biografiya"
    )
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Konsultatsiya narxi"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Mavjud"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqti"
    )
    
    class Meta:
        verbose_name = "Shifokor"
        verbose_name_plural = "Shifokorlar"
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

class DoctorSchedule(models.Model):
    """Shifokor jadval modeli"""
    WEEKDAYS = [
        (0, 'Dushanba'),
        (1, 'Seshanba'),
        (2, 'Chorshanba'),
        (3, 'Payshanba'),
        (4, 'Juma'),
        (5, 'Shanba'),
        (6, 'Yakshanba'),
    ]
    
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name="Shifokor"
    )
    weekday = models.IntegerField(
        choices=WEEKDAYS,
        verbose_name="Hafta kuni"
    )
    start_time = models.TimeField(verbose_name="Boshlanish vaqti")
    end_time = models.TimeField(verbose_name="Tugash vaqti")
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faol"
    )
    
    class Meta:
        verbose_name = "Shifokor jadvali"
        verbose_name_plural = "Shifokor jadvallari"
        unique_together = ['doctor', 'weekday']
    
    def __str__(self):
        return f"{self.doctor} - {self.get_weekday_display()}"
