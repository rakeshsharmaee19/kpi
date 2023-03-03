from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.models import KPI, SystemRole
from utils.utils import serialize
from .serializers import KPISerializer, RoleSerializer, UserSerializer, SystemRoleSerializer


# Create your views here.
class SaveKPI(APIView):
    def post(self, request):
        serializer = KPISerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SaveRole(APIView):
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetail(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SystemRolesList(APIView):
    def get(self, request):
        data = SystemRole.objects.all()
        serializer = SystemRoleSerializer(data, many=True)
        return Response(
            serialize(
                data=serializer.data,
                success=True,
                message='Lists all the system roles available',
                status_code=status.HTTP_200_OK
            ),
            status=status.HTTP_200_OK
        )

