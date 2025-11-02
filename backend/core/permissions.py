from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTransportador(BasePermission):
    message = "Acesso restrito ao papel 'transportador'."
    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False
        return getattr(user, "role", None) == "transportador"