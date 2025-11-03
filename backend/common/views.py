from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer


@method_decorator(csrf_exempt, name="dispatch")
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

