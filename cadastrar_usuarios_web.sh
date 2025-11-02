#!/bin/bash

echo "=== Cadastrando Motorista ==="
curl -X POST http://localhost:8000/api/motorista/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome_completo": "João Silva Santos",
    "cpf": "12345678900",
    "cnh": "12345678900",
    "categoria_cnh": "D",
    "telefone": "(11) 91234-5678",
    "email": "motorista.web@xbpneus.com",
    "password": "Senha123456",
    "password_confirm": "Senha123456"
  }' | python3 -m json.tool

echo -e "\n=== Cadastrando Borracharia ==="
curl -X POST http://localhost:8000/api/borracharia/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome_razao_social": "Borracharia Web Test Ltda",
    "cnpj": "98765432000111",
    "telefone": "(11) 92345-6789",
    "email": "borracharia.web@xbpneus.com",
    "password": "Senha123456",
    "password_confirm": "Senha123456"
  }' | python3 -m json.tool

echo -e "\n=== Cadastrando Revenda ==="
curl -X POST http://localhost:8000/api/revenda/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome_razao_social": "Revenda Web Test Ltda",
    "cnpj": "11222333000144",
    "telefone": "(11) 93456-7890",
    "email": "revenda.web@xbpneus.com",
    "password": "Senha123456",
    "password_confirm": "Senha123456"
  }' | python3 -m json.tool

echo -e "\n=== Cadastrando Recapagem ==="
curl -X POST http://localhost:8000/api/recapagem/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome_razao_social": "Recapagem Web Test Ltda",
    "cnpj": "55666777000188",
    "telefone": "(11) 94567-8901",
    "email": "recapagem.web@xbpneus.com",
    "password": "Senha123456",
    "password_confirm": "Senha123456"
  }' | python3 -m json.tool

echo -e "\n=== Todos os usuários cadastrados! ==="
