from django.urls import path
from .views import (
    appointment_list_view, book_appointment_view, appointment_detail_view,
    cancel_appointment_view
)

app_name = 'appointments'

urlpatterns = [
    path('', appointment_list_view, name='appointment_list'),
    path('book/<int:doctor_id>/', book_appointment_view, name='book_appointment'),
    path('<int:appointment_id>/', appointment_detail_view, name='appointment_detail'),
    path('<int:appointment_id>/cancel/', cancel_appointment_view, name='cancel_appointment'),
]
