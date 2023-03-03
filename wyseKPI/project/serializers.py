from rest_framework import serializers
from django.contrib.auth.models import User
from utils.models import Project, Employee, Workforce, KPI, Roles, KPIProject, Sprint, AggregateRating


class ProjectPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ["project_name", "start_date", "end_date", "created_by", "project_manager_id"]



class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ["sprint_id", "sprint_number", "project_id", "start_date", "end_date", "is_active", "is_completed"]


class PostSprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ["project_id", "sprint_number", "start_date", "end_date"]

#
# class ClassroomSerializer(serializers.ModelSerializer):
#     teachers = TeacherSerializer(source='teacher_set', many=True)
#
#     class Meta:
#         model = Classroom
#         field = ("teachers",)

class ProjectGetSerializer(serializers.ModelSerializer):
    sprint = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ["project_name", "start_date", "end_date", "created_by", "feedback_frequency", "sprint"]

    def get_sprint(self, obj):
        sprint = Sprint.objects.filter(project_id=obj, is_completed=False).first()
        return SprintSerializer(sprint).data


class ProjectPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["project_id", "project_manager_id", "status"]


class LeadProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["project_id", "feedback_frequency", "feedback"]


class KpiSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = ["kpi_id", "kpi_name", "description", "created_by", "is_active"]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ["role_id", "role"]


class KpiProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPIProject
        fields = ["kpi_id", "project_id", "weightage"]


class WorkforceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workforce
        fields = ["project_id", "emp_id", "role_id"]


class WorkforceDetailsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='emp_id.emp_id.first_name')
    last_name = serializers.CharField(source='emp_id.emp_id.last_name')
    designation = serializers.CharField(source='emp_id.designation')
    role = serializers.CharField(source='role_id.role')
    self_assessed = serializers.SerializerMethodField()
    assessed = serializers.SerializerMethodField()

    class Meta:
        model = Workforce
        fields = (
            "project_id", "emp_id", "role_id", "first_name", "last_name", "designation",
            "role", "self_assessed", "assessed")

    def get_self_assessed(self, obj):
        try:
            sprint = Sprint.objects.get(project_id=obj.project_id, is_active=True, is_completed=False)
            AggregateRating.objects.get(
                project_id=obj.project_id,
                sprint_id=sprint,
                emp_id=obj.emp_id,
                review_type='self'
            )
            return True
        except Sprint.DoesNotExist:
            return False
        except AggregateRating.DoesNotExist:
            return False

    def get_assessed(self, obj):
        try:
            sprint = Sprint.objects.get(project_id=obj.project_id, is_active=True, is_completed=False)
            AggregateRating.objects.get(
                project_id=obj.project_id,
                sprint_id=sprint,
                emp_id=obj.emp_id,
                review_type='review'
            )
            return True
        except Sprint.DoesNotExist:
            return False
        except AggregateRating.DoesNotExist:
            return False


class EmployeeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='emp_id.first_name')
    last_name = serializers.CharField(source='emp_id.last_name')
    email = serializers.CharField(source='emp_id.email')
    username = serializers.CharField(source='emp_id.username')

    class Meta:
        model = Employee
        fields = ["emp_id", "designation", "dob", "location", "projects_allocated", "first_name", "last_name", "email",
                  "username"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username']


class ProjectKPIListSerializer(serializers.ModelSerializer):
    kpi_name = serializers.CharField(source="kpi_id.kpi_name")
    description = serializers.CharField(source="kpi_id.description")
    created_by = serializers.CharField(source="kpi_id.created_by")
    is_active = serializers.CharField(source="kpi_id.is_active")

    class Meta:
        model = KPIProject
        fields = ["kpi_id", "kpi_name", "description", "created_by", "is_active", "weightage"]


class EmployeesUnderManagerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="emp_id.emp_id.first_name")
    last_name = serializers.CharField(source="emp_id.emp_id.last_name")
    username = serializers.CharField(source="emp_id.emp_id.username")
    email = serializers.CharField(source="emp_id.emp_id.email")
    designation = serializers.CharField(source="emp_id.designation")
    dob = serializers.CharField(source="emp_id.dob")
    location = serializers.CharField(source="emp_id.location")
    projects_allocated = serializers.CharField(source="emp_id.projects_allocated")

    class Meta:
        model = Workforce
        fields = (
        "emp_id", "designation", "dob", "location", "projects_allocated", "first_name", "last_name", "username",
        "email")


class SprintPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ["sprint_id", "is_active"]
