from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='doctors')
    fees = models.DecimalField(max_digits=8, decimal_places=2)
    experience = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"


class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Slot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('doctor', 'date', 'start_time')
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.doctor} - {self.date} {self.start_time}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='appointments')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} with {self.doctor} ({self.status})"


class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='prescription')
    medicines = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.appointment}"
