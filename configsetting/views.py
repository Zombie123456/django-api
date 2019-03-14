from rest_condition import Or
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from configsetting.models import GlobalPreference
from configsetting.serializers import GlobalPreferencesSerializer
from mewtwo.utils import MewtwoRenderer
from loginsvc.permissions import IsAdmin, IsStaff
from mewtwo.lib import constants


class GlobalPreferencesViewSet(viewsets.GenericViewSet,
                               mixins.UpdateModelMixin,
                               mixins.ListModelMixin):
    model = GlobalPreference
    queryset = GlobalPreference.objects.all()
    permission_classes = [Or(IsAdmin, IsStaff)]
    serializer_class = GlobalPreferencesSerializer
    renderer_classes = [MewtwoRenderer]
    lookup_field = 'key'

    def update(self, request, *args, **kwargs):
        if not kwargs.get('partial', False):  # HTTP method `PUT` not allowed
            return Response(constants.NOT_ALLOWED, status=400)
        else:
            return super().update(request, *args, **kwargs)
