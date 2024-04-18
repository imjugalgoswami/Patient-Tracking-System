from datetime import date, timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, Patient, Doctor,Appointment,MedicalRecord
from django.contrib.auth.decorators import login_required
from .forms import PatientUpdateForm, DoctorUpdateForm
from .forms import MedicalRecordForm,AppointmentForm

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Patient, Doctor
from django.contrib.auth import get_user_model

User = get_user_model()

from django.db import IntegrityError

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        is_patient = 'is_patient' in request.POST
        is_doctor = 'is_doctor' in request.POST

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        try:
            existing_user = User.objects.get(username=username)
            return render(request, 'register.html', {'error': 'Username already exists. Please choose a different one.'})
        except User.DoesNotExist:
            pass

        try:
            existing_email = User.objects.get(email=email)
            return render(request, 'register.html', {'error': 'Email already exists. Please use a different one.'})
        except User.DoesNotExist:
            pass

        user = User.objects.create_user(username=username, password=password, email=email)
        user.is_patient = is_patient
        user.is_doctor = is_doctor
        user.save()

        if is_patient:
            patient = Patient(user=user)
            patient.save()

        if is_doctor:
            qualification = request.POST['qualification']
            specialization = request.POST['specialization']
            doctor = Doctor(user=user, qualification=qualification, specialization=specialization)
            doctor.save()

        return redirect('login')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def update_patient(request):
    if request.method == 'POST':
        form = PatientUpdateForm(request.POST, instance=request.user.patient)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PatientUpdateForm(instance=request.user.patient)
    
    return render(request, 'update_patient.html', {'form': form})


@login_required
def update_doctor(request):
    if request.method == 'POST':
        form = DoctorUpdateForm(request.POST, instance=request.user.doctor)
        if form.is_valid():
            form.save()
            return redirect('some-success-url')
    else:
        try:
            form = DoctorUpdateForm(instance=request.user.doctor)
        except Doctor.DoesNotExist:
            form = DoctorUpdateForm()
        
    context = {'form': form}
    return render(request, 'update_doctor.html', context)

@login_required
def upload_medical_record(request, patient_id=None):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = Patient.objects.get(user__id=patient_id)
            medical_record.save()
            return redirect('upload-record-success')  
    else:
        form = MedicalRecordForm()
    
    return render(request, 'upload_medical_record.html', {'form': form, 'patient_id': patient_id})

@login_required
def upload_record_success(request):
    return render(request, 'upload_record_success.html')



@login_required
def schedule_appointment(request):
    doctors = Doctor.objects.all()  
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect('appointment_success')
    else:
        form = AppointmentForm()
    
    context = {'form': form, 'doctors': doctors}  
    return render(request, 'schedule_appointment.html', context)

def appointment_success(request):
    return render(request, 'appointment_success.html')

@login_required
def view_upcoming_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user, date__gte=date.today()).order_by('date', 'time')
    return render(request, 'view_upcoming_appointments.html', {'appointments': appointments})

@login_required
def view_appointment_history(request):
    appointments = Appointment.objects.filter(patient=request.user, date__lt=date.today()).order_by('-date', '-time')
    return render(request, 'view_appointment_history.html', {'appointments': appointments})


@login_required
def doctor_appointments(request):
    today = timezone.now().date()
    start_date = request.GET.get('start_date', today - timedelta(days=7))
    end_date = request.GET.get('end_date', today)
    
    appointments = Appointment.objects.filter(
        doctor=request.user.doctor, 
        date__range=[start_date, end_date]
    ).order_by('date', 'time')
    
    context = {
        'appointments': appointments,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'doctor_appointments.html', context)


@login_required
def search_patients(request):
    keyword = request.GET.get('keyword')
    
    if keyword:
        medical_records = MedicalRecord.objects.filter(description__icontains=keyword)
        
        patients = User.objects.filter(patient__medicalrecord__in=medical_records).distinct()
    else:
        patients = []

    return render(request, 'search_patients.html', {'patients': patients, 'keyword': keyword})

def doctor_patient_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_doctor:
        appointments = Appointment.objects.filter(doctor=request.user.doctor)
        return render(request, 'doctor_patient_list.html', {'appointments': appointments})

@login_required
def dashboard(request):
    if request.user.is_patient:
        return render(request, 'patient_dashboard.html')
    elif request.user.is_doctor:
        return render(request, 'doctor_dashboard.html')
    else:
        return redirect('home')


@login_required
def doctor_patient_filter(request):
    patients = Patient.objects.all()

    patient_id = request.GET.get('patient_id')
    patient_name = request.GET.get('patient_name')
    severity = request.GET.get('severity')

    if patient_id:
        patients = patients.filter(user__id=patient_id)
    if patient_name:
        patients = patients.filter(user__username__icontains=patient_name)
    if severity:
        patients = patients.filter(medicalrecord__severity=severity)

    return render(request, 'doctor_patient_filter.html', {'patients': patients})

@login_required
def view_medical_history(request, patient_id):
    try:
        patient = Patient.objects.get(user__id=patient_id)
    except Patient.DoesNotExist:
        return redirect('doctor_patient_filter')  

    appointments = Appointment.objects.filter(patient__id=patient_id).order_by('-date', '-time')
    medical_records = MedicalRecord.objects.filter(patient__user__id=patient_id).order_by('-uploaded_at')

    return render(request, 'view_medical_history.html', {
        'patient': patient,
        'appointments': appointments,
        'medical_records': medical_records
    })