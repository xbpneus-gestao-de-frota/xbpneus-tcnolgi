from .base_settings import *

# --- Configurações de Autenticação ---



AUTH_USER_MODEL = 'transportador.UsuarioTransportador'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

