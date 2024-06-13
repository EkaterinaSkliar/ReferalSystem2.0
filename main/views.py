from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import User
from main.serializers import UserSerializer, InviteCodeSerializer, PhoneNumberOnlySerializer


class GetUserProfile(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        queryset_invited = User.objects.filter(inviter=user)
        serializer_for_queryset_invited = PhoneNumberOnlySerializer(instance=queryset_invited, many=True, )
        return Response(
            {
                'user_info': serializer.data,
                'invited_users': serializer_for_queryset_invited.data
            })

    def post(self, request):
        user = request.user
        serializer = InviteCodeSerializer(user, request.data)
        serializer.is_valid(raise_exception=True)
        invite_code = serializer.validated_data.get("invite_code")

        if user.invite_code == invite_code:
            return Response({'message': 'Введите чужой инвайт-код'}, status=404)
        try:
            user_inviter = User.objects.get(invite_code=invite_code)
        except ObjectDoesNotExist:
            return Response({'message': 'Пользователь с таким инвайт-кодом не найден'}, status=404)
        user.inviter = user_inviter
        user.save()
        queryset_invited = User.objects.filter(inviter=user)
        serializer_for_queryset_invited = UserSerializer(instance=queryset_invited, many=True)
        return Response(serializer_for_queryset_invited.data, status=201)
