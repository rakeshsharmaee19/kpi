from utils.models import Project, Workforce, Employee, KPI, Roles, KPIProject, Sprint
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .generatesprint import datedivide
from .serializers import (
    KpiSerializer, ProjectPostSerializer, ProjectPutSerializer, KpiProjectSerializer,
    LeadProjectSerializer, RoleSerializer, WorkforceSerializer, EmployeeSerializer,
    UserSerializer, WorkforceDetailsSerializer, ProjectGetSerializer, SprintSerializer,
    PostSprintSerializer, ProjectKPIListSerializer, EmployeesUnderManagerSerializer, SprintPutSerializer
)
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User


class AddProject(APIView):
    """
    Rahul
    """
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = ProjectPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "model created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        list_of_projects = Project.objects.all()
        serializer = ProjectPostSerializer(list_of_projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectPutSerializer(project, data=request.data)
        if serializer.is_valid():
            k = serializer.save()
            return Response({"message": "model created successfully"}, status=status.HTTP_200_OK)
        return Response({"message": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)


class SingleProject(APIView):
    def get(self, request, pk):
        projects = Project.objects.get(project_id=pk)
        serializer = ProjectGetSerializer(projects)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LeadProject(APIView):
    """
    Rahul
    """

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = LeadProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            k = serializer.save()
            project_id = k.project_id
            feedback_frequency = serializer.data["feedback_frequency"]
            start_date = k.start_date
            end_date = k.end_date
            date_list = datedivide(project_id, start_date, end_date, feedback_frequency)
            sprint_serializer = PostSprintSerializer(data=date_list, many=True)
            if sprint_serializer.is_valid():
                sprint_serializer.save()
            return Response({"message": "model created successfully"}, status=status.HTTP_200_OK)
        return Response({"message": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)


class GetAllKpi(generics.ListAPIView):
    """
    Rahul
    """
    queryset = KPI.objects.all()
    serializer_class = KpiSerializer


class AssignKpi(APIView):
    """
    Rahul
    """

    def post(self, request):
        # Delete the existing KPIs
        data = request.data
        project_id = data[0]['project_id']
        KPIProject.objects.filter(project_id=project_id).delete()

        serializer = KpiProjectSerializer(data=data, many=True)
        total_weightage = 0
        if serializer.is_valid():
            for weightage in serializer.data:
                total_weightage += weightage['weightage']
            if total_weightage == 100:
                serializer.save()
                return Response({"message": "model created successfully"}, status=status.HTTP_201_CREATED)
            else:
                serializer.error_messages = "Aggregate Weightage is not 100, please re enter the weightages."

        return Response({"message": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, kpi_id):
        data = KPIProject.objects.get(project_id=project_id, kpi_id=kpi_id)
        data.delete()
        return Response(status=status.HTTP_200_OK)


class RolesList(generics.ListAPIView):
    """
    Rahul
    """
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer


class AssignWorkForce(APIView):
    """
    Assign, List Workforce for a project
    """

    def post(self, request):
        serializer = WorkforceSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "model created successfully"}, safe=False)
        return JsonResponse({"message": serializer.error_messages}, safe=False)

    def delete(self, request, project_id, emp_id):
        data = Workforce.objects.get(project_id=project_id, emp_id=emp_id)
        data.delete()
        return Response({'message': 'Employee removed successfully'}, status=status.HTTP_200_OK)

    def get(self, request, project_id):
        data = Workforce.objects.filter(project_id=project_id)
        serializer = WorkforceDetailsSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetManager(APIView):
    """
    fetch manager list
    """

    def get(self, request):
        data = User.objects.filter(profile__designation='manager')
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetOtherEmployee(APIView):
    """
    get employees who are not assigned in the project
    """

    def get(self, request, project_id):
        project = Project.objects.get(project_id=project_id)
        data = Workforce.objects.filter(project_id=project_id).values('emp_id')
        data = [d['emp_id'] for d in data]
        data.append(project.project_manager_id.pk)
        data = Employee.objects.exclude(pk__in=data).exclude(designation__in=['Admin', 'Manager'])
        serializer = EmployeeSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)


class GetOtherKPI(APIView):
    """
    get kpis which are not assigned to the project
    """

    def get(self, request, project_id):
        data = KPIProject.objects.filter(project_id=project_id).values('kpi_id')
        data = [d['kpi_id'] for d in data]
        data = KPI.objects.exclude(pk__in=data)
        serializer = KpiSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)


class GetSprintDetails(APIView):
    """
    Get sprint details related to particular project
    """

    def get(self, request, project_id):
        data = Sprint.objects.filter(project_id=project_id)
        serializer = SprintSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectKPIList(generics.ListAPIView):
    """
    Get all the KPIs in a project
    """
    serializer_class = ProjectKPIListSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return KPIProject.objects.filter(project_id=project_id)


class GetEmployeesUnderManager(APIView):
    """
    Get all employees under particular manager
    """

    def get(self, request, project_manager_id):
        data = Project.objects.filter(project_manager_id=project_manager_id).values('project_id')
        data = [d['project_id'] for d in data]
        data = Workforce.objects.filter(project_id__in=data)
        serializer = EmployeesUnderManagerSerializer(data, many=True)

        # Remove duplicates from the serializer data
        distinct_employees = set()
        response = []
        for employee in list(serializer.data):
            if employee['emp_id'] not in distinct_employees:
                #                 del response[index]
                #             else:
                response.append(employee)
            distinct_employees.add(employee['emp_id'])

        return Response(response)


class sprint_isactive(APIView):
    def get_object(self, sprint_id):
        try:
            return Sprint.objects.get(sprint_id=sprint_id)
        except Project.DoesNotExist:
            raise Http404

    def put(self, request, sprint_id):
        sprint = self.get_object(sprint_id)
        serializer = SprintPutSerializer(sprint, data=request.data)
        if serializer.is_valid():
            k = serializer.save()
            return Response({"message": "model created successfully"}, status=status.HTTP_200_OK)
        return Response({"message": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
