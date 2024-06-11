from rest_framework import serializers

from .models import User, SmsCode


class UserSerializer(serializers.ModelSerializer):
    password = serializers.HiddenField(default=None)

    class Meta:
        model = User
        fields = ['phone_number', 'password']


class SmsCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsCode
        fields = ['phone_number', 'code']
