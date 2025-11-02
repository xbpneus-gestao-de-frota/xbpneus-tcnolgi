from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(["POST"])
@permission_classes([IsAdminUser])
def approve_user_by_email(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        # Verifica o tipo de usuário e aprova o perfil relacionado
        if hasattr(user, 'usuariotransportador'):
            user.usuariotransportador.aprovado = True
            user.usuariotransportador.save()
        elif hasattr(user, 'usuariomotorista'):
            user.usuariomotorista.aprovado = True
            user.usuariomotorista.save()
        # Adicionar outros tipos de usuário conforme necessário

        user.is_active = True
        user.save()
        return Response({"message": f"Usuário {email} aprovado com sucesso!"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# A view existente para aprovação de motorista externo (manter para compatibilidade)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def approve_motorista_externo(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if hasattr(user, 'motorista_externo_perfil'):
            user.motorista_externo_perfil.aprovado = True
            user.motorista_externo_perfil.save()
            user.is_active = True
            user.save()
            return Response({"message": f"Motorista externo {user.email} aprovado com sucesso!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Usuário não é um Motorista Externo"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

