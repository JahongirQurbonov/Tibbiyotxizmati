from django.db import models

class Department(models.Model):
    """Bo'lim modeli"""
    name = models.CharField(max_length=100, verbose_name="Bo'lim nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    
    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"
    
    def __str__(self):
        return self.name

class Specialty(models.Model):
    """Mutaxassislik modeli"""
    name = models.CharField(max_length=100, verbose_name="Mutaxassislik nomi")
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        related_name='specialties',
        verbose_name="Bo'lim"
    )
    description = models.TextField(blank=True, verbose_name="Tavsif")
    
    class Meta:
        verbose_name = "Mutaxassislik"
        verbose_name_plural = "Mutaxassisliklar"
    
    def __str__(self):
        return self.name
