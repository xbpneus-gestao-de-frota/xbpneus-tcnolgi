#!/bin/bash

# Script de Testes Manuais - Sistema XBPNEUS v10
# Testa todos os endpoints de cadastro e login dos 5 tipos de usuário

BASE_URL="http://localhost:8000/api"
SENHA="SenhaSegura123"

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "================================================================================"
echo "              TESTES MANUAIS - ENDPOINTS DO SISTEMA XBPNEUS v10"
echo "================================================================================"
echo ""

# Função para testar endpoint
test_endpoint() {
    local tipo=$1
    local endpoint=$2
    local data=$3
    local descricao=$4
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}Testando: ${descricao}${NC}"
    echo -e "${BLUE}Endpoint: ${endpoint}${NC}"
    echo ""
    
    response=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}${endpoint}" \
        -H "Content-Type: application/json" \
        -d "${data}")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
        echo -e "${GREEN}✓ Sucesso (HTTP $http_code)${NC}"
        echo "$body" | python -m json.tool 2>/dev/null || echo "$body"
    else
        echo -e "${RED}✗ Falha (HTTP $http_code)${NC}"
        echo "$body" | python -m json.tool 2>/dev/null || echo "$body"
    fi
    
    echo ""
    return $http_code
}

# ============================================================================
# TESTE 1: CADASTRO DO TRANSPORTADOR
# ============================================================================

echo ""
echo "================================================================================"
echo "                      TESTE 1: CADASTRO DO TRANSPORTADOR"
echo "================================================================================"
echo ""

transportador_data='{
  "email": "manual_transportador@xbpneus.com",
  "password": "'$SENHA'",
  "password_confirm": "'$SENHA'",
  "nome_razao_social": "Transportadora Manual Test Ltda",
  "cnpj": "98.765.432/0001-99",
  "telefone": "(11) 99999-8888"
}'

test_endpoint "transportador" "/transportador/register/" "$transportador_data" "Cadastro de Transportador"

# ============================================================================
# TESTE 2: CADASTRO DO MOTORISTA
# ============================================================================

echo ""
echo "================================================================================"
echo "                        TESTE 2: CADASTRO DO MOTORISTA"
echo "================================================================================"
echo ""

motorista_data='{
  "email": "manual_motorista@xbpneus.com",
  "password": "'$SENHA'",
  "password_confirm": "'$SENHA'",
  "nome_completo": "Carlos Alberto Manual Test",
  "cpf": "987.654.321-00",
  "cnh": "98765432100",
  "categoria_cnh": "D",
  "telefone": "(11) 98888-7777"
}'

test_endpoint "motorista" "/motorista/register/" "$motorista_data" "Cadastro de Motorista"

# ============================================================================
# TESTE 3: CADASTRO DA BORRACHARIA
# ============================================================================

echo ""
echo "================================================================================"
echo "                       TESTE 3: CADASTRO DA BORRACHARIA"
echo "================================================================================"
echo ""

borracharia_data='{
  "email": "manual_borracharia@xbpneus.com",
  "password": "'$SENHA'",
  "password_confirm": "'$SENHA'",
  "nome_razao_social": "Borracharia Manual Test Ltda",
  "cnpj": "87.654.321/0001-88",
  "telefone": "(11) 97777-6666"
}'

test_endpoint "borracharia" "/borracharia/register/" "$borracharia_data" "Cadastro de Borracharia"

# ============================================================================
# TESTE 4: CADASTRO DA REVENDA
# ============================================================================

echo ""
echo "================================================================================"
echo "                         TESTE 4: CADASTRO DA REVENDA"
echo "================================================================================"
echo ""

revenda_data='{
  "email": "manual_revenda@xbpneus.com",
  "password": "'$SENHA'",
  "password_confirm": "'$SENHA'",
  "nome_razao_social": "Revenda Manual Test Ltda",
  "cnpj": "76.543.210/0001-77",
  "telefone": "(11) 96666-5555"
}'

test_endpoint "revenda" "/revenda/register/" "$revenda_data" "Cadastro de Revenda"

# ============================================================================
# TESTE 5: CADASTRO DA RECAPAGEM
# ============================================================================

echo ""
echo "================================================================================"
echo "                        TESTE 5: CADASTRO DA RECAPAGEM"
echo "================================================================================"
echo ""

recapagem_data='{
  "email": "manual_recapagem@xbpneus.com",
  "password": "'$SENHA'",
  "password_confirm": "'$SENHA'",
  "nome_razao_social": "Recapagem Manual Test Ltda",
  "cnpj": "65.432.109/0001-66",
  "telefone": "(11) 95555-4444"
}'

test_endpoint "recapagem" "/recapagem/register/" "$recapagem_data" "Cadastro de Recapagem"

# ============================================================================
# TESTE 6: LOGIN PRÉ-APROVAÇÃO (DEVE FALHAR)
# ============================================================================

echo ""
echo "================================================================================"
echo "                   TESTE 6: LOGIN PRÉ-APROVAÇÃO (DEVE FALHAR)"
echo "================================================================================"
echo ""

echo -e "${YELLOW}Testando login do Motorista ANTES da aprovação (deve retornar 403)${NC}"
echo ""

motorista_login='{
  "email": "manual_motorista@xbpneus.com",
  "password": "'$SENHA'"
}'

test_endpoint "motorista" "/motorista/login/" "$motorista_login" "Login de Motorista (Pré-Aprovação)"

