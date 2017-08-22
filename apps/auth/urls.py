from django.conf.urls import url

from apps.auth.views import login


urlpatterns = [
    url(r'^login/', login),
]
