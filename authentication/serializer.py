"""
this file used serialized a data for authentication
"""
from rest_framework import serializers

from common.views import get_token
from .models import User


class RegisterSerializer(serializers.Serializer):
    """
    serializer for signup user
    """
    username = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    first_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    last_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    password = serializers.CharField(
        required=True, allow_blank=False, allow_null=False, max_length=20, min_length=8
    )
    token = serializers.SerializerMethodField()

    @staticmethod
    def validate_email(email):
        """
        validate email
        """
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Email Already exists:'})
        return email

    @staticmethod
    def validate_password(value):
        """
        validate password
        """
        if len(value) < 5:
            raise serializers.ValidationError({'error': 'Password is too short!'})
        return value

    def to_representation(self, obj):
        attr = super().to_representation(obj)
        if 'password' in attr:
            attr.pop('password')
        return attr

    def create(self, validated_data):
        password = validated_data['password']
        instance = User.objects.create(**validated_data)
        instance.set_password(password)
        return instance

    @staticmethod
    def get_token(obj):
        """
        generate an access token
        """
        token = get_token(obj)
        return token

    class Meta:
        """
        class meta for signup
        """
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'token')


class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer class for Login
    """
    token = serializers.SerializerMethodField()
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=True)

    @staticmethod
    def validate_email(email):
        """
        validate email
        """
        email = email.lower()
        if not User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError({'error': 'Email not exists'})
        return email

    def validate(self, attrs):
        """
        validate password
        :param attrs:
        :return:
        """
        password = self.initial_data.get('password')
        email = self.initial_data.get('email')
        user_obj = User.objects.filter(email__iexact=email).first()
        if not user_obj.check_password(password):
            raise serializers.ValidationError({'error': 'Invalid Password'})
        attrs.update({'user': user_obj})
        return attrs

    @staticmethod
    def get_token(obj):
        """
        generate an access token
        """
        token = get_token(obj['user'])
        return token

    class Meta:
        """
        class Meta for User
        """
        model = User
        fields = ('id', 'email', 'token', 'password')


class UserSerializer(serializers.ModelSerializer):
    """
    get a details of user
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',)