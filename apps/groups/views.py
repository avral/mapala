from rest_framework import viewsets

from apps.groups.models import Group
from apps.groups.serializers import GroupSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'name'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
