# Variáveis de Ambiente — Sistema XBPNEUS

Este documento resume as variáveis de ambiente necessárias para executar o backend em diferentes contextos (desenvolvimento local, Render, pipelines de CI/CD).

## Autenticação e Bootstrap do Administrador

| Variável | Obrigatória | Descrição | Observações |
| --- | --- | --- | --- |
| `ADMIN_EMAIL` | Em produção | E-mail do superusuário criado pelo comando `bootstrap_admin`. | Usada quando `ADMIN_PASSWORD` também é fornecida. |
| `ADMIN_PASSWORD` | Em produção | Senha do superusuário bootstrap. | Nunca commitar valores padrão; defina diretamente no provedor (Render). |
| `ADMIN_NAME` | Opcional | Nome/Razão social do superusuário. | Caso ausente, usa `Administrador`. |
| `ADMIN_CNPJ` | Opcional | CNPJ do superusuário bootstrap. | Caso ausente, usa `00000000000000`. |
| `ADMIN_PHONE` | Opcional | Telefone associado ao superusuário. | Padrão `0000000000`. |
| `DJANGO_SUPERUSER_EMAIL` | Alternativa | Compatibilidade com scripts antigos. | Se definido junto da senha, o comando `bootstrap_admin` o utilizará. |
| `DJANGO_SUPERUSER_PASSWORD` | Alternativa | Compatibilidade com scripts legados. | — |
| `DJANGO_SUPERUSER_NOME_RAZAO_SOCIAL` | Alternativa | Nome usado no bootstrap. | Padrão `Administrador`. |
| `DJANGO_SUPERUSER_CNPJ` | Alternativa | CNPJ usado no bootstrap. | Padrão `00000000000000`. |
| `DJANGO_SUPERUSER_TELEFONE` | Alternativa | Telefone usado no bootstrap. | Padrão `0000000000`. |

> O script `build.sh` executa `python manage.py bootstrap_admin` automaticamente quando as variáveis necessárias estão definidas.

## Configurações de Segurança

| Variável | Obrigatória | Descrição |
| --- | --- | --- |
| `SECRET_KEY` | Sim (exceto dev) | Chave de criptografia do Django. |
| `DEBUG` | Não | Define se o Django roda em modo debug. No Render deve ser `False`. |
| `ALLOWED_HOSTS` | Sim | Lista de hosts permitidos separados por vírgula. |
| `CSRF_TRUSTED_ORIGINS` | Recomendado | Domínios autorizados para requisições com CSRF. |
| `SESSION_COOKIE_SECURE` | Recomendado | Ativa cookies de sessão seguros. |
| `CSRF_COOKIE_SECURE` | Recomendado | Ativa cookies CSRF seguros. |
| `SECURE_SSL_REDIRECT` | Recomendado | Redireciona tráfego HTTP para HTTPS. |

## Integrações e Serviços

| Variável | Obrigatória | Descrição |
| --- | --- | --- |
| `DATABASE_URL` | Sim | String de conexão com o banco (Postgres no Render). |
| `REDIS_URL` | Recomendado | Conexão com o Redis usado por filas e cache. |
| `OPENAI_API_KEY` | Opcional | Chave para recursos de IA. |
| `SENTRY_DSN` | Opcional | Integração com Sentry para monitoramento de erros. |

## CORS e API

| Variável | Obrigatória | Descrição |
| --- | --- | --- |
| `CORS_ALLOW_ALL_ORIGINS` | Não | Permite todos os domínios (`True`/`False`). |
| `CORS_ALLOWED_ORIGINS` | Recomendado | Lista de origens separadas por vírgula quando `CORS_ALLOW_ALL_ORIGINS=False`. |
| `CORS_ALLOW_CREDENTIALS` | Não | Habilita envio de cookies/autenticação em requisições CORS. |

## Execução Local

Para desenvolvimento local é comum definir as variáveis via arquivo `.env` ou exportá-las diretamente no shell:

```bash
export DEBUG=True
export DATABASE_URL=sqlite:///db.sqlite3
export ADMIN_EMAIL=admin@example.com
export ADMIN_PASSWORD=ChangeMe123
python manage.py bootstrap_admin
```

Garanta que `seed_perfis_xbpneus` seja executado após as migrações para configurar perfis e permissões mínimos.
