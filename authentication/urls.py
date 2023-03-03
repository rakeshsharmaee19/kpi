from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import ChangePasswordView, WyseTokenObtainPairView


urlpatterns = [
    path('token/', WyseTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
]
