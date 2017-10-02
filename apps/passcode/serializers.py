from datetime import datetime, timedelta

from rest_framework import serializers

from apps.auth_api.models import User
from apps.passcode.models import PassRequest


class PassRequestSerializer(serializers.ModelSerializer):
    number = serializers.CharField()

    class Meta:
        model = PassRequest
        fields = 'id', 'number'

    def validate_number(self, data):
        if User.objects.filter(number=data).exists():
            raise serializers.ValidationError(
                'User with this phone already exists: %s' %
                User.objects.get(number=data).username)

        # Отправить код можно только раз в 5 минут.
        active_time = datetime.now() - timedelta(minutes=5)

        if PassRequest.objects.filter(
                number=data,
                created_at__gt=active_time):

            raise serializers.ValidationError('SMS can be sent in 5 minutes')

        return data


class PassRequestValidateSerializer(serializers.Serializer):
    number = serializers.CharField()
    passcode = serializers.CharField()

    def validate(self, data):
        # Код активен в течении двух минут
        active_time = datetime.now() - timedelta(minutes=2)

        if not PassRequest.objects.filter(
            number=data['number'],
            code=data['passcode'],
            created_at__gt=active_time
        ).exists():
            raise serializers.ValidationError('Wrong sms code')
        else:
            return data
