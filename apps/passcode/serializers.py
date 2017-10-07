from datetime import datetime, timedelta

from phonenumbers import parse, format_number, PhoneNumberFormat
from rest_framework import serializers

from apps.common.mixins import ReCapchaMixin
from apps.auth_api.models import User
from apps.passcode.models import PassRequest


class PassRequestSerializer(ReCapchaMixin, serializers.ModelSerializer):
    number = serializers.CharField()

    class Meta:
        model = PassRequest
        fields = 'id', 'number', 'g_recaptcha_response'

    def validate_number(self, number):
        number = format_number(parse(number), PhoneNumberFormat.E164)

        if User.objects.filter(number=number).exists():
            raise serializers.ValidationError(
                'User with this phone already exists: %s' %
                User.objects.get(number=number).username)

        # Отправить код можно только раз в 5 минут.
        active_time = datetime.now() - timedelta(minutes=5)

        if PassRequest.objects.filter(
                number=number,
                created_at__gt=active_time):

            raise serializers.ValidationError('SMS can be sent in 5 minutes')

        return number


class PassRequestValidateSerializer(serializers.Serializer):
    number = serializers.CharField()
    passcode = serializers.CharField()

    def validate(self, data):
        # Код активен в течении четырех минут
        active_time = datetime.now() - timedelta(minutes=4)

        if not PassRequest.objects.filter(
            number=data['number'],
            code=data['passcode'],
            created_at__gt=active_time
        ).exists():
            raise serializers.ValidationError('Wrong sms code')
        else:
            return data