# ============================================================================
# TESTE 7: APROVAÇÃO AUTOMÁTICA
# ============================================================================

echo ""
echo "================================================================================"
echo "                        TESTE 7: APROVAÇÃO AUTOMÁTICA"
echo "================================================================================"
echo ""

echo -e "${YELLOW}Executando script de aprovação automática...${NC}"
echo ""

python approve_users.py --all 2>&1 | grep -E "(Aprovado|RESUMO|✅|❌)" || echo "Script de aprovação executado"

echo ""

# ============================================================================
# TESTE 8: LOGIN PÓS-APROVAÇÃO - TRANSPORTADOR
# ============================================================================

echo ""
echo "================================================================================"
echo "              TESTE 8: LOGIN PÓS-APROVAÇÃO - TRANSPORTADOR"
echo "================================================================================"
echo ""

transportador_login='{
  "email": "manual_transportador@xbpneus.com",
  "password": "'$SENHA'"
}'

test_endpoint "transportador" "/transportador/login/" "$transportador_login" "Login de Transportador (Pós-Aprovação)"

# ============================================================================
# TESTE 9: LOGIN PÓS-APROVAÇÃO - MOTORISTA
# ============================================================================

echo ""
echo "================================================================================"
echo "                TESTE 9: LOGIN PÓS-APROVAÇÃO - MOTORISTA"
echo "================================================================================"
echo ""

test_endpoint "motorista" "/motorista/login/" "$motorista_login" "Login de Motorista (Pós-Aprovação)"

# ============================================================================
# TESTE 10: LOGIN PÓS-APROVAÇÃO - BORRACHARIA
# ============================================================================

echo ""
echo "================================================================================"
echo "              TESTE 10: LOGIN PÓS-APROVAÇÃO - BORRACHARIA"
echo "================================================================================"
echo ""

borracharia_login='{
  "email": "manual_borracharia@xbpneus.com",
  "password": "'$SENHA'"
}'

test_endpoint "borracharia" "/borracharia/login/" "$borracharia_login" "Login de Borracharia (Pós-Aprovação)"

# ============================================================================
# TESTE 11: LOGIN PÓS-APROVAÇÃO - REVENDA
# ============================================================================

echo ""
echo "================================================================================"
echo "                TESTE 11: LOGIN PÓS-APROVAÇÃO - REVENDA"
echo "================================================================================"
echo ""

revenda_login='{
  "email": "manual_revenda@xbpneus.com",
  "password": "'$SENHA'"
}'

test_endpoint "revenda" "/revenda/login/" "$revenda_login" "Login de Revenda (Pós-Aprovação)"

# ============================================================================
# TESTE 12: LOGIN PÓS-APROVAÇÃO - RECAPAGEM
# ============================================================================

echo ""
echo "================================================================================"
echo "               TESTE 12: LOGIN PÓS-APROVAÇÃO - RECAPAGEM"
echo "================================================================================"
echo ""

recapagem_login='{
  "email": "manual_recapagem@xbpneus.com",
  "password": "'$SENHA'"
}'

test_endpoint "recapagem" "/recapagem/login/" "$recapagem_login" "Login de Recapagem (Pós-Aprovação)"

# ============================================================================
# TESTE 13: VALIDAÇÃO DE REDIRECTS
# ============================================================================

echo ""
echo "================================================================================"
echo "                    TESTE 13: VALIDAÇÃO DE REDIRECTS"
echo "================================================================================"
echo ""

echo -e "${YELLOW}Verificando se cada tipo de usuário recebe o redirect correto...${NC}"
echo ""

declare -A redirects=(
    ["transportador"]="/transportador/dashboard/"
    ["motorista"]="/motorista/dashboard/"
    ["borracharia"]="/borracharia/dashboard/"
    ["revenda"]="/revenda/dashboard/"
    ["recapagem"]="/recapagem/dashboard/"
)

for tipo in "${!redirects[@]}"; do
    expected="${redirects[$tipo]}"
    echo -e "${BLUE}Verificando redirect de ${tipo}...${NC}"
    
    # Fazer login e extrair redirect
    login_data='{
      "email": "manual_'$tipo'@xbpneus.com",
      "password": "'$SENHA'"
    }'
    
    redirect=$(curl -s -X POST "${BASE_URL}/${tipo}/login/" \
        -H "Content-Type: application/json" \
        -d "$login_data" | python -c "import sys, json; print(json.load(sys.stdin).get('redirect', 'N/A'))" 2>/dev/null)
    
    if [ "$redirect" = "$expected" ]; then
        echo -e "${GREEN}✓ Redirect correto: $redirect${NC}"
    else
        echo -e "${RED}✗ Redirect incorreto: esperado $expected, recebido $redirect${NC}"
    fi
    echo ""
done

# ============================================================================
# RESUMO FINAL
# ============================================================================

echo ""
echo "================================================================================"
echo "                              RESUMO FINAL"
echo "================================================================================"
echo ""
echo -e "${GREEN}✓ Testes manuais concluídos!${NC}"
echo ""
echo "Testes realizados:"
echo "  1. Cadastro do Transportador"
echo "  2. Cadastro do Motorista"
echo "  3. Cadastro da Borracharia"
echo "  4. Cadastro da Revenda"
echo "  5. Cadastro da Recapagem"
echo "  6. Login pré-aprovação (bloqueio)"
echo "  7. Aprovação automática"
echo "  8-12. Login pós-aprovação (5 tipos)"
echo "  13. Validação de redirects"
echo ""
echo "================================================================================"

