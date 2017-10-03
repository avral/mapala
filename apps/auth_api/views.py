import io
import logging
import requests
from PIL import Image, ImageOps

from piston.exceptions import AccountExistsException
from pistonbase.account import PasswordKey
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from pistonbase.account import PrivateKey
from piston.steem import Steem

from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError
from rest_framework.decorators import (
    list_route,
    detail_route,
    permission_classes,
    api_view
)

from backend import settings
from apps.common.golos import Golos
from apps.common.utils import is_eng, get_client_ip
from apps.common.mixins import ReCapchaMixin
from apps.blockchains.data_bases import BlockChainDB
from apps.pages.models import Page, Comment
from apps.auth_api.permissions import IsOwnerOrReadOnly, IsOwnerBlockchainOrReadOnly
from apps.auth_api.models import User, BlockChain, UserBlockChain, EmaliRequest
from apps.auth_api.utils import jwt_response_by_user
from apps.auth_api.serializers import (
    UserSerializer,
    BlockChainSerializer,
    UserBlockChainSerializer,
    UserRegiserSerializer,
    ExistUserRegiserSerializer,
)


logger = logging.getLogger('mapala')


class EmaliRequestView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        # Валидация рекапчи
        slz = ReCapchaMixin(data=request.data)
        slz.is_valid(raise_exception=True)

        try:
            EmaliRequest.objects.create(
                email=request.data.get('email_request')
            )
        except IntegrityError:
            return Response('Email already exists', status.HTTP_400_BAD_REQUEST)

        return Response('OK')


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

            db = BlockChainDB()
            pubkey = PrivateKey(wif).pubkey
            username = db.get_user_by_posting_key(pubkey).lower()
        except (ValueError, AssertionError, AttributeError):
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
    serializer_class = UserBlockChainSerializer
    permission_classes = IsOwnerBlockchainOrReadOnly,

    def get_queryset(self, request):
        qs = UserBlockChain.on_bc.all()

        return qs

    def create(self, request):
        """
        Блокчейна привязывается к аккаунту только один раз.
        Отвязать блокчейн от аккаунта или привязать к другому невозможно.
        """
        # TODO Поменять логику работы с поспами и их авторами.(ТЗ v2)
        wif = request.data.get('wif', '<non_valid>')

        try:
            # HACK не валидируем юзера в бч тк не исправили баг на голосе
            #   rpc = BaseUpdater('golos').rpc
            #   username = rpc.wallet.getAccountFromPrivateKey(wif).lower()
            # except (ValueError, AssertionError, AttributeError):

            db = BlockChainDB()
            pubkey = PrivateKey(wif).pubkey
            username = db.get_user_by_posting_key(pubkey).lower()
        except (ValueError, AssertionError, AttributeError):
            raise ValidationError('Invalid posting key')

        bc_by_user = UserBlockChain.on_bc.filter(user=request.user).first()

        if bc_by_user is not None:
            if username != bc_by_user.username:
                return Response(
                    'You already have account: %s, set key for it' %
                    bc_by_user.username, status.HTTP_400_BAD_REQUEST
                )

            return Response(self.serializer_class(bc_by_user).data)

        user_bc = UserBlockChain.on_bc.filter(username=username).first()

        if user_bc is not None:
            user = user_bc.user

            # тут проверка на uncativated
            if user != request.user:
                if '_unactivated' in user.username:
                    # TODO Удалять промежуточных юзеров
                    # Меняем автора с промежуточного юзера на текущего.
                    Page.objects.filter(author=user_bc.user).update(author=request.user)
                    Comment.objects.filter(author=user_bc.user).update(author=request.user)

                    user_bc.user = request.user
                    user_bc.save()
                    return Response(self.serializer_class(bc_by_user).data)
                else:
                    return Response(
                        'user with this key exists: %s' % user.username,
                        status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(self.serializer_class(user_bc).data)

        user_bc = UserBlockChain.objects.create(
            user=request.user,
            username=username,
            blockchain=BlockChain.current()
        )

        return Response(self.serializer_class(user_bc).data)


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    if settings.LOCALE == 'en':
        # Регистрируем юзера в блокчейне, пока GOLOS
        raise ValueError('Registration for existing steemit accounts only')

    slz = UserRegiserSerializer(data=request.data)

    if slz.is_valid(raise_exception=True):
        password = slz.validated_data['password']
        bc_username = slz.validated_data['bc_username']

        golos = Golos(
            BlockChain.current().wss,
            keys=[settings.REGISTRAR['wif']]
        )

        try:
            golos.create_account(
                bc_username,
                password=password,
                creator=settings.REGISTRAR['name'],
                storekeys=False,
            )['operations'][0][1]
        except Exception as e:
            logger.exception('Ошибка создания юзера golos')
            return Response('Invalid blockchain username',
                            status=status.HTTP_400_BAD_REQUEST)

        logger.info('Registration {} from {}'.format(
                slz.validated_data['username'], get_client_ip(request)))

        user = User.objects.create_user(
            username=slz.validated_data['username'],
            number=slz.validated_data['password'],
            password=password
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
        result['posting_key'] = str(
            PasswordKey(bc_username, password, role="posting").get_private()
        )
        return Response(result)


@api_view(['POST'])
@permission_classes((AllowAny,))
def register_existing_user(request):
    slz = ExistUserRegiserSerializer(data=request.data)

    if slz.is_valid():
        db = BlockChainDB()

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
                blockchain=BlockChain.current()
            )

        # Хук для создания юзера на альфе
        requests.get(
            'http://alfa.mapala.net/api/v1/site/create_user?user=%s'
            % mapala_username)

        logger.info('Registration {} from {}'
                    .format(username, get_client_ip(request)))

        return Response(jwt_response_by_user(user))
    else:
        return Response(slz._errors, status=status.HTTP_400_BAD_REQUEST)
