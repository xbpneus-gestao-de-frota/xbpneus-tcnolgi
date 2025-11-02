# Ajustes de dependências — XBPNEUS

Atualizado em: 20251030-214036

## Backend (Python)
- **Adicionados**: Django, python-decouple, requests, openpyxl, numpy, whitenoise, django-cors-headers, django-redis,
  django-axes, django-health-check, psutil, redis, pika, django-storages, boto3, gunicorn.
- **Mantidos**: djangorestframework, djangorestframework-simplejwt, django-filter, dj_database_url, sentry_sdk, python-json-logger.
- **Removidos**: Pillow (não encontrado uso no código).

> Observação: `sentry_sdk` e `python-json-logger` já são usados em `config/settings.py` (logging JSON + Sentry).

## Frontend (React/Vite)
- **Adicionados**: chart.js, react-chartjs-2, clsx.
- **Removidos**: date-fns, recharts, zustand (não referenciados no código).
- **Ajuste**: `vite` movido para `devDependencies`.

## Notas
- Recomendado rodar `npm install` no `frontend/` para **atualizar o package-lock.json** de acordo com as mudanças.
- Recomendado rodar `pip install -r backend/requirements.txt` em ambiente limpo para validar as novas dependências.
