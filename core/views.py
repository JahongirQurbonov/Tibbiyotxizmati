from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

def home_view(request):
    """Bosh sahifa"""
    context = {
        'total_doctors': Doctor.objects.count(),
        'total_patients': Patient.objects.count(),
        'total_appointments': Appointment.objects.count(),
    }
    return render(request, 'core/home.html', context)

@login_required
def dashboard_view(request):
    """Dashboard sahifasi"""
    user = request.user
    context = {'user': user}
    
    if user.role == 'doctor':
        try:
            doctor = user.doctor_profile
            context.update({
                'doctor': doctor,
                'recent_appointments': Appointment.objects.filter(
                    doctor=doctor
                ).order_by('-appointment_date', '-appointment_time')[:5],
                'total_patients': Patient.objects.filter(
                    appointments__doctor=doctor
                ).distinct().count(),
                'today_appointments': Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date=timezone.now().date()
                ).count()
            })
            return render(request, 'core/doctor_dashboard.html', context)
        except Doctor.DoesNotExist:
            messages.warning(request, "Shifokor profili yaratilmagan!")
            return redirect('doctors:create_profile')
            
    elif user.role == 'patient':
        try:
            patient = user.patient_profile
            context.update({
                'patient': patient,
                'recent_appointments': Appointment.objects.filter(
                    patient=patient
                ).order_by('-appointment_date', '-appointment_time')[:5],
                'medical_records': patient.medical_records.all()[:5] if hasattr(patient, 'medical_records') else []
            })
            return render(request, 'core/patient_dashboard.html', context)
        except Patient.DoesNotExist:
            messages.warning(request, "Bemor profili yaratilmagan!")
            return redirect('patients:create_profile')
    
    # Admin yoki boshqa rollar uchun
    context.update({
        'total_doctors': Doctor.objects.count(),
        'total_patients': Patient.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'recent_appointments': Appointment.objects.all().order_by('-created_at')[:10]
    })
    return render(request, 'core/admin_dashboard.html', context)
