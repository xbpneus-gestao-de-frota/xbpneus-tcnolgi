from rest_framework.filters import BaseFilterBackend

class EmpresaFilterBackend(BaseFilterBackend):
    """Filtra por empresa=usuario.empresa para qualquer queryset cujo modelo tenha o campo 'empresa'.
    Aplica-se em list/retrieve/update/delete pois DRF usa get_queryset() para get_object()."""
    def filter_queryset(self, request, queryset, view):
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return queryset.none()
        model = getattr(queryset, "model", None)
        if not model:
            return queryset
        try:
            field_names = [f.name for f in model._meta.get_fields()]
        except Exception:
            return queryset
        if "empresa" in field_names and getattr(user, "empresa_id", None):
            return queryset.filter(empresa=user.empresa)
        return queryset