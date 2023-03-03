from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ChangePasswordSerializer, WyseTokenObtainPairSerializer


class WyseTokenObtainPairView(TokenObtainPairView):
    serializer_class = WyseTokenObtainPairSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
