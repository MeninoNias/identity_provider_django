from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from rest_framework import authentication
from rest_framework import exceptions


class IdentityProviderUser(AnonymousUser):

    @property
    def is_authenticated(self):
        return True


class IdentityProviderAuthentication(authentication.BasicAuthentication):
    def authenticate_credentials(self, userid, password, request=None):
        try:
            if (settings.SSO_IDENTITY_PROVIDER_APP_ID == userid and settings.SSO_IDENTITY_PROVIDER_API_KEY == password):
                return (IdentityProviderUser(), None)
        except:
            pass
        raise exceptions.AuthenticationFailed()
