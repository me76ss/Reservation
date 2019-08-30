from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator

from .models import UserExtraInfo, UserType


class UserExtraInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtraInfo
        fields = ('id', 'user_type', 'admin_type')


class UserSerializer(serializers.ModelSerializer):
    extra_info = UserExtraInfoSerializer()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'extra_info')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')
        print(username, password)
        if username and password:
            user = authenticate(username=username, password=password)
            print(User.objects.all())
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg = 'User is deactivated.'
                    raise exceptions.ValidationError(msg)
            else:
                msg = 'Unable to login with given credentials.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Must provide both username and password.'
            raise exceptions.ValidationError(msg)
        return data


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        UserExtraInfo.objects.create(
            user_id=user.id,
            user_type=UserType.STUDENT.name
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}
