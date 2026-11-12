from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from hospital.models import Department, Doctor, Profile

DOCTORS = [
    ('drramesh', 'Ramesh', 'Kumar', 'General Physician', 500, 12),
    ('drsneha', 'Sneha', 'Reddy', 'Cardiology', 900, 15),
    ('drarjun', 'Arjun', 'Rao', 'Dermatology', 700, 8),
    ('drlakshmi', 'Lakshmi', 'Devi', 'Pediatrics', 600, 10),
    ('drvikram', 'Vikram', 'Sharma', 'Orthopedics', 800, 14),
]


class Command(BaseCommand):
    help = 'Add sample departments and doctors'

    def handle(self, *args, **options):
        for username, first, last, dept_name, fees, exp in DOCTORS:
            dept, _ = Department.objects.get_or_create(name=dept_name)
            if User.objects.filter(username=username).exists():
                continue
            user = User.objects.create_user(
                username=username,
                password='doctor123',
                first_name=first,
                last_name=last,
                email=f'{username}@hospital.com',
            )
            Profile.objects.create(user=user, role='doctor')
            Doctor.objects.create(user=user, department=dept, fees=fees, experience=exp)
        self.stdout.write(self.style.SUCCESS('Sample doctors added.'))