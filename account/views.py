from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer


def send_activation_mail(user):
    code = user.create_activation_code()
    send_mail('Активация аккаунта',
              f'Вы успешно зарегистрировались. Пожалуйста активируйте свой аккаунт. Для этого пройдите по ссылке http://127.0.0.1:8000/accounts/activate/{code}/',
              'test@test.com',
              [user.email, ])


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_activation_mail(user)
            return Response('Аккаунт успешно создан')


class ActivationView(APIView):
    def get(self, request, activation_code):
        User = get_user_model()
        user = get_object_or_404(User, activation_code=activation_code)
        user.activate_with_code(activation_code)
        return Response('Ваш аккаунт успешно активирован')


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Вы успешно вышли из своего аккаунта')