from rest_framework import permissions


class IsTransportador(permissions.BasePermission):
    """
    Permissão que permite acesso apenas para usuários do tipo Transportador
    """
    
    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Verifica se é um usuário transportador
        # O modelo de usuário transportador deve ter um relacionamento com User
        return hasattr(request.user, 'transportador')


class IsTransportadorOrAdmin(permissions.BasePermission):
    """
    Permissão que permite acesso para usuários Transportador ou Admin
    """
    
    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admins têm acesso total
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Verifica se é um usuário transportador
        return hasattr(request.user, 'transportador')

