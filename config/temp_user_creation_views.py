import os
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

@api_view(['POST'])
def create_superuser_temp(request):
    secret_key = request.data.get('secret_key')
    expected_secret = os.environ.get('TEMP_USER_CREATION_SECRET')

    if not secret_key or secret_key != expected_secret:
        return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    username = request.data.get('username', 'admin')
    email = request.data.get('email', 'admin@xbpneus.com')
    password = request.data.get('password', 'Teste@2025')

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        return Response({'detail': f'Superuser {username} created successfully.'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'detail': f'Superuser {username} already exists.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_test_users_temp(request):
    secret_key = request.data.get('secret_key')
    expected_secret = os.environ.get('TEMP_USER_CREATION_SECRET')

    if not secret_key or secret_key != expected_secret:
        return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    users_data = [
        {'username': 'transportador', 'email': 'transportador@xbpneus.com', 'password': 'Teste@2025', 'is_staff': False, 'is_superuser': False},
        {'username': 'borracharia', 'email': 'borracharia@xbpneus.com', 'password': 'Teste@2025', 'is_staff': False, 'is_superuser': False},
        {'username': 'revenda', 'email': 'revenda@xbpneus.com', 'password': 'Teste@2025', 'is_staff': False, 'is_superuser': False},
        {'username': 'motorista', 'email': 'motorista@xbpneus.com', 'password': 'Teste@2025', 'is_staff': False, 'is_superuser': False},
        {'username': 'recapadora', 'email': 'recapadora@xbpneus.com', 'password': 'Teste@2025', 'is_staff': False, 'is_superuser': False},
    ]

    created_users = []
    for data in users_data:
        if not User.objects.filter(username=data['username']).exists():
            User.objects.create_user(**data)
            created_users.append(data['username'])

    if created_users:
        users_list = ', '.join(created_users)
        return Response({'detail': f'Test users created: {users_list}'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'detail': 'All test users already exist.'}, status=status.HTTP_200_OK)

