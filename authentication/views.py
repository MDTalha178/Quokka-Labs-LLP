"""
In this file write a code for authentication part
"""
# Local import
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from authentication.models import User
from authentication.serializer import LoginSerializer, RegisterSerializer, UserSerializer
from common.utils import custom_response, custom_error_response
from common.views import ModelViewSet


class RegisterViewSet(ModelViewSet):
    """
    This class is used to register or create an account
    """
    http_method_names = ('post',)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        """
        this method is used to create data for registration
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(detail='Account created successfully!', data=serializer.data)
        return custom_error_response(
            status.HTTP_400_BAD_REQUEST, detail='Something went wrong', data=serializer.errors
        )


class LoginViewSet(ModelViewSet):
    """
    This class is used to perform a login
    """
    # request method
    http_method_names = ('post',)
    serializer_class = LoginSerializer
    queryset = User

    def create(self, request, *args, **kwargs):
        """
        create a login post create
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return custom_response(detail='Login successful!', data=serializer.data)
        return custom_error_response(
            status.HTTP_401_UNAUTHORIZED, detail='Invalid Credential', data=serializer.errors
        )


class RefreshTokenView(ModelViewSet):
    http_method_names = ('post',)

    def create(self, request, *args, **kwargs):
        """
        create a new refresh and access token
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        refresh_token = request.data.get('refresh_token')
        refresh = RefreshToken(refresh_token)
        try:
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token
            })

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutViewset(ModelViewSet):
    """
    this class is used to logout
    """
    http_method_names = ('post',)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """
        used to logout user
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return custom_response(status=status.HTTP_200_OK, detail='Logout Successfully!')
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(ModelViewSet):
    """
    get profile
    """
    http_method_names = ('get',)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User

    def retrieve(self, request, *args, **kwargs):
        self.get_object()
        serializer = self.serializer_class(self.get_object())
        return custom_response(status=status.HTTP_200_OK, data=serializer.data)
