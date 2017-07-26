import logging

from bitshares.bitshares import BitShares, Account
from bitshares.exceptions import AccountDoesNotExistsException

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view

from backend.settings import DACOM_NODE_WSS, REGISTRAR, REFERRER
from apps.auth.serializers import (
    SignedRequestSerializer,
    SignDacomAccSerialzer
)


logger = logging.getLogger('dacom')


@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    slz = SignedRequestSerializer(
        data=request.data,
        context={'request': request}
    )

    if slz.is_valid(raise_exception=True):
        # Подпись валидная
        return Response({'all': 'ok'})
    return Response({'valid': 'fail'})


@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    slz = SignDacomAccSerialzer(
        data=request.data,
        context={'request': request}
    )

    slz.is_valid(raise_exception=True)

    bitshares = BitShares(
        DACOM_NODE_WSS,
        keys=[REGISTRAR['wif']]
    )

    try:
        Account(slz.validated_data['account'], bitshares_instance=bitshares)
        return Response('Account already exists', status.HTTP_400_BAD_REQUEST)
    except:
        pass

    registrar = Account(REGISTRAR['name'], bitshares_instance=bitshares)
    try:
        referrer = Account(REFERRER['name'], bitshares_instance=bitshares)
    except AccountDoesNotExistsException:
        return Response('Unknown referrer', status.HTTP_400_BAD_REQUEST)

    referrer_percent = REFERRER['present']

    try:
        bitshares.create_account(
            slz.validated_data['account'],
            registrar=registrar['id'],
            referrer=referrer['id'],
            referrer_percent=referrer_percent,
            owner_key=slz.validated_data['owner_key'],
            active_key=slz.validated_data['active_key'],
            memo_key=slz.validated_data['memo_key'],
            # proxy_account=config.get("proxy", None),
            # additional_owner_accounts=config.get("additional_owner_accounts", []),
            # additional_active_accounts=config.get("additional_active_accounts", []),
            # additional_owner_keys=config.get("additional_owner_keys", []),
            # additional_active_keys=config.get("additional_active_keys", []),
        )
    except Exception as e:
        logger.exception('Ошибка создания пользователя')
        return Response(e, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        "account": {
            "name": slz.validated_data['account'],
            "owner_key": slz.validated_data["owner_key"],
            "active_key": slz.validated_data["active_key"],
            "memo_key": slz.validated_data["memo_key"],
            "referrer": referrer["name"]
        }
    })
