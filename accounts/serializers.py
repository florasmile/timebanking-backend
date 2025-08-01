from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate

class EmailAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        user = authenticate(
            username=attrs['email'],
            password=attrs['password']
        )
        if not user:
            raise serializers.ValidationError('Invalid email/password')
        attrs['user'] = user
        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2', 'bio', 'skills', 'interests', 'street', 'city', 'state', 'zip_code', 'avatar')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'bio',
            'skills',
            'interests',
            'street',
            'city',
            'state',
            'zip_code',
            'time_credits',
            'avatar',
        )
        read_only_fields = ('email', 'time_credits')

    def to_representation(self, instance):
        """Override to ensure avatar returns full URL"""
        representation = super().to_representation(instance)
        if instance.avatar:
            representation['avatar'] = instance.avatar.url
        else:
            representation['avatar'] = None
        return representation

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])