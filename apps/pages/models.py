from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from mptt.models import MPTTModel, TreeForeignKey

from backend import settings
from apps.auth_api.models import User, BlockChain, UserBlockChain

STATUS_CHOICES = (
    (0, u'Ошибка публикации'),
    (1, u'Публикуется'),
    (2, u'Опубликовано')
)


class MasterTag(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'Тэг дерева',
                            db_index=True)
    name = models.CharField(max_length=100, unique=False)
    description = models.CharField(max_length=1024, default='', unique=False)

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class Image(models.Model):
    file = models.ImageField()


class PageOnBlockchainManager(models.GeoManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            blockchain__locale=settings.LOCALE
        )


class Page(models.Model):
    # TODO Добавить норальный geoField с названием места
    title = models.CharField(max_length=1000)
    updated_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(null=True)
    author = models.ForeignKey(User, related_name='pages')

    permlink = models.SlugField(max_length=255, null=True)
    body = models.TextField()

    total_payout_value = models.FloatField(blank=True, null=True)
    total_pending_payout_value = models.FloatField(blank=True, null=True)

    tags = models.ManyToManyField(Tag, blank=True)
    master_tag = models.ForeignKey(MasterTag, null=True)
    blockchain = models.ForeignKey(BlockChain, null=True)

    links = models.CharField(max_length=100000, blank=True, null=True)
    images = models.ManyToManyField(Image, blank=True)
    meta = JSONField(default={})

    voters = models.ManyToManyField(User, related_name='pages_vote', blank=True)

    status = models.IntegerField(default=0, choices=STATUS_CHOICES)

    # TODO Сделать нормальный PointField
    position = models.PointField(srid=4326, blank=True, null=True)
    position_text = models.CharField(max_length=1000)

    has_point = models.BooleanField(default=False)

    objects = models.GeoManager()
    on_bc = PageOnBlockchainManager()

    class Meta:
        app_label = 'pages'
        unique_together = (('author', 'permlink'), )

    def __str__(self):
        return self.title

    @property
    def payout(self):
        return self.total_pending_payout_value + self.total_payout_value

    @property
    def blockchain_author(self):
        return UserBlockChain.on_bc.get(user=self).username


class Comment(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    page = models.ForeignKey(Page, related_name='comments')
    permlink = models.CharField(max_length=512, null=True, blank=True)
    author = models.ForeignKey(User)
    voters = models.ManyToManyField(User, related_name='voters', blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(default=1, choices=STATUS_CHOICES)
    body = models.TextField(null=True)

    class Meta:
        unique_together = (('author', 'permlink'), )

    def __str__(self):
        return '%s - %s' % (self.author, self.body)

    @property
    def blockchain_author(self):
        return UserBlockChain.objects.get(
            user=self.author,
            blockchain=self.page.blockchain).username
