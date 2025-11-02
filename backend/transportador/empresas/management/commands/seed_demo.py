import random
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from django.apps import apps

def _generic_value_for(field):
    from django.db import models
    name = field.name.lower()
    if isinstance(field, models.CharField):
        if "email" in name:
            return "demo@example.org"
        if "cnpj" in name or "cpf" in name:
            return "00000000000000"
        if "telefone" in name:
            return "0000000000"
        return "DEMO"
    if isinstance(field, models.IntegerField):
        return 0
    if isinstance(field, models.BooleanField):
        return True
    if isinstance(field, models.DateTimeField):
        return datetime.now()
    if isinstance(field, models.DateField):
        return datetime.now().date()
    if isinstance(field, models.DecimalField):
        return 0
    return None

def _ensure_instance(model, unique_field_candidates=("nome","razao_social","name","fantasia","descricao")):
    payload = {}
    for f in model._meta.fields:
        if f.primary_key: 
            continue
        if getattr(f, "auto_now", False) or getattr(f, "auto_now_add", False):
            continue
        required = not f.null and not f.blank and f.default is f.empty
        if required:
            val = _generic_value_for(f)
            if val is not None:
                payload[f.name] = val
    lookup = {}
    for uf in unique_field_candidates:
        if uf in [fld.name for fld in model._meta.fields]:
            lookup = {uf: payload.get(uf, "DEMO")}
            payload.update(lookup)
            break
    obj, _ = model.objects.get_or_create(**(lookup or {"id": 1}), defaults=payload)
    return obj

class Command(BaseCommand):
    help = "Cria dados de demonstração (empresa, usuário admin, veículo, pneus, OS, etc.) — idempotente."

    @transaction.atomic
    def handle(self, *args, **options):
        Empresa = apps.get_model("empresas", "Empresa")
        empresa = _ensure_instance(Empresa)

        User = get_user_model()
        admin_username = "admin"
        admin_email = "admin@example.org"
        admin_password = "admin123"
        # compat: username field can vary
        username_field = getattr(User, "USERNAME_FIELD", "username")
        admin, created = User.objects.get_or_create(
            **{username_field: admin_username},
            defaults={"email": admin_email}
        )
        if created:
            admin.set_password(admin_password)
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()

        Veiculo = apps.get_model("transportador_frota", "Veiculo")
        PosicaoPneu = apps.get_model("transportador_frota", "PosicaoPneu")
        Pneu = apps.get_model("transportador_pneus", "Pneu")
        AplicacaoPneu = apps.get_model("transportador_pneus", "AplicacaoPneu")
        EventoPneu = apps.get_model("transportador_pneus", "EventoPneu")
        MovEstoque = apps.get_model("transportador_estoque", "MovimentacaoEstoquePneu")
        OrdemServico = apps.get_model("transportador_manutencao", "OrdemServico")
        ItemOS = apps.get_model("transportador_manutencao", "ItemOS")
        TestePosManutencao = apps.get_model("transportador_manutencao", "TestePosManutencao")

        veic, _ = Veiculo.objects.get_or_create(
            empresa=empresa, placa="DEM0A00",
            defaults={"tipo":"CAMINHAO","eixos_total":3,"marca":"XBP","modelo":"DemoTruck","km_atual":123456}
        )

        def _ensure_posicoes(v, empresa):
            # eixo 1
            for codigo in ["1E","1D"]:
                PosicaoPneu.objects.get_or_create(
                    empresa=empresa, veiculo=v, codigo=codigo,
                    defaults={"eixo_numero":1,"lado":"E" if codigo.endswith("E") else "D","camada":"S"}
                )
            # eixos restantes
            for eixo in range(2, v.eixos_total+1):
                for lado in ["E","D"]:
                    for camada, sufixo in [("I","-I"),("X","-X")]:
                        codigo = f"{eixo}{lado}{sufixo}"
                        PosicaoPneu.objects.get_or_create(
                            empresa=empresa, veiculo=v, codigo=codigo,
                            defaults={"eixo_numero":eixo,"lado":lado,"camada":camada}
                        )
        _ensure_posicoes(veic, empresa)

        p1, _ = Pneu.objects.get_or_create(
            empresa=empresa, codigo_interno="PN-DEMO-001",
            defaults={"medida":"295/80R22.5","marca":"XBRI","modelo":"CurveF1","status":"ESTOQUE","profundidade_sulco":16.0}
        )
        p2, _ = Pneu.objects.get_or_create(
            empresa=empresa, codigo_interno="PN-DEMO-002",
            defaults={"medida":"295/80R22.5","marca":"XBRI","modelo":"EcoWayF1","status":"APLICADO","profundidade_sulco":16.0}
        )

        pos_2ei = PosicaoPneu.objects.filter(veiculo=veic, codigo="2E-I").first() or                       PosicaoPneu.objects.filter(veiculo=veic).first()
        if pos_2ei:
            AplicacaoPneu.objects.get_or_create(
                empresa=empresa, pneu=p2, veiculo=veic, posicao_codigo=pos_2ei.codigo,
                defaults={"km_aplicacao":veic.km_atual, "status":"ATIVA"}
            )

        EventoPneu.objects.get_or_create(
            empresa=empresa, pneu=p2, tipo="CALIBRAGEM",
            defaults={"descricao":"Seed calibragem 100 PSI", "km":veic.km_atual, "pressao_psi":100}
        )

        MovEstoque.objects.get_or_create(
            empresa=empresa, pneu=p1, tipo="ENTRADA_NF",
            defaults={"quantidade":1, "nf_numero":"0001", "fornecedor":"Fornecedor Demo"}
        )

        os1, _ = OrdemServico.objects.get_or_create(
            empresa=empresa, veiculo=veic, status="ABERTA",
            defaults={"tipo":"CORRETIVA","prioridade":"MEDIA","descricao":"OS seed de demonstração"}
        )
        ItemOS.objects.get_or_create(
            os=os1, servico="Rodízio de pneus", defaults={"quantidade":1, "custo_unitario":0}
        )
        TestePosManutencao.objects.get_or_create(
            os=os1, defaults={"torque_ok":True,"pressao_ok":True,"rodagem_teste_ok":True}
        )

        self.stdout.write(self.style.SUCCESS("Seed de demonstração finalizado."))
        self.stdout.write("Usuário admin: admin / admin123")
