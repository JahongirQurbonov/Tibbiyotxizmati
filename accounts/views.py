from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .forms import DoctorRegistrationForm, PatientRegistrationForm, CustomAuthenticationForm

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, "Muvaffaqiyatli kirildi!")
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Tizimdan chiqildi!")
        return super().dispatch(request, *args, **kwargs)

def register_choice_view(request):
    """Ro'yxatdan o'tish turini tanlash"""
    return render(request, 'accounts/register_choice.html')

def register_doctor_view(request):
    """Shifokor ro'yxatdan o'tishi"""
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Shifokor sifatida muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect('core:dashboard')
    else:
        form = DoctorRegistrationForm()
    
    return render(request, 'accounts/register_doctor.html', {'form': form})

def register_patient_view(request):
    """Bemor ro'yxatdan o'tishi"""
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Bemor sifatida muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect('core:dashboard')
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'accounts/register_patient.html', {'form': form})
