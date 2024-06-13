from rest_framework import serializers

from .models import User, SmsCode


class UserSerializer(serializers.ModelSerializer):
    password = serializers.HiddenField(default=None)
    inviter = serializers.ReadOnlyField(source="inviter.invite_code")

    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'inviter', 'password']

    # def generate_invite_code(self):
    #     invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class PhoneNumberOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']


class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6, required=True)


class SmsCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsCode
        fields = ['phone_number', 'code']
