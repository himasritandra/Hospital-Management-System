from django.contrib import admin
from .models import Profile, Department, Doctor, Patient, Slot, Appointment, Prescription

admin.site.register(Profile)
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Slot)
admin.site.register(Appointment)
admin.site.register(Prescription)
