from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class SystemRole(models.Model):
    SystemRoleId = models.AutoField(primary_key=True)
    SystemRole = models.CharField(max_length=255)

    def __str__(self):
        return self.SystemRole


class Employee(models.Model):
    emp_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="profile")
    designation = models.CharField(max_length=255)
    dob = models.DateField(default=None)
    location = models.CharField(max_length=255)
    projects_allocated = models.TextField(default=None)
    system_role_id = models.ForeignKey(SystemRole, on_delete=models.RESTRICT,
                                       to_field="SystemRoleId", related_name="Employee_SystemRoleId", default=None, null=True)

    def __int__(self):
        return self.emp_id

    def __str__(self):
        return self.emp_id.username


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    project_manager_id = models.ForeignKey(Employee, on_delete=models.RESTRICT,
                                           to_field='emp_id', related_name='Project_PROJECT_MANAGER_ID', default=None,
                                           null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    feedback_frequency = models.CharField(max_length=200)
    status = models.CharField(max_length=10)
    created_by = models.ForeignKey(Employee, on_delete=models.RESTRICT, to_field="emp_id",
                                   related_name='Project_CREATED_BY', default=None, null=True)
    feedback = models.CharField(max_length=10, null=True)

    def __int__(self):
        return self.project_id

    def __str__(self):
        return self.project_name


class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=255)

    def __int__(self):
        return self.role_id

    def __str__(self):
        return self.role


class Workforce(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.RESTRICT, to_field="project_id",
                                   related_name="WORK_FORCE_PROJECT_ID",
                                   default=None)
    emp_id = models.ForeignKey(Employee, on_delete=models.RESTRICT, to_field="emp_id", related_name="WORK_FORCE_EMP_ID",
                               default=None)
    role_id = models.ForeignKey(Roles, on_delete=models.RESTRICT, to_field="role_id",
                                related_name="WORK_FORCE_ROLE_ID",
                                default=None)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('project_id', 'emp_id')

    def __int__(self):
        return self.project_id


class KPI(models.Model):
    kpi_id = models.AutoField(primary_key=True)
    kpi_name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(Employee, on_delete=models.RESTRICT, to_field="emp_id",
                                   related_name="KPI_MASTER_CREATED_BY",
                                   default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField()

    def __int__(self):
        return self.kpi_id

    def __str__(self):
        return self.kpi_name


class KPIProject(models.Model):
    kpi_id = models.ForeignKey(KPI, on_delete=models.RESTRICT, to_field="kpi_id", related_name="KPI_PROJECT_KPI_ID",
                               default=None)
    project_id = models.ForeignKey(Project, on_delete=models.RESTRICT, to_field="project_id",
                                   related_name="KPI_PROJECT_Project_ID", default=None)
    weightage = models.FloatField(default=None)

    class Meta:
        unique_together = ('kpi_id', 'project_id')

    def __int__(self):
        return self.kpi_id


# class Notes(models.Model):
#     note_id = models.AutoField(primary_key=True)
#     employee_notes = models.TextField()
#     emp_id = models.ForeignKey(Employee, on_delete=models.RESTRICT, to_field="emp_id", related_name="NOTES_EMP_ID",
#                                default=None)
#     employee_current_time_stamp = models.DateTimeField(auto_now_add = True)
#     project_id = models.ForeignKey(Project, on_delete=models.RESTRICT, to_field="project_id", related_name="NOTES_PROJECT_ID",
#                                    default=None)
#     reviewer_id = models.ForeignKey(Employee, on_delete=models.RESTRICT, to_field="emp_id", related_name="NOTES_REVIEWER_ID",
#                                     default=None )
#     reviewer_notes = models.TextField(default=None, null=True)
#     reviewer_current_time_stamp = models.DateTimeField(null = True, auto_now=True)

#     class Meta:
#         ordering = ['-employee_current_time_stamp']

#     def __int__(self):
#         return self.note_id


class Sprint(models.Model):
    sprint_id = models.AutoField(primary_key=True)
    sprint_number = models.IntegerField()
    project_id = models.ForeignKey(Project, on_delete=models.RESTRICT, to_field="project_id",
                                   related_name="Sprint_Project_ID", default=None)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('sprint_number', 'project_id')
        ordering = ['start_date', 'end_date']

    def __int__(self):
        return self.sprint_id

    def __str__(self):
        return f'{self.project_id.project_name} - {self.sprint_id}'


class KPIRating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    emp_id = models.ForeignKey(Employee, on_delete=models.RESTRICT, to_field="emp_id", related_name="KPI_RATING_EMP_ID",
                               default=None)
    kpi_id = models.ForeignKey(KPI, on_delete=models.RESTRICT, to_field="kpi_id",
                               related_name="KPI_RATING_KPI_ID",
                               default=None)
    rating = models.IntegerField()
    project_id = models.ForeignKey(Project, on_delete=models.RESTRICT, to_field="project_id",
                                   related_name="KPI_RATING_Project_ID", default=None)
    current_time_stamp = models.DateTimeField(auto_now_add=True)
    reviewer_id = models.ForeignKey(Employee, on_delete=models.RESTRICT, to_field="emp_id",
                                    related_name="KPI_RATING_REVIEWER_ID",
                                    default=None)
    sprint_id = models.ForeignKey(Sprint, on_delete=models.RESTRICT, to_field="sprint_id",
                                  related_name="KPI_RATING_SPRINT_ID",
                                  default=None)
    review_type = models.CharField(max_length=20, default='review')
    notes = models.TextField(default=None)

    class Meta:
        ordering = ['current_time_stamp']

    def __int__(self):
        return self.rating_id

    def __str__(self):
        return f'{self.emp_id.emp_id.username} - {self.review_type} - {str(self.sprint_id)}'


class AggregateRating(models.Model):
    emp_id = models.ForeignKey(Employee, on_delete=models.RESTRICT, to_field="emp_id",
                               related_name="AggregateRating_EMP_ID",
                               default=None)
    project_id = models.ForeignKey(Project, on_delete=models.RESTRICT, to_field="project_id",
                                   related_name="AggregateRating_Project_ID", default=None)
    rating = models.FloatField()
    sprint_id = models.ForeignKey(Sprint, on_delete=models.RESTRICT, to_field="sprint_id",
                                  related_name="AggregateRating_SPRINT_ID",
                                  default=None)
    review_type = models.CharField(max_length=20, default='review')

    class Meta:
        ordering = ['sprint_id']
        unique_together = ('sprint_id', 'project_id', 'emp_id', 'review_type')
