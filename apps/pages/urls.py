# coding:utf-8
from django.conf.urls import url
from apps.pages.views import page_list, page, page_save, tags_list, post_image
from backend.views import IndexView

urlpatterns = [
    url(r'^api/v1/tree_tags', tags_list),
    url(r'^add/?$', page_save),
    url(r'^post_image/?$', post_image),
    url(r'^tag/(?P<match>.+)/?$', page_list),
    url(r'^(?P<author>.+)/tag/(?P<match>.+)/?$', page_list),
    url(r'^(?P<author>.+)/(?P<permlink>.+)/?$', IndexView.as_view()),
    url(r'^(?P<author>.+)/?$', page_list),
]
