# userapp/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        """
        Регистрация: просто создаём пользователя, токен не выдаём
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "Пользователь успешно зарегистрирован",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "phone_number": user.phone_number
            }
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Логин: выдаём JWT токены
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Генерируем JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "phone_number": user.phone_number
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })