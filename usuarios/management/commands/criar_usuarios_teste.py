"""
Django management command para criar usuários de teste
Uso: python manage.py criar_usuarios_teste
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from usuarios.models import Usuario

User = get_user_model()


class Command(BaseCommand):
    help = 'Cria superusuário admin e usuários de teste para cada tipo'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("CRIANDO SUPERUSUÁRIO ADMIN")
        self.stdout.write("=" * 60)

        admin_email = 'admin@xbpneus.com'
        admin_password = 'Admin@2025'

        try:
            if User.objects.filter(email=admin_email).exists():
                self.stdout.write(self.style.WARNING(f"Superusuário {admin_email} já existe"))
                admin = User.objects.get(email=admin_email)
                # Atualizar senha
                admin.set_password(admin_password)
                admin.save()
                self.stdout.write(self.style.SUCCESS(f"Senha atualizada"))
            else:
                admin = User.objects.create_superuser(
                    email=admin_email,
                    password=admin_password,
                    nome='Administrador Sistema'
                )
                self.stdout.write(self.style.SUCCESS(f"Superusuário criado: {admin_email}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao criar superusuário: {e}"))

        self.stdout.write("")

        # Dados dos usuários de teste
        usuarios_teste = [
            {
                'email': 'transportador.teste@xbpneus.com',
                'password': 'Teste@2025',
                'nome': 'Transportador Teste',
                'tipo_usuario': 'transportador',
                'cpf_cnpj': '12345678901',
                'telefone': '11999999001',
                'is_active': True,
                'is_approved': True,
            },
            {
                'email': 'borracharia.teste@xbpneus.com',
                'password': 'Teste@2025',
                'nome': 'Borracharia Teste',
                'tipo_usuario': 'borracharia',
                'cpf_cnpj': '12345678902',
                'telefone': '11999999002',
                'is_active': True,
                'is_approved': True,
            },
            {
                'email': 'revenda.teste@xbpneus.com',
                'password': 'Teste@2025',
                'nome': 'Revenda Teste',
                'tipo_usuario': 'revenda',
                'cpf_cnpj': '12345678903',
                'telefone': '11999999003',
                'is_active': True,
                'is_approved': True,
            },
            {
                'email': 'motorista.teste@xbpneus.com',
                'password': 'Teste@2025',
                'nome': 'Motorista Teste',
                'tipo_usuario': 'motorista',
                'cpf_cnpj': '12345678904',
                'telefone': '11999999004',
                'is_active': True,
                'is_approved': True,
            },
            {
                'email': 'recapadora.teste@xbpneus.com',
                'password': 'Teste@2025',
                'nome': 'Recapadora Teste',
                'tipo_usuario': 'recapadora',
                'cpf_cnpj': '12345678905',
                'telefone': '11999999005',
                'is_active': True,
                'is_approved': True,
            },
        ]

        self.stdout.write("=" * 60)
        self.stdout.write("CRIANDO USUÁRIOS DE TESTE")
        self.stdout.write("=" * 60)

        usuarios_criados = []

        for user_data in usuarios_teste:
            email = user_data['email']
            password = user_data.pop('password')
            
            try:
                if User.objects.filter(email=email).exists():
                    self.stdout.write(self.style.WARNING(f"Usuário {email} já existe"))
                    user = User.objects.get(email=email)
                    # Atualizar senha e dados
                    user.set_password(password)
                    for key, value in user_data.items():
                        setattr(user, key, value)
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f"Dados atualizados"))
                else:
                    user = User.objects.create_user(
                        email=email,
                        password=password,
                        **user_data
                    )
                    self.stdout.write(self.style.SUCCESS(f"Usuário criado: {email}"))
                    self.stdout.write(f"   Tipo: {user_data['tipo_usuario']}")
                
                usuarios_criados.append({
                    'email': email,
                    'password': password,
                    'tipo': user_data['tipo_usuario'],
                    'nome': user_data['nome']
                })
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao criar usuário {email}: {e}"))
            
            self.stdout.write("")

        # Resumo final
        self.stdout.write("=" * 60)
        self.stdout.write("RESUMO - CREDENCIAIS DE ACESSO")
        self.stdout.write("=" * 60)
        self.stdout.write("")
        self.stdout.write("🔐 SUPERUSUÁRIO ADMIN")
        self.stdout.write(f"   Email: {admin_email}")
        self.stdout.write(f"   Senha: {admin_password}")
        self.stdout.write(f"   URL: https://xbpneus-backend.onrender.com/admin")
        self.stdout.write("")

        self.stdout.write("👥 USUÁRIOS DE TESTE")
        for user in usuarios_criados:
            self.stdout.write(f"   [{user['tipo'].upper()}] {user['nome']}")
            self.stdout.write(f"   Email: {user['email']}")
            self.stdout.write(f"   Senha: {user['password']}")
            self.stdout.write("")

        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("✅ COMANDO CONCLUÍDO COM SUCESSO!"))
        self.stdout.write("=" * 60)

