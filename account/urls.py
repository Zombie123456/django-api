from django.conf.urls import url, include
from django.views.static import serve
from rest_framework import routers

from account import views as account
from mewtwo import settings
from loginsvc.views import login, logout, refresh_access_token


manage_router = routers.DefaultRouter()
manage_router.register(r'staff',
                       account.StaffViewSet,
                       base_name='staff')

urlpatterns = [
    url(r'^manage/', include(manage_router.urls)),

    url(r'^manage/password/$', account.reset_password,
        name='dashboard_reset_password'),
    url(r'^manage/my/$', account.current_user, name='admin_current_user'),

    # dashboard apis without routers
    url(r'^manage/login/$', login, name='dashboard_login'),
    url(r'^manage/login/refresh/', refresh_access_token,
        name='dashboard_refresh'),
    url(r'^logout/$', logout, name='account_logout'),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    url(r'^upload/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
