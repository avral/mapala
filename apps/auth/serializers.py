import uuid

from rest_framework import serializers

from apps.auth.utils import AccountDoesNotExist, verify_signature


class SignedRequestSerializer(serializers.Serializer):
    account = serializers.CharField()
    auth_sig = serializers.CharField()

    def validate(self, data):
        request = self.context['request']
        auth_sig_hash = bytearray(request.session.get('authSigHash'), 'utf-8')

        if auth_sig_hash is None:
            # Если это первый запрос и AuthSigHashMiddleware еще не отработал
            raise serializers.ValidationError('Invalid authSigHash')

        try:
            verify_signature(data['account'], auth_sig_hash, data['auth_sig'])

            # Обновляем хеш для подписи
            request.session['authSigHash'] = str(uuid.uuid4())
        except AccountDoesNotExist:
            raise serializers.ValidationError('User not exists')
        except ValueError:
            raise serializers.ValidationError('Invalid AuthSig')

        return data


class SignDacomAccSerialzer(serializers.Serializer):
    # TODO Написать регулярку на юзернейм
    account = serializers.CharField()
    active_key = serializers.CharField()
    memo_key = serializers.CharField()
    owner_key = serializers.CharField()
