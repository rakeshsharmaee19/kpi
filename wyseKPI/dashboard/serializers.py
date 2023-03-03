from rest_framework import serializers
from utils.models import Employee, Project, KPIRating, Workforce, AggregateRating, Sprint

class EmployeeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="emp_id.first_name")
    last_name = serializers.CharField(source="emp_id.last_name")
    username = serializers.CharField(source="emp_id.username")
    email = serializers.CharField(source="emp_id.email")
    class Meta:
        model = Employee
        fields = ("emp_id", "designation", "dob", "location", "projects_allocated", "first_name", "last_name", "username", "email")


class EmployeeRatingSerializer(serializers.ModelSerializer):
    sprint = serializers.IntegerField(source="sprint_id.sprint_number")
    kpi_name = serializers.CharField(source="kpi_id.kpi_name")

    class Meta:
        model = KPIRating
        fields = '__all__'


class EmployeeAggregateRatingSerializer(serializers.ModelSerializer):
    sprint = serializers.IntegerField(source="sprint_id.sprint_number")

    class Meta:
        model = AggregateRating
        fields = '__all__'


class MultiEmployeeAggregateRatingSerializer(serializers.ModelSerializer):
    sprint = serializers.IntegerField(source="sprint_id.sprint_number")
    employee = serializers.SerializerMethodField()

    class Meta:
        model = AggregateRating
        fields = '__all__'
    
    def get_employee(self, obj: AggregateRating):
        emp = Employee.objects.get(emp_id=obj.emp_id)
        return f'{emp.emp_id.first_name} {emp.emp_id.last_name}'


# class NotesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notes
#         fields = ("employee_notes", "emp_id", "project_id", "reviewer_id")


class ProjectSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()
    kpi_count = serializers.SerializerMethodField()
    project_manager_first_name = serializers.CharField(source='project_manager_id.emp_id.first_name', default='NA')
    project_manager_last_name = serializers.CharField(source='project_manager_id.emp_id.last_name', default='')

    class Meta:
        model = Project
        fields = (
            "project_id", "project_name", "project_manager_id",
            "start_date", "end_date", "feedback_frequency",
            "status", "created_by", "feedback", "employee_count",
            "kpi_count", "project_manager_first_name", "project_manager_last_name"
        )

    def get_employee_count(self, obj):
        try:
            return obj.WORK_FORCE_PROJECT_ID.count()
        except Exception:
            return 0

    def get_kpi_count(self, obj):
        try:
            return obj.KPI_PROJECT_Project_ID.count() or 0
        except Exception:
            return 0


class CompletedSprintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sprint
        fields = ('sprint_number',)


# class KpiRatingSerializer(serializers.ModelSerializer):
#     kpi_name = serializers.CharField(source="kpi_id.kpi_name")
#     class Meta:
#         model = KPIRating
#         fields = ("rating", "current_time_stamp", "kpi_id", "kpi_name")



