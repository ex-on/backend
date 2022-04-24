from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from core.utils.jwt import cognito_jwt_decode_handler
from uuid import UUID

import inspect
import warnings

UserModel = get_user_model()


class CustomRemoteUserBackend(RemoteUserBackend):
    def authenticate(self, request, remote_user):
        """
        The username passed as ``remote_user`` is considered trusted. Return
        the ``User`` object with the given username. Create a new ``User``
        object if ``create_unknown_user`` is ``True``.

        Return None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        if not remote_user:
            return
        user = None
        username = self.clean_username(remote_user)

        # Note that this could be accomplished in one try-except clause, but
        # instead we use get_or_create when creating unknown users since it has
        # built-in safeguards for multiple threads.
        if self.create_unknown_user:
            user, created = UserModel._default_manager.get_or_create(**{
                UserModel.UUID_FIELD: username
            })
            if created:  # ← Attention
                args = (request, user)
                try:
                    inspect.getcallargs(self.configure_user, request, user)
                except TypeError:
                    args = (user,)
                    warnings.warn(
                        'Update %s.configure_user() to accept `request` as '
                        'the first argument.'
                        % self.__class__.__name__
                    )
                user = self.configure_user(*args)  # ← Attention
            else:  # ← Add
                user = self.configure_user(request, user)  # ← Add
        else:
            try:
                user = UserModel._default_manager.get_by_natural_key(
                    UUID(username).hex)
                # user = UserModel.objects.filter(uuid=username)
            except UserModel.DoesNotExist:
                pass
        return user if self.user_can_authenticate(user) else None
