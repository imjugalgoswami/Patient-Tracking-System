from django.urls import path
from . import views

urlpatterns = [
    # other url patterns
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('update/', views.update_patient, name='update_patient'),
    path('update-doctor/', views.update_doctor, name='update_doctor'),
    # path('upload-medical-record/', views.upload_medical_record, name='upload_medical_record'),
    path('upload-medical-record/<int:patient_id>/', views.upload_medical_record, name='upload_medical_record'),
    path('upload-record-success/', views.upload_record_success, name='upload-record-success'),

    path('schedule-appointment/', views.schedule_appointment, name='schedule_appointment'),
    path('appointment-success/', views.appointment_success, name='appointment_success'),
    path('view-upcoming-appointments/', views.view_upcoming_appointments, name='view_upcoming_appointments'),
    path('view-appointment-history/', views.view_appointment_history, name='view_appointment_history'),
    path('doctor-appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('search-patients/', views.search_patients, name='search_patients'),
    path('patients/', views.doctor_patient_list, name='doctor_patient_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('filter-patients/', views.doctor_patient_filter, name='doctor_patient_filter'),
    path('view-medical-history/<int:patient_id>/', views.view_medical_history, name='view_medical_history'),






]
