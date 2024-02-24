from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from rest_framework import authentication
from rest_framework import exceptions

from service.models import IdentityClient

class IdentityProviderUser(AnonymousUser):

    def __init__(self, client):
        self.identityClient = client
    
    @property
    def is_authenticated(self):
        return True


class IdentityProviderAuthentication(authentication.BasicAuthentication):
    def authenticate_credentials(self, userid, password, request=None):
        try:
            client = IdentityClient.objects.get(app_id=userid, api_key=password)
            return (IdentityProviderUser(client), None)
        except:
             raise exceptions.AuthenticationFailed()

