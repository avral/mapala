from pistonbase.account import PrivateKey

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from apps.common.utils import is_eng
from apps.auth_api.models import User, BlockChain, UserBlockChain


class UserRegiserBaseSerializer(serializers.Serializer):
    username = serializers.RegexField('^[\d\w.-]+$')
    password = serializers.CharField()

    def validate_username(self, data):
        username = data.lower()

        if not is_eng(data):
            raise ValidationError('Username can contains only eng symbols')

        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exist')

        return data


class UserRegiserSerializer(UserRegiserBaseSerializer):
    bc_username = serializers.CharField()


class ExistUserRegiserSerializer(UserRegiserBaseSerializer):
    wif = serializers.CharField()

    def validate_wif(self, data):
        try:
            PrivateKey(data).pubkey
        except ValueError:
            raise serializers.ValidationError('Невалидный постинг ключ')

        return data


class UserSerializer(serializers.ModelSerializer):
    # TODO валидировать юзера на патчинг самого себя
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'locale', 'avatar', 'has_avatar',
            'bc_username'
        )

    def get_avatar(self, obj):
        return obj.avatar_url


class ShortUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = 'id', 'username', 'bc_username', 'avatar'


class BlockChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockChain
        fields = '__all__'


class UserBlockChainSerializer(serializers.ModelSerializer):
    bc_data = serializers.SerializerMethodField()

    class Meta:
        model = UserBlockChain
        fields = '__all__'

    def get_bc_data(self, obj):
        return BlockChainSerializer(obj.blockchain).data
