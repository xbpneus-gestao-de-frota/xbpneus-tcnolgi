"""
Endpoint temporário para executar migrations remotamente
ATENÇÃO: Este arquivo deve ser removido após uso por questões de segurança
"""
import os
import subprocess
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["POST"])
def run_migrations(request):
    """
    Endpoint temporário para executar migrations
    Requer secret key para segurança
    """
    # Verificar secret key
    secret = request.headers.get('X-Migration-Secret')
    expected_secret = os.environ.get('TEMP_MIGRATION_SECRET', 'xbpneus-migrate-2025')
    
    if secret != expected_secret:
        return JsonResponse({
            'error': 'Unauthorized',
            'message': 'Invalid secret key'
        }, status=401)
    
    try:
        # Executar migrations
        result = subprocess.run(
            ['python', 'manage.py', 'migrate'],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos de timeout
        )
        
        return JsonResponse({
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
        
    except subprocess.TimeoutExpired:
        return JsonResponse({
            'error': 'Timeout',
            'message': 'Migration process timed out after 5 minutes'
        }, status=500)
        
    except Exception as e:
        return JsonResponse({
            'error': 'Exception',
            'message': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def show_migrations(request):
    """
    Endpoint para mostrar status das migrations
    """
    secret = request.headers.get('X-Migration-Secret')
    expected_secret = os.environ.get('TEMP_MIGRATION_SECRET', 'xbpneus-migrate-2025')
    
    if secret != expected_secret:
        return JsonResponse({
            'error': 'Unauthorized',
            'message': 'Invalid secret key'
        }, status=401)
    
    try:
        # Mostrar migrations
        result = subprocess.run(
            ['python', 'manage.py', 'showmigrations'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return JsonResponse({
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
        
    except Exception as e:
        return JsonResponse({
            'error': 'Exception',
            'message': str(e)
        }, status=500)





@csrf_exempt
@require_http_methods(["POST"])
def make_migrations(request):
    """
    Endpoint para criar migrations
    """
    secret = request.headers.get('X-Migration-Secret')
    expected_secret = os.environ.get('TEMP_MIGRATION_SECRET', 'xbpneus-migrate-2025')
    
    if secret != expected_secret:
        return JsonResponse({
            'error': 'Unauthorized',
            'message': 'Invalid secret key'
        }, status=401)
    
    try:
        # Criar migrations
        result = subprocess.run(
            ['python', 'manage.py', 'makemigrations'],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        return JsonResponse({
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
        
    except Exception as e:
        return JsonResponse({
            'error': 'Exception',
            'message': str(e)
        }, status=500)

