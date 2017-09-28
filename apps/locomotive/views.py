from rest_framework.views import APIView
from rest_framework.response import Response

from apps.common.serializers import WifSerializer
from apps.auth_api.models import BlockChain, UserBlockChain
from apps.locomotive.models import LocoMember


class LocoView(APIView):
    def _member_exists(self, request):
        return LocoMember.objects.filter(
            user_blockchain__blockchain=BlockChain.current(),
            user_blockchain__user=request.user
        ).exists()

    def get(self, request):
        """ Статус, добавлен ли ключ """
        return Response(self._member_exists(request))

    def post(self, request):
        if self._member_exists(request):
            return Response('Already exists')

        slz = WifSerializer(data=request.data)
        slz.is_valid(raise_exception=True)

        wif = slz.validated_data['wif']

        user_bc = UserBlockChain.on_bc.get(user=request.user)

        LocoMember.objects.create(
            user_blockchain=user_bc,
            wif=wif
        )

        return Response('OK')

    def delete(self, request):
        if not self._member_exists(request):
            return Response('not exists')

        ins = LocoMember.objects.get(
            user_blockchain__blockchain=BlockChain.current(),
            user_blockchain__user=request.user
        )

        ins.delete()

        return Response('OK')
