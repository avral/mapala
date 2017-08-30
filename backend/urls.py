import re
import django
import logging
import requests

from django.views.decorators.cache import cache_page
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include
from django.http import HttpResponse

from robot_detection import is_robot
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from backend.settings import PRERENDER_PROXY, PRERENDER_UA_REGEX
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


def ssr(request):
    """ HACK Рендерим страничку для робота """
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    if re.search(PRERENDER_UA_REGEX, user_agent, re.I) and user_agent:
        url = PRERENDER_PROXY + request.build_absolute_uri()

        try:
            html = requests.get(url, allow_redirects=False).text
        except requests.exceptions.ConnectionError:
            logger.warning('Prerender connection err: %s' % url)
            return HttpResponse(status=500)
    else:
        html = render_to_string('base.html')

    return HttpResponse(html)


def alfa(request):
    alfa_url = 'http://alfa.mapala.net' + request.get_full_path()

    r = requests.get(alfa_url.replace('https', 'http'))
    return HttpResponse(r.content, content_type=r.headers['content-type'])


urlpatterns += [
    url(r'^admin/', admin.site.urls),

    # DACom Auth
    url(r'^auth/', include(auth_urls)),

    url(r'^api-auth/', obtain_jwt_token),
    url(r'^api-auth-refresh/', refresh_jwt_token),

    # TODO Вынести в ресурс картинок
    url(r'^post_image/', page_views.post_image),

    url(r'^api/v1/', alfa),

    url(r'^sign-up/', auth_views.register),
    url(r'^existng-sign-up/', auth_views.register_existing_user),
    url(r'^api/', include(router.urls)),

    # Паравозик
    url(r'^api/locomotive/', LocoView.as_view()),

    # Vue on frontend
    # url(r'^', TemplateView.as_view(template_name='base.html'))
    url(r'^', ssr)
]
