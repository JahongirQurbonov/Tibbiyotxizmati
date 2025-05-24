from django.urls import path
from .views import (
    patient_profile_view, create_patient_profile_view, medical_records_view,
    patient_list_view, patient_detail_view, edit_patient_profile_view
)

app_name = 'patients'

urlpatterns = [
    path('profile/', patient_profile_view, name='patient_profile'),
    path('profile/create/', create_patient_profile_view, name='create_profile'),
    path('profile/edit/', edit_patient_profile_view, name='edit_profile'),
    path('medical-records/', medical_records_view, name='medical_records'),
    path('list/', patient_list_view, name='patient_list'),
    path('<int:patient_id>/', patient_detail_view, name='patient_detail'),
]
