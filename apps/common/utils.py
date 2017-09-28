import io
import PIL.Image

from alphabet_detector import AlphabetDetector
from django.forms.models import model_to_dict
from django.core.files.base import ContentFile

from rest_framework.pagination import PageNumberPagination
from mptt.templatetags.mptt_tags import cache_tree_children

from apps.pages.models import Image

from backend.settings import (
    COMPRESS_IMAGE_QUALITY,
)


ad = AlphabetDetector()


def is_eng(string):
    return ad.is_latin(string)


def _node_to_dict(node, fields):
    result = model_to_dict(node, fields)

    children = [_node_to_dict(c, fields) for c in node.get_children()]

    if children:
        result['children'] = children

    return result


def make_tree_by_root_nodes(root_nodes, fields=None):
    """
    root_nodes: pодительские элементы
    fields: поля для сериализации
    """
    nodes = cache_tree_children(root_nodes)

    return [_node_to_dict(n, fields=fields) for n in nodes]


class _CustomPageViewSetPagination(PageNumberPagination):
    """
    Изменены ссылка на страницы, на номера страниц
    """
    page_size = 10

    def get_next_link(self):
        if not self.page.has_next():
            return None

        return self.page.next_page_number()

    def get_previous_link(self):
        if not self.page.has_previous():
            return None

        return self.page.previous_page_number()


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        Thanks gonz: http://stackoverflow.com/a/22922156/11440

        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()


def save_image(file, path, quality=None):
    # TODO Не используется
    image = Image.objects.create()
    b_img = io.BytesIO()

    img = PIL.Image.open(io.BytesIO(file.read()))
    img.save(b_img, "JPEG", quality=quality or COMPRESS_IMAGE_QUALITY)
    b_img.seek(0)

    image.file.save(path + str(file), ContentFile(b_img.read()))

    return image


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip
