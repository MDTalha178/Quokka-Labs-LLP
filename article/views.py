"""
In this file write a code for authentication part
"""
# Local import
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from article.models import Article
from article.serializer import AddArticleSerializer, GetDetailArticleSerializer, EditArticleSerializer
from common.utils import custom_response, custom_error_response
from common.views import ModelViewSet


class ArticleViewSet(ModelViewSet):
    """
    This class is used give functionality user can able perform operation all type of request on
    article
    """
    http_method_names = ('post', 'get', 'put', 'delete',)
    permission_classes = (IsAuthenticated,)
    serializer_class = AddArticleSerializer
    queryset = Article

    def get_queryset(self):
        """
        get a queryset for article
        :return: queryset
        """
        return self.queryset.objects.select_related('create_by').filter(status=0)

    def list(self, request, *args, **kwargs):
        """
        get a list of article
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = GetDetailArticleSerializer(self.get_queryset(), many=True)
        return custom_response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request, *args, **kwargs):
        """
        create a article
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = self.request.user
        serializer = self.serializer_class(data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return custom_response(detail='Article created successfully!', data=serializer.data)
        return custom_error_response(
            status.HTTP_400_BAD_REQUEST, detail='Something went wrong', data=serializer.errors
        )

    def retrieve(self, request, *args, **kwargs):
        """
        retrieve  an article
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        serializer = GetDetailArticleSerializer(instance)
        return custom_response(status=status.HTTP_200_OK, data=serializer.data)

    def update(self, request, *args, **kwargs):
        """
        update an article
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = EditArticleSerializer(data=request.data, context={'instance':self.get_object(),'user': self.request.user})
        if serializer.is_valid():
            data_obj = serializer.update(self.get_object(), request.data)
            data = GetDetailArticleSerializer(data_obj).data
            return custom_response(status=status.HTTP_200_OK, detail='updated Successfully', data=data)
        return custom_error_response(
            status.HTTP_400_BAD_REQUEST, detail='Something went wrong', data=serializer.errors
        )

    def destroy(self, request, *args, **kwargs):
        """
        delete an article
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        instance.delete()
        return custom_response(status=status.HTTP_200_OK, detail='Article deleted successfully!')
