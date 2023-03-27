import re
from django.contrib.auth import get_user_model, authenticate
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers, exceptions
from rest_framework.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainSerializer, PasswordField
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class CustomUserSerializer(UserCreateSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=150, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')

    def validate_username(self, username):
        if not re.match(r'^[a-zA-Z0-9-_]+$', username):
            raise serializers.ValidationError('Недопустимые символы username.')

        return username


class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = User.EMAIL_FIELD

