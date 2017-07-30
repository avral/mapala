import io
import json
import logging
import requests
from PIL import Image, ImageOps

from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from pistonbase.account import PrivateKey

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError
from rest_framework.decorators import (
    list_route,
    detail_route,
    permission_classes,
    api_view
)

from backend.settings import BITSHARES_PASS, FRONTEND_APP_NAME
from apps.common.utils import is_eng
from apps.blockchains.sync import BaseUpdater
from apps.blockchains.data_bases import BlockChainDB
from apps.blockchains.api import Api
from apps.auth_api.permissions import IsOwnerOrReadOnly, IsOwnerBlockchainOrReadOnly
from apps.auth_api.models import User, BlockChain, UserBlockChain
from apps.auth_api.utils import jwt_response_by_user
from apps.auth_api.serializers import (
    UserSerializer,
    BlockChainSerializer,
    UserBlockChainSerializer,
    UserRegiserSerializer,
    ExistUserRegiserSerializer
)


logger = logging.getLogger('mapala')


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    lookup_value_regex = '[A-Za-z0-9.@_*-]+'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = IsOwnerOrReadOnly,
    filter_fields = 'username',

    @list_route()
    def current(self, request):
        return Response(self.serializer_class(request.user).data)

    @list_route(permission_classes=[AllowAny], methods=['POST'])
    def reset_password(self, request):
        password = request.data.get('password')
        wif = request.data.get('wif')

        try:
            # HACK Пока приходится чекать в базе тк. нет фикса от голоса
            # rpc = BaseUpdater('golos').rpc
            # username = rpc.wallet.getAccountFromPrivateKey(wif)

            db = BlockChainDB('golos')
            pubkey = PrivateKey(wif).pubkey
            username = db.get_user_by_posting_key(pubkey).lower()
        except ValueError:
            raise ValidationError('Невалидный постинг ключ')

        try:
            user = UserBlockChain.on_bc.get(username=username).user
        except ObjectDoesNotExist:
            raise ValidationError('Пользователь не зарегистрирован')

        if '_unactivated' in user.username:
            raise ValidationError('Пользователь не зарегистрирован')

        user.set_password(password)
        user.save()

        return Response(user.username)

    @list_route(methods=['POST'])
    def set_password(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not request.user.check_password(old_password):
            raise ValidationError('Wrong old password.')

        if not is_eng(old_password) or not is_eng(new_password):
            raise ValidationError('Password can contains only eng symbols')

        request.user.set_password(new_password)
        request.user.save()

        return Response(new_password)

    @detail_route(methods=['POST'])
    def set_avatar(self, request, username=None):
        obj = self.get_object()

        file = request.FILES.get('file')
        size = (120, 120)

        b_image = io.BytesIO()
        img = Image.open(file)
        img = ImageOps.fit(img, size, Image.ANTIALIAS)
        img.save(b_image, format='PNG')

        obj.avatar.save(str(file), ContentFile(b_image.getvalue()))

        return Response(obj.avatar.url)

    @detail_route(methods=['POST'])
    def remove_avatar(self, request, username):
        obj = self.get_object()

        obj.avatar = None
        obj.save()

        return Response(obj.avatar_url)

    @detail_route(methods=['GET'])
    def initial_blockchains(self, request, username):
        """
        Метод возвращает все подключенные к проекту блокчейны,
        блокчейн хранит username пользователя если пользователь
        активировал постинг-ключ для блокчейна.
        """
        user = self.get_object()

        result = []

        for blockchain in BlockChain.objects.all():
            data = BlockChainSerializer(blockchain).data

            user_blockchain = UserBlockChain.objects.filter(
                blockchain=blockchain, user=user
            ).first()

            data['activated'] = False if user_blockchain is None else True

            if user_blockchain is not None:
                data['blockchain_username'] = user_blockchain.username

            result.append(data)

        return Response(result)


class BlockChainViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlockChain.objects.all()
    serializer_class = BlockChainSerializer


class UserBlockChainViewSet(viewsets.ModelViewSet):
    queryset = UserBlockChain.on_bc.all()
    serializer_class = UserBlockChainSerializer
    permission_classes = IsOwnerBlockchainOrReadOnly,

    def create(self, request):
        wif = request.data.get('wif', '<non_valid>')
        blockchain = request.data.get('blockchain')
        blockchain = BlockChain.objects.get(name=blockchain)

        try:
            # HACK не валидируем юзера в бч тк не исправили баг на голосе
            #   rpc = BaseUpdater('golos').rpc
            #   username = rpc.wallet.getAccountFromPrivateKey(wif).lower()
            # except (ValueError, AssertionError, AttributeError):

            db = BlockChainDB('golos')
            pubkey = PrivateKey(wif).pubkey
            username = db.get_user_by_posting_key(pubkey).lower()
        except (ValueError, AssertionError, AttributeError):
            raise ValidationError('Невалидный постинг ключ')

        existing_user_bc = self.queryset.filter(username=username).first()

        if existing_user_bc is not None:
            user = existing_user_bc.user

            if user != request.user:
                return Response('user with this key exists: %s'
                                % user.username, status.HTTP_400_BAD_REQUEST)

        ins, _ = self.queryset.update_or_create(
            user=request.user,
            blockchain=blockchain,
            defaults={'username': username}
        )

        return Response(self.serializer_class(ins).data)


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    slz = UserRegiserSerializer(data=request.data)

    if slz.is_valid():
        password = slz.validated_data['password']
        bc_username = slz.validated_data['bc_username'].lower()

        # Регистрируем юзера в блокчейне, пока GOLOS
        api = Api('http://144.217.94.119:8093')
        api('unlock', BITSHARES_PASS)

        if api.user_exists(bc_username):
            raise ValidationError('Username exist in blockchain')

        keys = {role: api(
                'get_private_key_from_password',
                bc_username, role, password)['result']
                for role in ['owner', 'active', 'posting', 'memo']}

        new_user = api(
            'create_account_with_keys',
            'mapala',
            bc_username,
            json.dumps({'app': FRONTEND_APP_NAME}),
            keys['owner'][0],
            keys['active'][0],
            keys['posting'][0],
            keys['memo'][0],
            True
        )

        if 'error' in new_user:
            return Response('Invalid blockchain username',
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=slz.validated_data['username'],
            password=password,
        )

        # Хук для создания юзера на альфе
        requests.get(
            'http://alfa.mapala.net/api/v1/site/create_user?user=%s'
            % slz.validated_data['username'])

        UserBlockChain.objects.create(
            user=user,
            username=bc_username,
            blockchain=BlockChain.objects.get(name='golos')
        )

        result = jwt_response_by_user(user)

        # Возвращаем постинг ключ при успешной регистрации
        result['posting_key'] = keys['posting'][1]

        return Response(result)
    else:
        return Response(slz._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def register_existing_user(request):
    slz = ExistUserRegiserSerializer(data=request.data)

    if slz.is_valid():
        db = BlockChainDB('golos')

        wif = slz.validated_data['wif']
        mapala_username = slz.validated_data['username']

        username = db.get_user_by_posting_key(PrivateKey(wif).pubkey)

        if username is None:
            return Response('User with this key not exists',
                            status.HTTP_404_NOT_FOUND)

        existng_bc = UserBlockChain.on_bc.filter(
            username=username
        )

        if existng_bc.exists():
            user = existng_bc.first().user

            if '_unactivated' in user.username:
                user.username = mapala_username
                user.set_password(request.data.get('password'))
                user.save()
            else:
                return Response('Mapala user with this key already exists: %s'
                                % user.username, status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create_user(
                username=mapala_username,
                password=request.data.get('password')
            )

            UserBlockChain.objects.create(
                username=username,
                user=user,
                # FIXME Реагет только под голос
                blockchain=BlockChain.objects.get(name='golos')
            )

        # Хук для создания юзера на альфе
        requests.get(
            'http://alfa.mapala.net/api/v1/site/create_user?user=%s'
            % mapala_username)

        return Response(jwt_response_by_user(user))
    else:
        return Response(slz._errors, status=status.HTTP_400_BAD_REQUEST)
