from django.contrib import admin
from .models import User, Patient, Doctor,Appointment,MedicalRecord

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'email', 'is_patient', 'is_doctor']

class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address']

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'specialization', 'qualification']

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date', 'time','status']

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'symptoms', 'diagnosis', 'record_type', 'uploaded_at']
    search_fields = ['patient__username', 'symptoms', 'diagnosis', 'record_type']
    list_filter = ['uploaded_at']

admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
