from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from backend.transportador.motorista_externo.models import MotoristaExterno

class Command(BaseCommand):
    help = 'Creates a new MotoristaExterno user'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='The email of the user')
        parser.add_argument('password', type=str, help='The password of the user')
        parser.add_argument('nome_completo', type=str, help='The full name of the user')
        parser.add_argument('cpf', type=str, help='The CPF of the user')
        parser.add_argument('cnh', type=str, help='The CNH of the user')
        parser.add_argument('telefone', type=str, help='The phone number of the user')
        parser.add_argument('--cnpj', type=str, help='The CNPJ of the user', default=None)

    def handle(self, *args, **options):
        User = get_user_model()
        email = options['email']
        password = options['password']
        nome_completo = options['nome_completo']
        cpf = options['cpf']
        cnh = options['cnh']
        telefone = options['telefone']
        cnpj = options['cnpj']

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f'User with email {email} already exists.'))
            return

        if MotoristaExterno.objects.filter(cpf=cpf).exists():
            self.stdout.write(self.style.ERROR(f'MotoristaExterno with CPF {cpf} already exists.'))
            return

        if MotoristaExterno.objects.filter(cnh=cnh).exists():
            self.stdout.write(self.style.ERROR(f'MotoristaExterno with CNH {cnh} already exists.'))
            return

        if cnpj and MotoristaExterno.objects.filter(cnpj=cnpj).exists():
            self.stdout.write(self.style.ERROR(f'MotoristaExterno with CNPJ {cnpj} already exists.'))
            return

        user = User.objects.create_user(email=email, password=password, is_active=False)

        motorista_data = {
            'usuario': user,
            'nome_completo': nome_completo,
            'cpf': cpf,
            'cnh': cnh,
            'telefone': telefone,
            'email': email,
            'aprovado': False
        }

        if cnpj:
            motorista_data['cnpj'] = cnpj

        MotoristaExterno.objects.create(**motorista_data)

        self.stdout.write(self.style.SUCCESS(f'Successfully created MotoristaExterno user {email}'))

