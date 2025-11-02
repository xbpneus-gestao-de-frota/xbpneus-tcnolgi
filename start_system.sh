#!/bin/bash

# Script para iniciar o sistema XBPneus localmente
# Criado automaticamente

echo "========================================="
echo "  Iniciando Sistema XBPneus"
echo "========================================="
echo ""

# Verificar e iniciar Redis
echo "[1/4] Verificando Redis..."
if ! redis-cli ping > /dev/null 2>&1; then
    echo "  → Iniciando Redis..."
    redis-server --daemonize yes
    sleep 2
fi
echo "  ✓ Redis rodando"
echo ""

# Iniciar Backend Django
echo "[2/4] Iniciando Backend (Django)..."
cd /home/ubuntu/xbpneus
python3.11 manage.py runserver 0.0.0.0:8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > backend_pid.txt
echo "  ✓ Backend iniciado (PID: $BACKEND_PID)"
echo "  → Logs: backend.log"
echo ""

# Aguardar backend iniciar
sleep 3

# Iniciar Frontend React
echo "[3/4] Iniciando Frontend (React + Vite)..."
cd /home/ubuntu/xbpneus/frontend
npm run dev > ../frontend.log 2>&1 &
sleep 5
FRONTEND_PID=$(lsof -t -i:3000)
echo $FRONTEND_PID > ../frontend_pid.txt
echo "  ✓ Frontend iniciado (PID: $FRONTEND_PID)"
echo "  → Logs: frontend.log"
echo ""

# Aguardar frontend iniciar
sleep 3

echo "[4/4] Sistema iniciado com sucesso!"
echo ""
echo "========================================="
echo "  URLs de Acesso:"
echo "========================================="
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000/api"
echo "  Admin Django: http://localhost:8000/admin"
echo "  API Docs: http://localhost:8000/api/schema/swagger-ui/"
echo ""
echo "========================================="
echo "  Processos:"
echo "========================================="
echo "  Backend PID: $BACKEND_PID"
echo "  Frontend PID: $FRONTEND_PID"
echo ""
echo "Para parar o sistema, execute:"
echo "  ./stop_system.sh"
echo ""
echo "Para ver os logs em tempo real:"
echo "  tail -f backend.log"
echo "  tail -f frontend.log"
echo ""

