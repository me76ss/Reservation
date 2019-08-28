from django.contrib.auth import login, logout
from rest_framework import status, generics
from rest_framework import views
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import LoginSerializer, UserSerializer, UserCreateSerializer


class UserProfile(views.APIView):
    serializer_class = UserSerializer

    def get(self, request):
        user_data = UserSerializer(self.request.user)
        return Response({'user': user_data.data})


class UserLogin(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class RegisterUser(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return Response({'user': response.data})


class UserLogout(views.APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
