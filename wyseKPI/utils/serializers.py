from rest_framework import serializers
from utils.models import KPI, Roles, Employee, SystemRole
from django.contrib.auth.models import User


class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = ("kpi_name", "description", "created_by", "is_active")


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ('role', )

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("designation", "dob", "location", "projects_allocated")

class UserSerializer(serializers.ModelSerializer):
    designation = serializers.CharField(max_length=255)
    dob = serializers.DateField()
    location = serializers.CharField(max_length=255)
    projects_allocated = serializers.CharField()
    system_role_id = serializers.IntegerField()
    
    class Meta:
        model = User
        fields = (
            "username", "email", "password", "first_name",
            "last_name", "designation", "dob", "location",
            "projects_allocated", "system_role_id"
        )

    def create(self, validated_data: dict):
        # profile_data = validated_data.pop('profile')
        profile = {
            "designation": validated_data.pop('designation'),
            "dob": validated_data.pop('dob'),
            "location": validated_data.pop('location'),
            "projects_allocated": validated_data.pop('projects_allocated'),
        }
        system_role_id = validated_data.pop('system_role_id')
        system_role = SystemRole.objects.get(SystemRoleId=system_role_id)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        # for track_data in tracks_data:
        Employee.objects.create(emp_id=user, system_role_id=system_role, **profile)
        return user


class SystemRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemRole
        fields = '__all__'

