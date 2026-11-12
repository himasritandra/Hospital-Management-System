from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Patient,Department,Doctor


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        phone = validated_data.pop('phone', '')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, role='patient', phone=phone)
        Patient.objects.create(user=user)
        return user
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class DoctorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'department', 'department_name', 'fees', 'experience']

    def get_name(self, obj):
        full = obj.user.get_full_name()
        return f"Dr. {full or obj.user.username}"