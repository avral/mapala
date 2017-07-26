from django.conf.urls import url

from apps.auth.views import login, sign_up


urlpatterns = [
    url(r'^login/', login),
    url(r'^sign_up/', sign_up),
]
