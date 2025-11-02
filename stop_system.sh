#!/bin/bash

# Script para parar o sistema XBPneus
# Criado automaticamente

echo "========================================="
echo "  Parando Sistema XBPneus"
echo "========================================="
echo ""

# Parar processos Django
echo "[1/3] Parando Backend (Django)..."
pkill -f "manage.py runserver" && echo "  ✓ Backend parado" || echo "  ⚠ Backend não estava rodando"
echo ""

# Parar processos Vite/Node
echo "[2/3] Parando Frontend (React + Vite)..."
pkill -f "vite" && echo "  ✓ Frontend parado" || echo "  ⚠ Frontend não estava rodando"
echo ""

# Parar Redis (opcional)
echo "[3/3] Mantendo Redis rodando (para próxima execução)"
echo "  → Para parar Redis: redis-cli shutdown"
echo ""

echo "========================================="
echo "  Sistema parado com sucesso!"
echo "========================================="
echo ""

