# Diagnóstico do Django Admin

## Entrada e autenticação
- O admin fica exposto em `/admin/`, configurado diretamente em [`config/urls.py`](../config/urls.py).
- A administração dos usuários do transportador usa `UsuarioTransportadorAdmin`, permitindo aprovar/rejeitar contas pelo próprio Django Admin e mantendo os campos de auditoria como somente leitura. Isso está em [`backend/transportador/admin.py`](../backend/transportador/admin.py).

## Cobertura dos módulos
- Cada subaplicação registra seus modelos com configurações padrão (`list_display`, filtros e buscas) para garantir navegação completa. Exemplos: frota (`backend/transportador/frota/admin.py`) e multas (`backend/transportador/multas/admin.py`).
- Diversos módulos usam `list_display = [f.name for f in Model._meta.fields]`, garantindo visibilidade rápida sem precisar atualizar manualmente a configuração.

## Erro encontrado: Plano de Manutenção Preventiva
- O admin de manutenção ainda referenciava o campo `empresa` no fieldset "Informações Básicas", mas o campo foi removido do modelo [`PlanoManutencaoPreventiva`](../backend/transportador/manutencao/models.py). Ao carregar o formulário, o Django dispara `FieldError: Unknown field(s) (empresa) specified...`.
- É possível reproduzir o problema (antes da correção) executando:
  ```bash
  python manage.py shell -c "from django.contrib import admin; from django.test import RequestFactory; from types import SimpleNamespace; from backend.transportador.manutencao.admin import PlanoManutencaoPreventivaAdmin; from backend.transportador.manutencao.models import PlanoManutencaoPreventiva; rf=RequestFactory(); request=rf.get('/'); request.user=SimpleNamespace(has_perm=lambda perm: True); PlanoManutencaoPreventivaAdmin(PlanoManutencaoPreventiva, admin.site).get_form(request)"
  ```

## Correção aplicada
- Atualizamos o fieldset em [`backend/transportador/manutencao/admin.py`](../backend/transportador/manutencao/admin.py) para remover o campo inexistente e documentar a decisão. Agora o formulário é gerado normalmente e a linha de comando acima retorna os campos disponíveis sem exceções.
- O comando de verificação geral `python manage.py check` continua passando sem apontar regressões.
