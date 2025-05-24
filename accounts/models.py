from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Foydalanuvchi modeli"""
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('doctor', 'Shifokor'),
        ('patient', 'Bemor'),
        ('staff', 'Xodim'),
    ]
    
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='patient',
        verbose_name="Rol"
    )
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        verbose_name="Telefon raqami"
    )
    birth_date = models.DateField(
        blank=True, 
        null=True,
        verbose_name="Tug'ilgan sanasi"
    )
    address = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Manzil"
    )
    
    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
