# Patient Tracking System (PTS)

## Overview
PTS is a Django-based web application designed for managing patients, doctors, medical records, and appointments in a healthcare setting.

## Features
- **User Authentication**: Register, login, and logout functionalities with roles: patient and doctor.
- **Profile Management**: Update profiles for patients and doctors.
- **Medical Record Management**: Upload medical records with details.
- **Appointment Scheduling**: Schedule appointments and view upcoming ones.
- **Search Functionality**: Search patients based on medical record keywords.
- **Dashboards**: Personalized dashboards for patients and doctors.

## Technologies Used
- **Django**: Backend framework.
- **HTML/CSS**: Frontend development.
- **Bootstrap**: Styling and responsive design.

## Setup and Installation
1. **Clone Repository**
   \`\`\`bash
   git clone https://github.com/imjugalgoswami/Patient-Tracking-System
   cd Patient-Tracking-System
   \`\`\`

2. **Install Dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Database Migration**
   \`\`\`bash
   python manage.py makemigrations
   python manage.py migrate
   \`\`\`

4. **Configure Media Settings**
   - Open `settings.py` and set the following:
     \`\`\`python
     MEDIA_ROOT = os.path.join(BASE_DIR, 'medical_records')
     MEDIA_URL = '/medical_records/'
     \`\`\`

5. **Run Application**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

6. **Access Application**
   Open `http://127.0.0.1:8000/` in your browser.

## Usage
- **Registration**: Fill in details and select role.
- **Login**: Use username and password.
- **Profile**: Update details from the dashboard.
- **Medical Records**: Upload from the dashboard.
- **Appointments**: Schedule and manage from the dashboard.
- **Search**: Use search functionality for patients.

## Notes
- Configure `MEDIA_ROOT` and `MEDIA_URL` for file uploads in `settings.py`.
- Assumes one account per doctor and patient.

## Contact
For questions, contact [Jugal Goswami] at [iamjugalgoswami@gmail.com].


