from django.db import models
from django.conf import settings

class Patient(models.Model):
    """Bemor modeli"""
    GENDER_CHOICES = [
        ('M', 'Erkak'),
        ('F', 'Ayol'),
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        verbose_name="Foydalanuvchi"
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Jinsi",
        null=True,
        blank=True
    )
    blood_type = models.CharField(
        max_length=3,
        choices=BLOOD_TYPE_CHOICES,
        blank=True,
        verbose_name="Qon guruhi"
    )
    emergency_contact = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Favqulodda aloqa"
    )
    emergency_phone = models.CharField(
        max_length=15,
        blank=True,
        verbose_name="Favqulodda telefon"
    )
    medical_history = models.TextField(
        blank=True,
        verbose_name="Tibbiy tarix"
    )
    allergies = models.TextField(
        blank=True,
        verbose_name="Allergiyalar"
    )
    current_medications = models.TextField(
        blank=True,
        verbose_name="Joriy dorilar"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqti"
    )
    
    class Meta:
        verbose_name = "Bemor"
        verbose_name_plural = "Bemorlar"
    
    def __str__(self):
        return f"{self.user.get_full_name()}"

class MedicalRecord(models.Model):
    """Tibbiy yozuv modeli"""
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_records',
        verbose_name="Bemor"
    )
    doctor = models.ForeignKey(
        'doctors.Doctor',
        on_delete=models.CASCADE,
        verbose_name="Shifokor"
    )
    diagnosis = models.TextField(verbose_name="Tashxis")
    treatment = models.TextField(verbose_name="Davolash")
    prescription = models.TextField(
        blank=True,
        verbose_name="Retsept"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Izohlar"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqti"
    )
    
    class Meta:
        verbose_name = "Tibbiy yozuv"
        verbose_name_plural = "Tibbiy yozuvlar"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.patient} - {self.created_at.strftime('%d.%m.%Y')}"
