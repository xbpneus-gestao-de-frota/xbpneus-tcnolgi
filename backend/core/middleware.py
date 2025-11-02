from django.http import JsonResponse

class TransportadorPathGuard:
    """Bloqueia acesso a /api/transportador/* se usuário não for role='transportador'."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path or ""
        if path.startswith("/api/transportador/"):
            user = getattr(request, "user", None)
            if not (user and getattr(user, "is_authenticated", False) and getattr(user, "role", None) == "transportador"):
                return JsonResponse({"detail": "Rota restrita ao Transportador."}, status=403)
        return self.get_response(request)