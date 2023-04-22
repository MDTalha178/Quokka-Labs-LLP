"""
this file used serialized a data for article
"""
from rest_framework import serializers

from article.models import Article
from authentication.serializer import UserSerializer


class AddArticleSerializer(serializers.ModelSerializer):
    """
    create an Article
    """
    title = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=250)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data):
        """
        create an article
        :param validated_data:
        :return:
        """
        validated_data['create_by_id'] = self.context['user'].id
        obj = Article.objects.create(**validated_data)
        return obj

    class Meta:
        model = Article
        fields = ('id', 'title', 'description')


class GetDetailArticleSerializer(serializers.ModelSerializer):
    """
    get details article serializer
    """
    posted_by = serializers.SerializerMethodField()

    @staticmethod
    def get_posted_by(obj):
        """
        get details posted by
        :param obj:
        :return:
        """
        if obj.create_by:
            return UserSerializer(obj.create_by).data

    class Meta:
        model = Article
        fields = ('id', 'title', 'description', 'posted_by',)


class EditArticleSerializer(serializers.ModelSerializer):
    """
    update article
    """
    title = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=250)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def update(self, instance, validated_data):
        """
        update article
        :param instance:
        :param validated_data:
        :return:
        """
        Article.objects.filter(id=instance.id).update(
            create_by_id=self.context['user'].id,
            title=validated_data['title'], description=validated_data['description']
        )
        obj = Article.objects.get(id=instance.id)
        return obj

    class Meta:
        model = Article
        fields = ('title', 'description')
