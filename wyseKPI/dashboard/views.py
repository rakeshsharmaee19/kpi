# from django.shortcuts import render
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from utils.models import Employee, Project, KPIRating, Workforce, AggregateRating, Sprint
from .serializers import (
    EmployeeSerializer,
    EmployeeRatingSerializer,
    ProjectSerializer,
    EmployeeAggregateRatingSerializer,
    CompletedSprintSerializer,
    MultiEmployeeAggregateRatingSerializer
)
from utils.utils import serialize
# from .serializers import NotesSerializer,KpiRatingSerializer
# from django.db import connection
# import datetime

from utils import utils


# Create your views here.
class EmployeeDetails(APIView):

    def get(self, request,emp_id):
        try:
            employee = Employee.objects.get(emp_id=emp_id)
            serializer = EmployeeSerializer(employee)
            return Response(utils.serialize(
                data=serializer.data,
                success=True,
                message='Details of the employee',
                status_code=status.HTTP_200_OK
            ), status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response(utils.serialize(
                data=None,
                success=False,
                message='Employee not found',
                status_code=status.HTTP_404_NOT_FOUND
            ), status=status.HTTP_404_NOT_FOUND)


class EmployeeRating(APIView):

    def get(self, request, emp_id, project_id, from_sprint=None, to_sprint=None):
        if from_sprint and to_sprint:

            if from_sprint > to_sprint:
                return Response(utils.serialize(
                    data=None,
                    success=False,
                    message="To Sprint cannot be smaller than From Sprint",
                    status_code=status.HTTP_400_BAD_REQUEST
                ), status=status.HTTP_400_BAD_REQUEST)
                
            ratings = KPIRating.objects.filter(
                emp_id=emp_id,
                project_id=project_id,
                review_type='review',
                sprint_id__sprint_number__gte=from_sprint,
                sprint_id__sprint_number__lte=to_sprint
            )
        else:
            ratings = KPIRating.objects.filter(emp_id=emp_id, project_id=project_id, review_type='review')

        if ratings.exists():
            serializer = EmployeeRatingSerializer(ratings, many=True)
        
            sprints = {}
            for rating in serializer.data:
                if rating['sprint'] in sprints:
                    sprints[rating['sprint']][rating['kpi_name']] = rating['rating']
                else:
                    # sprints[rating['sprint']]['sprint'] = rating['sprint']
                    sprints[rating['sprint']] = {'sprint': rating['sprint'], rating['kpi_name']: rating['rating']}
            data = list(sprints.values())
            success=True
            message='Ratings of an employee for a project'
            status_code=status.HTTP_200_OK
        else:
            data = None
            success = False
            message = f'No ratings available for employee {emp_id} for the project {project_id}'
            status_code = status.HTTP_404_NOT_FOUND
            
        return Response(utils.serialize(
            data=data,
            success=success,
            message=message,
            status_code=status_code
        ), status=status_code)


class EmployeeSelfRating(APIView):

    def get(self, request, emp_id, project_id, from_sprint=None, to_sprint=None):
        if from_sprint and to_sprint:

            if from_sprint > to_sprint:
                return Response(utils.serialize(
                    data=None,
                    success=False,
                    message="To Sprint cannot be smaller than From Sprint",
                    status_code=status.HTTP_400_BAD_REQUEST
                ), status=status.HTTP_400_BAD_REQUEST)
                
            ratings = KPIRating.objects.filter(
                emp_id=emp_id,
                project_id=project_id,
                review_type='self',
                sprint_id__sprint_number__gte=from_sprint,
                sprint_id__sprint_number__lte=to_sprint
            )
        else:
            ratings = KPIRating.objects.filter(emp_id=emp_id, project_id=project_id, review_type='self')

        if ratings.exists():
            serializer = EmployeeRatingSerializer(ratings, many=True)
        
            sprints = {}
            for rating in serializer.data:
                if rating['sprint'] in sprints:
                    sprints[rating['sprint']][rating['kpi_name']] = rating['rating']
                else:
                    # sprints[rating['sprint']]['sprint'] = rating['sprint']
                    sprints[rating['sprint']] = {'sprint': rating['sprint'], rating['kpi_name']: rating['rating']}
            data = list(sprints.values())
            success=True
            message='Self Ratings of an employee for a project'
            status_code=status.HTTP_200_OK
        else:
            data = None
            success = False
            message = f'No self ratings available for employee {emp_id} for the project {project_id}'
            status_code = status.HTTP_404_NOT_FOUND
            
        return Response(utils.serialize(
            data=data,
            success=success,
            message=message,
            status_code=status_code
        ), status=status_code)


class EmployeeAggregateRating(APIView):

    def get(self, request, emp_id, project_id, from_sprint=None, to_sprint=None):
        if from_sprint and to_sprint:
            ratings = AggregateRating.objects.filter(
                emp_id=emp_id,
                project_id=project_id,
                sprint_id__sprint_number__gte=from_sprint,
                sprint_id__sprint_number__lte=to_sprint,
                review_type='review'
            )
        else:
            ratings = AggregateRating.objects.filter(emp_id=emp_id, project_id=project_id, review_type='review')

        if ratings.exists():
            serializer = EmployeeAggregateRatingSerializer(ratings, many=True)
            data = serializer.data
            success = True
            message = 'Aggregate ratings of an employee for a project'
            status_code = status.HTTP_200_OK
        else:
            data = None
            success = False
            message = f'No ratings available for employee {emp_id} for the project {project_id}'
            status_code = status.HTTP_404_NOT_FOUND
        
        return Response(utils.serialize(
            data=data,
            success=success,
            message=message,
            status_code=status_code
        ), status=status_code)


class EmployeeSelfAggregateRating(APIView):

    def get(self, request, emp_id, project_id, from_sprint=None, to_sprint=None):
        if from_sprint and to_sprint:
            ratings = AggregateRating.objects.filter(
                emp_id=emp_id,
                project_id=project_id,
                sprint_id__sprint_number__gte=from_sprint,
                sprint_id__sprint_number__lte=to_sprint,
                review_type='self'
            )
        else:
            ratings = AggregateRating.objects.filter(emp_id=emp_id, project_id=project_id, review_type='self')

        if ratings.exists():
            serializer = EmployeeAggregateRatingSerializer(ratings, many=True)
            data = serializer.data
            success = True
            message = 'Aggregate ratings (self) of an employee for a project'
            status_code = status.HTTP_200_OK
        else:
            data = None
            success = False
            message = f'No self ratings available for employee {emp_id} for the project {project_id}'
            status_code = status.HTTP_404_NOT_FOUND
        
        return Response(utils.serialize(
            data=data,
            success=success,
            message=message,
            status_code=status_code
        ), status=status_code)


class MultipleEmployeesAggregateRating(APIView):
    def get(self, request, project_id, from_sprint=None, to_sprint=None):
        if from_sprint and to_sprint:

            if from_sprint > to_sprint:
                return Response(utils.serialize(
                    data=None,
                    success=False,
                    message="To Sprint cannot be smaller than From Sprint",
                    status_code=status.HTTP_400_BAD_REQUEST
                ), status=status.HTTP_400_BAD_REQUEST)

            ratings = AggregateRating.objects.filter(
                project_id=project_id,
                sprint_id__sprint_number__gte=from_sprint,
                sprint_id__sprint_number__lte=to_sprint,
                review_type='review'
            )
        else:
            ratings = AggregateRating.objects.filter(project_id=project_id, review_type='review')

        if ratings.exists():
            serializer = MultiEmployeeAggregateRatingSerializer(ratings, many=True)

            sprints = {}
            for rating in serializer.data:
                if rating['sprint'] in sprints:
                    sprints[rating['sprint']][rating['employee']] = rating['rating']
                else:
                    sprints[rating['sprint']] = {'sprint': rating['sprint'], rating['employee']: rating['rating']}
            data = list(sprints.values())
            
            success = True
            message = 'Aggregate ratings of an employee for a project'
            status_code = status.HTTP_200_OK
        else:
            data = None
            success = False
            message = f'No ratings available for the project {project_id}'
            status_code = status.HTTP_404_NOT_FOUND
        
        return Response(utils.serialize(
            data=data,
            success=success,
            message=message,
            status_code=status_code
        ), status=status_code)


# class SaveEmployeeNotes(APIView):

#     def post(self, request):
#         notes = NotesSerializer(data=request.data)
#         if notes.is_valid():
#             notes.save()
#             return Response(status=status.HTTP_201_CREATED)
#         return Response(notes.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectsList(APIView):

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


# class KpiRatings(APIView):

#     def get(self, request, emp_id, project_id):
#         ratings = KPIRating.objects.filter(emp_id=emp_id, project_id=project_id)
#         serializer = KpiRatingSerializer(ratings, many=True)
#         return Response(serializer.data)

class ProjectsUnderManager(APIView):

    def get(self, request,project_manager_id):
        projects_list = Project.objects.filter(project_manager_id = project_manager_id)
        serializer = ProjectSerializer(projects_list, many=True)
        return Response(serializer.data)


class ProjectToEmployee(APIView):
    def get(self,request,emp_id):
        projects_list = Workforce.objects.filter(emp_id = emp_id)
        serializer = ProjectSerializer(
            [project.project_id for project in projects_list],
            many=True
        )
        return Response(serializer.data)


# class WeightedRating(APIView):

#     def get(self, request, project_id, emp_id):
#         cursor  = connection.cursor()
#         query ="""
#             select utils_kpiproject.project_id_id,utils_project.project_name,utils_kpirating.emp_id_id,auth_user.username,
#             utils_kpiproject.kpi_id_id,utils_kpi.kpi_name,utils_kpirating.rating,
#             utils_kpirating.current_time_stamp,utils_kpiproject.weightage from
#             utils_kpi inner join utils_kpiproject
#             on utils_kpi.kpi_id = utils_kpiproject.kpi_id_id
#             inner join utils_kpirating
#             on utils_kpiproject.project_id_id = utils_kpirating.project_id_id and utils_kpiproject.kpi_id_id = utils_kpirating.kpi_id_id
#             inner join auth_user
#             on auth_user.id = utils_kpirating.emp_id_id
#             inner join utils_project
#             on utils_project.project_id = utils_kpirating.project_id_id
#             where utils_kpirating.project_id_id = %s and utils_kpirating.emp_id_id = %s;
#         """
#         value = (project_id, emp_id)
#         cursor.execute(query,value)
#         data = cursor.fetchall()
#         parse_data = []
#         update_parse_list = []
#         datetime_list =set()
#         for datas in data:
#             value = {}
#             value['project_id'] = datas[0]
#             value['project_name']=datas[1]
#             value['emp_id']=datas[2]
#             value['username']=datas[3]
#             value['kpi_is']=datas[4]
#             value['kpi_name']=datas[5]
#             value['rating'] = datas[6]
#             datetime = datas[7]
#             value['datetime']=datetime.date()
#             datetime_list.add(datetime.date())
#             value['weightage']= datas[8]
#             parse_data.append(value)
#         for i in datetime_list:
#             w_rate = 0
#             val ={}
#             for j in parse_data:
#                 if i == j['datetime']:
#                     w_rate =w_rate + j['rating']*(j['weightage']/100)
#                     j['weightage_rating'] = round(w_rate,2)
#                     val['project_name'] = j['project_name']
#                     val['username'] = j['username']
#                     val['datetime'] = j['datetime']
#                     val['weightage_rating'] = j['weightage_rating']
#             update_parse_list.append(val)
#         return Response(update_parse_list)


class AllEmployees(APIView):
    def get(self, request):
        employees_list = Employee.objects.all()
        serializer = EmployeeSerializer(employees_list, many=True)
        return Response(serializer.data)


class CompletedSprintList(APIView):

    def get(self, request, project_id):
        sprints = Sprint.objects.filter(project_id=project_id, is_completed=True)
        serializer = CompletedSprintSerializer(sprints, many=True)
        return Response(
            serialize(
                data=serializer.data,
                success=True,
                message=f'Completed sprints for project {project_id}',
                status_code=status.HTTP_200_OK
            )
        )

