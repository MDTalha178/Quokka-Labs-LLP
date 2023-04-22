"""
This file is used store common class and method
"""

# Third party import
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    This class is used to perform a crud operation in database this is common class
    """
    pass


def get_token(user):
    """
    create token for user
    :param user:
    :return: token
    """
    refresh = RefreshToken.for_user(user)
    token_dict = {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
    return token_dict
