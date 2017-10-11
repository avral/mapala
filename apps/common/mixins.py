import requests

from rest_framework import serializers

from backend import settings


class ReCapchaMixin(serializers.Serializer):
    g_recaptcha_response = serializers.CharField(write_only=True)

    def validate_g_recaptcha_response(self, res):
        r = requests.post(settings.GR_CAPTCHA_URL, {
            'secret': settings.GR_CAPTCHA_SECRET_KEY,
            'response': res
        })

        if not r.json()['success']:
            raise serializers.ValidationError('invalid capcha')

        return res

    def create(self, validated_data):
        validated_data.pop('g_recaptcha_response')

        return super().create(validated_data)
