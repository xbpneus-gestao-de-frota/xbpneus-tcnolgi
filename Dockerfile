# Dockerfile para Sistema XBPneus
FROM python:3.11-slim

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements-production.txt .

# Instalar dependências Python
RUN pip install --upgrade pip && \
    pip install -r requirements-production.txt

# Copiar código do projeto
COPY . .

# Criar diretórios necessários
RUN mkdir -p logs staticfiles media

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput --settings=config.production

# Criar usuário não-root
RUN useradd -m -u 1000 xbpneus && \
    chown -R xbpneus:xbpneus /app

USER xbpneus

# Expor porta
EXPOSE 8000

# Comando para iniciar
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "config.wsgi:application"]

