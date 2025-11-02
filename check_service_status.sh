
#!/bin/bash

echo "\n--- Verificação de Status dos Serviços ---"

# Verificar Redis
if pgrep redis-server > /dev/null; then
    echo "[OK] Redis está rodando."
else
    echo "[ERRO] Redis NÃO está rodando."
fi

# Verificar Backend (Django)
BACKEND_PID=$(cat backend_pid.txt)
if [ -n "$BACKEND_PID" ] && ps -p $BACKEND_PID > /dev/null; then
    echo "[OK] Backend (Django) está rodando (PID: $BACKEND_PID)."
else
    echo "[ERRO] Backend (Django) NÃO está rodando ou PID não encontrado/inválido."
fi

# Verificar Frontend (React + Vite)
FRONTEND_PID=$(cat frontend_pid.txt)
if [ -n "$FRONTEND_PID" ] && ps -p $FRONTEND_PID > /dev/null; then
    echo "[OK] Frontend (React + Vite) está rodando (PID: $FRONTEND_PID)."
else
    echo "[ERRO] Frontend (React + Vite) NÃO está rodando ou PID não encontrado/inválido."
fi

