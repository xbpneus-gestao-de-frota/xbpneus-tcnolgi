import os
from rest_framework.permissions import BasePermission

class OptionalRolePermission(BasePermission):
    """
    If env XBP_ROLE_ENFORCE is truthy, require user to be staff/superuser or in one of allowed groups.
    Otherwise, allow authenticated users (IsAuthenticated still runs separately).
    """
    allowed_groups = {"transportador", "admin", "ops"}

    def has_permission(self, request, view):
        enforce = os.environ.get("XBP_ROLE_ENFORCE", "").lower() in {"1","true","yes","on"}
        if not enforce:
            return True
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or user.is_staff:
            return True
        try:
            return user.groups.filter(name__in=self.allowed_groups).exists()
        except Exception:
            return False



class IsMotorista(BasePermission):
    """
    Permissão que permite acesso apenas para usuários do tipo Motorista
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'motorista'


class IsTransportador(BasePermission):
    """
    Permissão que permite acesso apenas para usuários do tipo Transportador
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'transportador'


class IsRevenda(BasePermission):
    """
    Permissão que permite acesso apenas para usuários do tipo Revenda
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'revenda'


class IsBorracharia(BasePermission):
    """
    Permissão que permite acesso apenas para usuários do tipo Borracharia
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'borracharia'


class IsRecapagem(BasePermission):
    """
    Permissão que permite acesso apenas para usuários do tipo Recapagem
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'recapagem'


class HasRolePermission(BasePermission):
    """
    Permissão genérica que verifica se o usuário tem um dos roles permitidos
    Use: permission_classes = [HasRolePermission]
    E defina: allowed_roles = ['motorista', 'transportador']
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        allowed_roles = getattr(view, 'allowed_roles', [])
        if not allowed_roles:
            return True  # Se não especificou roles, permite todos autenticados
        
        return request.user.role in allowed_roles

