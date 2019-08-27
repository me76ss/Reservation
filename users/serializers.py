from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers, exceptions


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
