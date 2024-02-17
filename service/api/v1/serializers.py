import uuid

from rest_framework import serializers

from service.models import User
from service.utils import PasswordField


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_full_name

    class Meta:
        model = User
        fields = ['email', 'name', 'is_active', 'create_at', 'update_at']


class SingInUserSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = PasswordField(write_only=True)

    def _validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        users = User.objects.filter(email=email)
        if users.exists():
            user = users.first()

            if user.check_password(password):
                user = user
                if not user.is_active:
                    msg = u'Usuário inativo.'
                    raise serializers.ValidationError(msg, code='user_disabled')
                return {
                    'token': '{}'.format(uuid.uuid4()),
                    'user': UserSerializer(instance=user).data
                }
            else:
                msg = 'Login e/ou senha incorretos!'
                raise serializers.ValidationError(msg, code='login_failed')
        else:
            msg = 'Login e/ou senha incorretos!'
            raise serializers.ValidationError(msg, code='login_failed')

    def validate(self, attrs):
        request = self.context.get('request')
        try:
            return self._validate(attrs)
        except serializers.ValidationError as e:
            raise e

    def to_representation(self, instance):
        return instance
