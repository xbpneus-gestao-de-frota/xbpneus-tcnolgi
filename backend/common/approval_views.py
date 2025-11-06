from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from transportador.models import UsuarioTransportador
from motorista.models import UsuarioMotorista
from motorista_externo.models import UsuarioMotoristaExterno
from borracharia.models import UsuarioBorracharia
from revenda.models import UsuarioRevenda
from recapagem.models import UsuarioRecapagem

# List of user models and their type identifiers. This makes it easy to
# iterate across the different profiles without duplicating code.
USER_MODELS = [
    ("transportador", UsuarioTransportador),
    ("motorista", UsuarioMotorista),
    ("motorista_externo", UsuarioMotoristaExterno),
    ("borracharia", UsuarioBorracharia),
    ("revenda", UsuarioRevenda),
    ("recapagem", UsuarioRecapagem),
]

@api_view(["GET"])
@permission_classes([IsAdminUser])
def list_pending_users(request):
    """Return all user profiles awaiting approval.

    This aggregates pending users across all defined user models and
    returns a unified representation containing the fields id, name,
    email, userType and data_criacao. Only administrators are allowed
    to access this endpoint.
    """
    results = []
    for user_type, model in USER_MODELS:
        # Filter for users that have not been approved yet. We rely on
        # the `aprovado` flag defined in each profile model.
        pending = model.objects.filter(aprovado=False)
        for user in pending:
            # Determine a display name: use the attribute
            # `nome_razao_social` if present, otherwise fallback to
            # `nome_completo`. If neither exists, default to an empty
            # string.
            name = (
                getattr(user, "nome_razao_social", None)
                or getattr(user, "nome_completo", None)
                or ""
            )
            created_at = getattr(user, "criado_em", None) or getattr(
                user, "created_at", None
            )
            results.append(
                {
                    "id": user.id,
                    "name": name,
                    "email": user.email,
                    "userType": user_type,
                    "data_criacao": created_at,
                }
            )
    return Response(results, status=status.HTTP_200_OK)

def _find_user_by_id(user_id):
    """Locate a user profile by primary key across all registered models.

    This helper returns a tuple (user_type, instance) if a user with
    the given ID is found, or (None, None) otherwise.
    """
    for user_type, model in USER_MODELS:
        try:
            return user_type, model.objects.get(id=user_id)
        except model.DoesNotExist:
            continue
    return None, None

@api_view(["POST"])
@permission_classes([IsAdminUser])
def approve_user(request, user_id):
    """Approve a pending user identified by its primary key.

    Once approved, the profile is marked as active (`is_active=True`) and
    approved (`aprovado=True`). If the model defines an `aprovado_em`
    timestamp, it will be updated to the current time. An error is
    returned if the user cannot be found.
    """
    user_type, user = _find_user_by_id(user_id)
    if user is None:
        return Response(
            {"detail": "Usuário não encontrado"},
            status=status.HTTP_404_NOT_FOUND,
        )
    user.aprovado = True
    user.is_active = True
    if hasattr(user, "aprovado_em"):
        user.aprovado_em = timezone.now()
    user.save()
    return Response(
        {"detail": f"{user_type.capitalize()} aprovado com sucesso"},
        status=status.HTTP_200_OK,
    )

@api_view(["POST"])
@permission_classes([IsAdminUser])
def reject_user(request, user_id):
    """Reject a pending user identified by its primary key.

    This implementation deactivates the profile (`is_active=False`) and
    keeps the `aprovado` flag false. The `aprovado_em` field (if
    present) is cleared. Adjust the logic here if you prefer to delete
    the profile entirely instead of simply deactivating it.
    """
    user_type, user = _find_user_by_id(user_id)
    if user is None:
        return Response(
            {"detail": "Usuário não encontrado"},
            status=status.HTTP_404_NOT_FOUND,
        )
    user.aprovado = False
    user.is_active = False
    if hasattr(user, "aprovado_em"):
        user.aprovado_em = None
    user.save()
    return Response(
        {"detail": f"{user_type.capitalize()} rejeitado com sucesso"},
        status=status.HTTP_200_OK,
    )
