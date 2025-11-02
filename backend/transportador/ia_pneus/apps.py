from django.apps import AppConfig


class IaPneusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.transportador.ia_pneus'
    verbose_name = 'IA - Análise de Pneus'
    
    def ready(self):
        """Inicialização do módulo de IA"""
        pass

