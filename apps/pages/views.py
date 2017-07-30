import os
import uuid
import magic
import logging
import pprint
from pistonapi.exceptions import RPCError
from piston.steem import Steem

import django_filters
from django.db import models as django_models
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, list_route, detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.contrib.gis.geos import Polygon

from apps.pages.permissions import IsOwnerOrReadOnly
from apps.blockchains.sync import BaseUpdater
from apps.pages.models import Page, Comment
from apps.common.storage import Storage
from apps.common.utils import (
        _CustomPageViewSetPagination,
        MultiSerializerViewSetMixin,
)

from apps.pages.serializers import (
    PageSerializer,
    PageListSerializer,
    CommentSerializer,
    CommentTreeSerializer,
    MarkerSerializer,
)


logger = logging.getLogger('mapala')
storage = Storage()


class PageFilter(filters.FilterSet):
    class Meta:
        model = Page
        fields = {
            'created_at': ('lte', 'gte'),
            'author__username': ('exact',),
            'has_point': ('exact',)
        }

    filter_overrides = {
        django_models.DateTimeField: {
            'filter_class': django_filters.IsoDateTimeFilter
        },
    }


class PageViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    queryset = Page.on_bc.all().order_by('-created_at')
    filter_class = PageFilter
    filter_fields = 'author__username', 'has_point', 'created_at'
    lookup_value_regex = '[A-Za-z0-9.@_*-]+'
    pagination_class = _CustomPageViewSetPagination
    permission_classes = IsOwnerOrReadOnly,
    serializer_class = PageSerializer
    serializer_action_classes = {
        'list': PageListSerializer
    }

    def get_object(self):
        # HACK *@* эта штука разделяет юзернейм и пермлинк,
        # для соблюдения уникальности постов
        username, permlink = self.kwargs.get('pk').split('*@*')

        return get_object_or_404(
            self.filter_queryset(self.get_queryset()),
            author__username=username,
            permlink=permlink
        )

    def get_queryset(self):
        qs = self.queryset

        # HACK Так как для JSONField нет поддержки фильтрации
        # реализуем ее сдесть, для тегов
        tag = self.request.GET.get('tag')

        if tag is not None:
            qs = qs.filter(meta__tags__contains=tag)

        return qs

    def create(self, serializer):
        # TODO Зарефатороить или вынести в отдельный модуль
        # методы создания постов и комментариев
        tx = self.request.data.get('tx')
        updater = BaseUpdater(self.request.data.get('blockchain'))

        rpc = Steem(updater.blockchain.wss)

        try:
            r = rpc.broadcast(tx)
        except RPCError as e:
            logger.warning(
                '%s: %s' % (e, pprint.pformat(tx['operations'][0][1]))
            )
            return Response(str(e), status.HTTP_400_BAD_REQUEST)

        operation = r['operations'][0][1]

        p = rpc.get_content({
            'permlink': operation['permlink'],
            'author': operation['author']
        })

        post = updater.upgrade_post(p)

        return Response(self.serializer_action_classes['list'](post).data)

    @detail_route(['get'])
    def comments_tree(self, request, permlink=None):
        comments = self.get_object().comments
        tree = CommentTreeSerializer(comments, many=True).data

        return Response(tree)

    @list_route(permission_classes=[IsAuthenticated], methods=['POST'])
    def update_post(self, request):
        author = request.data.get('author')
        permlink = request.data.get('permlink')

        if not all([author, permlink]):
            return Response('Not author or permlink',
                            status.HTTP_400_BAD_REQUEST)

        updater = BaseUpdater('golos')
        updated_post = updater.update_post(author, permlink)

        return Response(self.serializer_class(updated_post).data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = IsOwnerOrReadOnly,
    filter_fields = 'page',

    def create(self, serializer):
        tx = self.request.data.get('tx')
        updater = BaseUpdater(self.request.data.get('blockchain'))

        rpc = Steem(updater.blockchain.wss)

        try:
            r = rpc.broadcast(tx)
        except RPCError as e:
            logger.warning(
                '%s: %s' % (e, pprint.pformat(tx['operations'][0][1]))
            )
            return Response(str(e), status.HTTP_400_BAD_REQUEST)

        operation = r['operations'][0][1]

        comm = rpc.get_content({
            'permlink': operation['permlink'],
            'author': operation['author']
        })

        page = None

        author = updater.get_author(comm.parent_author)

        if Page.objects.filter(permlink=comm.parent_permlink).exists():
            # Если это коммект к посту
            page = Page.objects.get(
                author=author,
                permlink=comm.parent_permlink
            )
        else:
            parent_comm = Comment.objects.get(
                author=author,
                permlink=comm.parent_permlink
            )

        if page is not None:
            comment = updater.get_comment_ins(comm, page, parent=None)
        else:
            comment = updater.get_comment_ins(
                comm,
                parent_comm.page,
                parent=parent_comm
            )

        comment.save()

        return Response(self.serializer_class(comment).data)


# TODO Вынести абстрактную логику
@api_view(['POST'])
def post_image(request):
    """
    Compress and save image
    """
    file = request.FILES.get('file')

    if file is None:
        return Response('No data for upload', status.HTTP_400_BAD_REQUEST)

    content_type = magic.from_buffer(file.read(), mime=True)
    file.seek(0)

    if 'image' not in content_type:
        return Response('Only images accepted', status.HTTP_400_BAD_REQUEST)

    container = 'posts'
    ext = file.name.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)

    storage.put_object(
        container,
        filename,
        contents=file.read(),
        content_type=content_type
    )

    # TODO Реализовать url картинки на уровне Storage класса
    image_url = os.path.join(storage.storage_url, container, filename)

    return Response(image_url)


class MarkerViewSetPagination(PageNumberPagination):
    """
    Изменены ссылка на страницы, на номера страниц
    """
    page_size = 100


class MarkerViewSet(viewsets.ModelViewSet):
    queryset = Page.on_bc.filter(has_point=True)
    serializer_class = MarkerSerializer
    filter_fields = 'author__username',
    pagination_class = MarkerViewSetPagination

    def get_queryset(self):
        qs = self.queryset

        bbox = self.request.GET.get('bbox')

        if bbox is not None:
            box = bbox.split(',')

            if len(box) != 4:
                return Response('Invalid bbox', status.HTTP_400_BAD_REQUEST)

            geom = Polygon.from_bbox(box)
            qs = qs.filter(position__within=geom)

        return qs
