from time import sleep

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from service.api.v1.serializers import SingInUserSerializer
from service.auth import IdentityProviderAuthentication
from service.models import User


class SingInAPIView(APIView):
    authentication_classes = (IdentityProviderAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SingInUserSerializer
    queryset = User.objects.all()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.data)
            user = serializer.data.get('user')

            sleep(500/1000)

            token = serializer.data.get('token')
            response_data = {'user': user, 'token': token}
            response = Response(response_data)
            response['authorization'] = response_data['token']
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
