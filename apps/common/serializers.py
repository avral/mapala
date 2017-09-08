from pistonbase.account import PrivateKey

from rest_framework import serializers


class WifSerializer(serializers.Serializer):
    wif = serializers.CharField()

    def validate_wif(self, data):
        try:
            PrivateKey(data).pubkey
        except (ValueError, AssertionError):
            raise serializers.ValidationError('Невалидный постинг ключ')

        return data
