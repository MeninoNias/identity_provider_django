from django.core.management.base import BaseCommand
from service.models import User


class Command(BaseCommand):
    help = 'Cria 1000 usuários'

    def handle(self, *args, **options):
        for i in range(5000):
            first_name = f'USER {i}'
            email = f'user_{i}@example.com'
            User.objects.create_user(email=email, password='123456', first_name=first_name)
            print(f'Usuário criado: {first_name}')
        
