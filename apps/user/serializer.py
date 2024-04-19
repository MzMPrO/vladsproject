import random

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework import serializers

from config.settings import EMAIL_HOST_USER
from apps.user.models import User, getKey, setKey


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email',
            "first_name", "last_name",
            'middle_name', 'phone_number',
            'email', 'bio', 'date_of_birth',
            'gender', "password"
        ]

    def validate(self, attrs):
        activate_code = random.randint(100000, 999999)
        user = User(
            first_name=attrs['first_name'],
            last_name=attrs['last_name'],
            middle_name=attrs['middle_name'],
            phone_number=attrs['phone_number'],
            date_of_birth=attrs['date_of_birth'],
            bio=attrs['bio'],
            gender=attrs['gender'],
            email=attrs['email'],
            username=attrs['username'],
            password=make_password(attrs['password']),
            is_active=True,
        )
        setKey(
            key=attrs['email'],
            value={
                "user": user,
                "activate_code": activate_code
            },
            timeout=300
        )
        send_mail(
            subject="Subject here",
            message=f"Your activate code.\n{activate_code}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[attrs['email']],
            fail_silently=False,
        )
        return super().validate(attrs)


class CheckActivationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activate_code = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        data = getKey(key=attrs['email'])
        print(data)
        if data and data['activate_code'] == attrs['activate_code']:
            return attrs
        raise serializers.ValidationError(
            {"error": "Error activate code or email"}
        )


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            "first_name", "last_name",
            'middle_name', 'phone_number',
            'email', 'bio', 'date_of_birth',
            'gender'
        ]
