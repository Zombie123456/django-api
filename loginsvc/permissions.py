from rest_framework import permissions
from django.utils.translation import ugettext as _
from oauth2_provider.models import AccessToken

from mewtwo.utils import parse_request_for_token, get_user_type


class IsAdmin(permissions.BasePermission):
    message = _('Only authorized users are allowed to access this API')

    def has_permission(self, request, view):
        user = request.user

        return user and user.is_staff


def is_staff(user):
    return user and user.groups.filter(name='staff_grp').exists()


class IsStaff(permissions.BasePermission):
    message = _('Only authorized user are allowed to access this API')

    def has_permission(self, request, view):
        user = request.user

        return is_staff(user)


def IsUserPermittedAdv(request, perms):
    user, user_group = parse_request_for_token(request)

    if user is None and user_group is None:
        user, user_type = parse_token_param(request)
    else:
        user_type = get_user_type(user)

    if not isinstance(perms, list):  # perms is a single permission
        perms = [perms]

    # Just need to check permissions for staff
    if user_type == 'staff':
        staff = user.staff_user
        if set(perms).issubset(
            set(staff.perms.values_list('key', flat=True))):
            return True
    elif user_type is None:
        return False
    elif user_type == 'admin':
        return True
    return False


def parse_token_param(request):
    token = request.GET.get('token') or ''
    token_obj = AccessToken.objects.filter(token=token).first()

    if token_obj:
        user = token_obj.user
        user_type = get_user_type(user)

        return user, user_type

    return None, None
