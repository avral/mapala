from django.contrib.gis.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.staticfiles.templatetags.staticfiles import static

from backend import settings

LOCALE_CHOICES = (
    ('ru', 'Русский'),
    ('en', 'English')
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(**extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True, null=True)
    email = models.EmailField('email address', unique=True, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, max_length=500)
    position = models.PointField(srid=4326, blank=True, null=True)
    locale = models.CharField(max_length=100, choices=LOCALE_CHOICES, default=LOCALE_CHOICES[0][0])

    btc_wallet = models.CharField(max_length=200, null=True)
    btc_wallet_direct = models.CharField(max_length=200, null=True)

    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('manager', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return '{}: {}'.format(self.name, self.email)

    def get_short_name(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def has_avatar(self):
        return True if self.avatar and hasattr(self.avatar, 'url') else False

    @property
    def avatar_url(self):
        return self.avatar.url if self.has_avatar else static('ic-profile.svg')

    @property
    def bc_username(self):
        ubc = UserBlockChain.on_bc.filter(user=self).first()

        return ubc.username if ubc is not None else self.username


class BlockChain(models.Model):
    name = models.CharField(max_length=100, null=True)
    wss = models.CharField(max_length=100, null=True)
    address_prefix = models.CharField(max_length=200, null=True)
    chain_id = models.CharField(max_length=200, null=True)
    locale = models.CharField(max_length=5, choices=LOCALE_CHOICES, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def current(cls):
        """ Return current blockchain by locale """
        return cls.objects.get(locale=settings.LOCALE)


class UserBlockChainOnBlockchainManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            blockchain__locale=settings.LOCALE
        )


class UserBlockChain(models.Model):
    user = models.ForeignKey(User, related_name='blockchains', null=True)
    username = models.CharField(max_length=200, null=True)
    blockchain = models.ForeignKey(BlockChain, null=True)

    objects = models.Manager()
    on_bc = UserBlockChainOnBlockchainManager()

    class Meta:
        unique_together = ('user', 'blockchain'), ('username', 'blockchain')

    def __str__(self):
        return '{}: {}'.format(self.blockchain.name, self.username)
