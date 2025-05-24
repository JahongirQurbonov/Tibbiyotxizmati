from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Doctor
from .forms import DoctorProfileForm
from patients.models import Patient
from appointments.models import Appointment

def doctor_list_view(request):
    """Shifokorlar ro'yxati"""
    doctors = Doctor.objects.filter(is_available=True).select_related('user', 'specialty')
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})

def doctor_detail_view(request, doctor_id):
    """Shifokor tafsilotlari"""
    doctor = get_object_or_404(Doctor, id=doctor_id, is_available=True)
    schedules = doctor.schedules.filter(is_active=True).order_by('weekday')
    return render(request, 'doctors/doctor_detail.html', {
        'doctor': doctor,
        'schedules': schedules
    })

@login_required
def doctor_profile_view(request):
    """Shifokor profili"""
    if request.user.role != 'doctor':
        messages.error(request, "Bu sahifaga faqat shifokorlar kira oladi!")
        return redirect('core:home')
    
    try:
        doctor = request.user.doctor_profile
        schedules = doctor.schedules.all().order_by('weekday')
        return render(request, 'doctors/doctor_profile.html', {
            'doctor': doctor,
            'schedules': schedules
        })
    except Doctor.DoesNotExist:
        return redirect('doctors:create_profile')

@login_required
def create_doctor_profile_view(request):
    """Shifokor profili yaratish"""
    if request.user.role != 'doctor':
        messages.error(request, "Bu sahifaga faqat shifokorlar kira oladi!")
        return redirect('core:home')
    
    if hasattr(request.user, 'doctor_profile'):
        return redirect('doctors:doctor_profile')
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.user = request.user
            doctor.save()
            messages.success(request, "Shifokor profili muvaffaqiyatli yaratildi!")
            return redirect('doctors:doctor_profile')
    else:
        form = DoctorProfileForm()
    
    return render(request, 'doctors/create_profile.html', {'form': form})

@login_required
def doctor_patients_view(request):
    """Shifokor bemorlarini ko'rish"""
    if request.user.role != 'doctor':
        messages.error(request, "Bu sahifaga faqat shifokorlar kira oladi!")
        return redirect('core:home')
    
    try:
        doctor = request.user.doctor_profile
        # Shifokor qabul qilgan bemorlar
        patients = Patient.objects.filter(
            appointments__doctor=doctor
        ).distinct().select_related('user')
        
        return render(request, 'doctors/doctor_patients.html', {
            'patients': patients,
            'doctor': doctor
        })
    except Doctor.DoesNotExist:
        return redirect('doctors:create_profile')

@login_required
def edit_doctor_profile_view(request):
    """Shifokor profilini tahrirlash"""
    if request.user.role != 'doctor':
        messages.error(request, "Bu sahifaga faqat shifokorlar kira oladi!")
        return redirect('core:home')
    
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return redirect('doctors:create_profile')
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi!")
            return redirect('doctors:doctor_profile')
    else:
        form = DoctorProfileForm(instance=doctor)
    
    return render(request, 'doctors/edit_profile.html', {'form': form, 'doctor': doctor})
