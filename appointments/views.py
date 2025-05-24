from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Appointment
from .forms import AppointmentForm
from doctors.models import Doctor
from patients.models import Patient

@login_required
def appointment_list_view(request):
    """Qabullar ro'yxati"""
    user = request.user
    appointments = []
    
    if user.role == 'patient':
        try:
            patient = user.patient_profile
            appointments = Appointment.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            messages.warning(request, "Avval bemor profilini yarating!")
            return redirect('patients:create_profile')
    elif user.role == 'doctor':
        try:
            doctor = user.doctor_profile
            appointments = Appointment.objects.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            messages.warning(request, "Avval shifokor profilini yarating!")
            return redirect('doctors:create_profile')
    else:
        # Admin yoki boshqa rollar
        appointments = Appointment.objects.all()
    
    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments
    })

@login_required
def book_appointment_view(request, doctor_id):
    """Qabulga yozilish"""
    if request.user.role != 'patient':
        messages.error(request, "Faqat bemorlar qabulga yozila oladi!")
        return redirect('core:home')
    
    doctor = get_object_or_404(Doctor, id=doctor_id, is_available=True)
    
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        messages.error(request, "Avval bemor profilini yarating!")
        return redirect('patients:create_profile')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.doctor = doctor
            
            # Bir xil vaqtda boshqa qabul borligini tekshirish
            existing = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment.appointment_date,
                appointment_time=appointment.appointment_time,
                status__in=['scheduled', 'confirmed']
            ).exists()
            
            if existing:
                messages.error(request, "Bu vaqtda shifokor band!")
                return render(request, 'appointments/book_appointment.html', {
                    'form': form, 'doctor': doctor
                })
            
            appointment.save()
            messages.success(request, "Qabulga muvaffaqiyatli yozildingiz!")
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/book_appointment.html', {
        'doctor': doctor,
        'form': form
    })

@login_required
def appointment_detail_view(request, appointment_id):
    """Qabul tafsilotlari"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Faqat tegishli foydalanuvchilar ko'ra oladi
    if (request.user.role == 'patient' and appointment.patient.user != request.user) or \
       (request.user.role == 'doctor' and appointment.doctor.user != request.user):
        if not request.user.is_staff:
            messages.error(request, "Bu qabulni ko'rishga ruxsatingiz yo'q!")
            return redirect('appointments:appointment_list')
    
    return render(request, 'appointments/appointment_detail.html', {
        'appointment': appointment
    })

@login_required
def cancel_appointment_view(request, appointment_id):
    """Qabulni bekor qilish"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Faqat bemor yoki shifokor bekor qila oladi
    if (request.user.role == 'patient' and appointment.patient.user != request.user) or \
       (request.user.role == 'doctor' and appointment.doctor.user != request.user):
        if not request.user.is_staff:
            messages.error(request, "Bu qabulni bekor qilishga ruxsatingiz yo'q!")
            return redirect('appointments:appointment_list')
    
    if appointment.status in ['completed', 'cancelled']:
        messages.error(request, "Bu qabulni bekor qilib bo'lmaydi!")
        return redirect('appointments:appointment_detail', appointment_id=appointment_id)
    
    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request, "Qabul bekor qilindi!")
    return redirect('appointments:appointment_list')
