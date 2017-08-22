import logging

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view

from apps.auth.serializers import (
    SignedRequestSerializer,
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
