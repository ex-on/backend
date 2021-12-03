from django.contrib.auth import get_user_model
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework import exceptions
from rest_framework_jwt.compat import gettext_lazy as _


class CustomJSONWebTokenAuthentication(JSONWebTokenAuthentication):

    def jwt_get_uuid_from_payload(cls, *args, **kwargs):
        return api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER(*args, **kwargs)

    def authenticate_credentials(self, payload):
        uuid = self.jwt_get_uuid_from_payload(payload)

        if not uuid:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)
        try:
            User = get_user_model()
            user = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            msg = _('Invalid token.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user
