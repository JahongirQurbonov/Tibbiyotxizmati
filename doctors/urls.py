from django.urls import path
from .views import (
    doctor_list_view, doctor_detail_view, doctor_profile_view,
    create_doctor_profile_view, doctor_patients_view, edit_doctor_profile_view
)

app_name = 'doctors'

urlpatterns = [
    path('', doctor_list_view, name='doctor_list'),
    path('<int:doctor_id>/', doctor_detail_view, name='doctor_detail'),
    path('profile/', doctor_profile_view, name='doctor_profile'),
    path('profile/create/', create_doctor_profile_view, name='create_profile'),
    path('profile/edit/', edit_doctor_profile_view, name='edit_profile'),
    path('patients/', doctor_patients_view, name='doctor_patients'),
]
