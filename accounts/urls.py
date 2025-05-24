from django.urls import path
from .views import (
    CustomLoginView, CustomLogoutView, 
    register_choice_view, register_doctor_view, register_patient_view
)

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register_choice_view, name='register_choice'),
    path('register/doctor/', register_doctor_view, name='register_doctor'),
    path('register/patient/', register_patient_view, name='register_patient'),
]
