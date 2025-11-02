#!/bin/bash

echo "=== Testando Login de Todos os 5 Tipos de Usuário ==="
echo ""

tipos=("transportador" "motorista" "borracharia" "revenda" "recapagem")

for tipo in "${tipos[@]}"; do
    echo "Testando $tipo..."
    response=$(curl -s -X POST http://localhost:8000/api/$tipo/login/ \
        -H "Content-Type: application/json" \
        -d "{\"email\":\"teste_${tipo}@xbpneus.com\",\"password\":\"Senha123456\"}")
    
    if echo "$response" | grep -q "Login realizado com sucesso"; then
        echo "✅ $tipo: Login OK"
    else
        echo "❌ $tipo: Login FALHOU"
    fi
    echo ""
done

echo "=== Teste Concluído ==="
