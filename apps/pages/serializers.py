from lxml.html import document_fromstring

from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from drf_extra_fields.geo_fields import PointField

from apps.pages.models import Page, Image, MasterTag, Comment, Tag
from apps.auth_api.serializers import ShortUserSerializer


class CommentTreeSerializer(serializers.HyperlinkedModelSerializer):
    # TODO Стал ненужным
    children = RecursiveField(source='children.all', many=True, read_only=True)
    author_avatar = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = 'id', 'body', 'children', 'author_avatar', 'author'

    def get_author_avatar(self, obj):
        return obj.author.avatar_url

    def get_author(self, obj):
        return obj.author.username


class ImageSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        exclude = 'file',

    def get_name(self, obj):
        return obj.file.name.split('/')[-1]

    def get_url(self, obj):
        return obj.file.url


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class MasterTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterTag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)
    parent_author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username

    def get_parent_author(self, obj):
        return obj.parent.author.bc_username if obj.parent else None

    class Meta:
        model = Comment
        fields = '__all__'


class PageBaseSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    position = PointField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = '__all__'

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_comments(self, obj):
        qs = obj.comments.order_by('created_at').reverse()[:3][::-1]

        return CommentSerializer(qs, many=True).data


class PageListSerializer(PageBaseSerializer):
    body = serializers.SerializerMethodField()
    miniature = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = (
            'id', 'author', 'comments', 'position', 'position_text',
            'comments_count', 'title', 'created_at', 'permlink', 'body',
            'miniature', 'payout'
        )

    def get_body(self, obj):
        dom = document_fromstring(obj.body)

        return dom.text_content()[:100].rsplit(' ', 1)[0]

    def get_miniature(self, obj):
        try:
            xhtml = document_fromstring(obj.body)
            images = xhtml.xpath('//img[1]/@src')
        except:
            return None

        return images[0] if images else None


class PageSerializer(PageBaseSerializer):
    next_page = serializers.SerializerMethodField()
    prev_page = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = (
            'id', 'author', 'comments', 'created_at', 'permlink', 'body',
            'payout', 'comments_count', 'position', 'position_text', 'title',
            'prev_page', 'next_page', 'meta'
        )

    def get_next_page(self, obj):
        return Page.objects.filter(
            author=obj.author,
            created_at__gt=obj.created_at
        ).values('author__username', 'permlink').first()

    def get_prev_page(self, obj):
        return Page.objects.filter(
            author=obj.author,
            created_at__lt=obj.created_at
        ).values('author__username', 'permlink').last()


class MarkerSerializer(PageListSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = 'author', 'position', 'body', 'permlink', 'title'

    def get_author(self, obj):
        return obj.author.username
