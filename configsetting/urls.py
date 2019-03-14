from django.conf.urls import url, include
from configsetting import views as configsettings
from rest_framework import routers


manage_router = routers.DefaultRouter()
manage_router.register(r'global-preferences',
                       configsettings.GlobalPreferencesViewSet,
                       base_name='globalpreferences_config')

urlpatterns = [
    url(r'^manage/', include(manage_router.urls)),
]
