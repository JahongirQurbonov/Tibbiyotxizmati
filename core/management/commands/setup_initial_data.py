from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Department, Specialty
from doctors.models import Doctor
from patients.models import Patient

User = get_user_model()

class Command(BaseCommand):
    help = 'Boshlang\'ich ma\'lumotlarni yaratish'

    def handle(self, *args, **options):
        # Bo'limlar yaratish
        departments_data = [
            {'name': 'Ichki kasalliklar', 'description': 'Ichki a\'zolar kasalliklari bo\'limi'},
            {'name': 'Jarrohlik', 'description': 'Jarrohlik amaliyotlari bo\'limi'},
            {'name': 'Pediatriya', 'description': 'Bolalar kasalliklari bo\'limi'},
            {'name': 'Nevrologiya', 'description': 'Asab tizimi kasalliklari bo\'limi'},
        ]
        
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={'description': dept_data['description']}
            )
            if created:
                self.stdout.write(f"Bo'lim yaratildi: {dept.name}")

        # Mutaxassisliklar yaratish
        specialties_data = [
            {'name': 'Kardiolog', 'department': 'Ichki kasalliklar'},
            {'name': 'Gastroenterolog', 'department': 'Ichki kasalliklar'},
            {'name': 'Umumiy jarroh', 'department': 'Jarrohlik'},
            {'name': 'Pediatr', 'department': 'Pediatriya'},
            {'name': 'Nevrolog', 'department': 'Nevrologiya'},
            {'name': 'Oftalmolog', 'department': 'Ichki kasalliklar'},
        ]
        
        for spec_data in specialties_data:
            try:
                department = Department.objects.get(name=spec_data['department'])
                spec, created = Specialty.objects.get_or_create(
                    name=spec_data['name'],
                    defaults={'department': department}
                )
                if created:
                    self.stdout.write(f"Mutaxassislik yaratildi: {spec.name}")
            except Department.DoesNotExist:
                self.stdout.write(f"Bo'lim topilmadi: {spec_data['department']}")

        # Namuna shifokor yaratish
        if not User.objects.filter(username='doctor1').exists():
            doctor_user = User.objects.create_user(
                username='doctor1',
                email='doctor1@example.com',
                password='password123',
                first_name='Ahmadjon',
                last_name='Karimov',
                role='doctor'
            )
            
            try:
                specialty = Specialty.objects.get(name='Kardiolog')
                Doctor.objects.create(
                    user=doctor_user,
                    specialty=specialty,
                    license_number='DOC001',
                    experience_years=10,
                    education='Toshkent Tibbiyot Akademiyasi',
                    bio='Yurak kasalliklari bo\'yicha 10 yillik tajribaga ega shifokor',
                    consultation_fee=150000,
                    is_available=True
                )
                self.stdout.write("Namuna shifokor yaratildi: doctor1/password123")
            except Specialty.DoesNotExist:
                self.stdout.write("Kardiolog mutaxassisligi topilmadi")

        # Namuna bemor yaratish
        if not User.objects.filter(username='patient1').exists():
            patient_user = User.objects.create_user(
                username='patient1',
                email='patient1@example.com',
                password='password123',
                first_name='Farrux',
                last_name='Aliyev',
                role='patient'
            )
            
            Patient.objects.create(
                user=patient_user,
                gender='M',
                blood_type='A+',
                emergency_contact='Ona - Gulnora Aliyeva',
                emergency_phone='+998901234567'
            )
            self.stdout.write("Namuna bemor yaratildi: patient1/password123")

        self.stdout.write(
            self.style.SUCCESS('Boshlang\'ich ma\'lumotlar muvaffaqiyatli yaratildi!')
        )
