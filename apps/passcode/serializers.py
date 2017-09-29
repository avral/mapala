from datetime import datetime, timedelta

from rest_framework import serializers

from apps.passcode.models import PassRequest


class PassRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassRequest
        fields = 'id', 'number'


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
