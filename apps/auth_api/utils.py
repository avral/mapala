from steembase.account import PrivateKey

from rest_framework_jwt.settings import api_settings


def check_steam_key(key):
    try:
        PrivateKey(key).pubkey
    except (ValueError, AssertionError):
        return False

    return True


def jwt_response_payload_handler(token, user=None, request=None):
    from apps.auth_api.serializers import UserSerializer

    return {'token': token, 'user': UserSerializer(user).data}


def jwt_response_by_user(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    return jwt_response_payload_handler(token, user)
