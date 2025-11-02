from django.contrib.auth.backends import ModelBackend

class CustomAuthBackend(ModelBackend):
    """
    Backend de autenticação customizado que usa o ModelBackend padrão
    mas adiciona a verificação do campo 'aprovado' e 'is_active'
    após a autenticação bem-sucedida.

    Este backend é necessário para o processo inicial de obtenção do token
    através do /api/token/ (TokenObtainPairView), que usa o sistema
    de autenticação padrão do Django.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Tenta autenticar o usuário usando o ModelBackend padrão
        user = super().authenticate(request, username=username, password=password, **kwargs)
        
        if user:
            # Verifica se o usuário está ativo
            if not user.is_active:
                return None
            
            # Verifica se o usuário está aprovado (campo 'aprovado' é customizado)
            if hasattr(user, 'aprovado') and not user.aprovado:
                # Retornar None para falhar a autenticação
                return None
            
            return user
        
        return None
