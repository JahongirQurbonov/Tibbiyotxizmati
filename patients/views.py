from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient, MedicalRecord
from .forms import PatientProfileForm

@login_required
def patient_profile_view(request):
    """Bemor profili"""
    if request.user.role != 'patient':
        messages.error(request, "Bu sahifaga faqat bemorlar kira oladi!")
        return redirect('core:home')
    
    try:
        patient = request.user.patient_profile
        medical_records = patient.medical_records.all()[:10]
        return render(request, 'patients/patient_profile.html', {
            'patient': patient,
            'medical_records': medical_records
        })
    except Patient.DoesNotExist:
        return redirect('patients:create_profile')

@login_required
def create_patient_profile_view(request):
    """Bemor profili yaratish"""
    if request.user.role != 'patient':
        messages.error(request, "Bu sahifaga faqat bemorlar kira oladi!")
        return redirect('core:home')
    
    if hasattr(request.user, 'patient_profile'):
        return redirect('patients:patient_profile')
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()
            messages.success(request, "Bemor profili muvaffaqiyatli yaratildi!")
            return redirect('patients:patient_profile')
    else:
        form = PatientProfileForm()
    
    return render(request, 'patients/create_profile.html', {'form': form})

@login_required
def medical_records_view(request):
    """Tibbiy yozuvlar"""
    if request.user.role != 'patient':
        messages.error(request, "Bu sahifaga faqat bemorlar kira oladi!")
        return redirect('core:home')
    
    try:
        patient = request.user.patient_profile
        medical_records = patient.medical_records.all()
        return render(request, 'patients/medical_records.html', {
            'medical_records': medical_records,
            'patient': patient
        })
    except Patient.DoesNotExist:
        return redirect('patients:create_profile')

@login_required
def patient_list_view(request):
    """Bemorlar ro'yxati (shifokorlar uchun)"""
    if request.user.role != 'doctor':
        messages.error(request, "Bu sahifaga faqat shifokorlar kira oladi!")
        return redirect('core:home')
    
    patients = Patient.objects.all().select_related('user')
    return render(request, 'patients/patient_list.html', {'patients': patients})

@login_required
def patient_detail_view(request, patient_id):
    """Bemor tafsilotlari (shifokorlar uchun)"""
    if request.user.role != 'doctor':
        messages.error(request, "Bu sahifaga faqat shifokorlar kira oladi!")
        return redirect('core:home')
    
    patient = get_object_or_404(Patient, id=patient_id)
    medical_records = patient.medical_records.all()
    
    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'medical_records': medical_records
    })

@login_required
def edit_patient_profile_view(request):
    """Bemor profilini tahrirlash"""
    if request.user.role != 'patient':
        messages.error(request, "Bu sahifaga faqat bemorlar kira oladi!")
        return redirect('core:home')
    
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        return redirect('patients:create_profile')
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi!")
            return redirect('patients:patient_profile')
    else:
        form = PatientProfileForm(instance=patient)
    
    return render(request, 'patients/edit_profile.html', {'form': form, 'patient': patient})
