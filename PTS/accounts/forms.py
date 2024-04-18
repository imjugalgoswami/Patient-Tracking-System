from django import forms
from .models import Patient, Doctor
from .models import MedicalRecord,Appointment

class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['phone', 'address']

class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['phone', 'specialization']

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['symptoms', 'diagnosis', 'prescribed_medication', 'record_type', 'file']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


