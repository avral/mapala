import django
import logging
import requests

from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include
from django.http import HttpResponse

from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from apps.locomotive.views import LocoView
from apps.auth import urls as auth_urls
from apps.pages import views as page_views
from apps.groups import views as groups_views
from apps.auth_api import views as auth_views


logger = logging.getLogger('mapala')


router = DefaultRouter()
router.register('pages', page_views.PageViewSet, base_name='pages')
router.register('users', auth_views.UserViewSet)
router.register('comments', page_views.CommentViewSet)
router.register('blockchains', auth_views.BlockChainViewSet)
router.register('user-blockchains', auth_views.UserBlockChainViewSet, base_name='user_blockchains')
router.register('markers', page_views.MarkerViewSet, base_name='markers')
router.register('groups', groups_views.GroupViewSet)


urlpatterns = []

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
    urlpatterns += staticfiles_urlpatterns()

    urlpatterns.append(
        url(r'^media/(?P<path>.*)$', django.views.static.serve, {
            'document_root': settings.MEDIA_ROOT})
    )


def alfa(request):
    alfa_url = 'http://alfa.mapala.net' + request.get_full_path()

    r = requests.get(alfa_url.replace('https', 'http'))
    return HttpResponse(r.content, content_type=r.headers['content-type'])


urlpatterns += [
    url(r'^admin/', admin.site.urls),

    # TODO перенести в модуль авторизации
    url(r'^api/auth/login/', obtain_jwt_token),
    url(r'^api/auth/refresh/', refresh_jwt_token),
    url(r'^api/auth/sign-up/', auth_views.register),
    url(r'^api/auth/existng-sign-up/', auth_views.register_existing_user),
    url(r'^api/email_request/', auth_views.EmaliRequestView.as_view()),

    # TODO Вынести в ресурс картинок
    url(r'^api/images/', page_views.post_image),

    url(r'^api/v1/', alfa),

    url(r'^api/', include(router.urls)),

    # Паравозик
    url(r'^api/locomotive/', LocoView.as_view()),
]
