import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from backend.transportador.empresas.models import Empresa
from backend.transportador.frota.models import Veiculo, VeiculoPosicao
from backend.transportador.pneus.models import Pneu
from backend.transportador.manutencao.models import OrdemServico, ItemOS

DATA_DIR = Path(__file__).resolve().parents[4] / "data"

class Command(BaseCommand):
    help = "Carrega dados demo (empresa, veículos/posições, pneus) a partir dos CSVs em xbpneus/data"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            emp, _ = Empresa.objects.get_or_create(
                cnpj="00.000.000/0001-00",
                defaults={"nome": "Transportador Demo LTDA", "tipo": "transportador"},
            )
            self.stdout.write(self.style.SUCCESS(f"Empresa: {emp}"))

            # Veículos a partir de catalogo_modelos (apenas alguns de exemplo)
            veiculos = []
            placas = ["ABC1D23","ABC2D34","ABC3D45","ABC4D56","ABC5D67"]
            try:
                with open(DATA_DIR/"catalogo_modelos_v05.csv", newline="", encoding="utf-8") as f:
                    reader = list(csv.DictReader(f))
                    for i, row in enumerate(reader[:5]):
                        v = Veiculo.objects.create(
                            empresa=emp,
                            placa=placas[i],
                            categoria=row.get("categoria","CAMINHAO")[:12] or "CAMINHAO",
                            marca=row.get("marca") or "GEN",
                            modelo=(row.get("familia_modelo") or "MODELO")+" "+ (row.get("variante") or ""),
                            ano=int(row.get("ano_inicio") or 2020),
                            config_id="CFG"+str(i+1),
                        )
                        veiculos.append(v)
                        self.stdout.write(self.style.SUCCESS(f"Veiculo criado: {v.placa} ({v.config_id})"))
            except FileNotFoundError:
                self.stdout.write(self.style.WARNING("catalogo_modelos_v05.csv não encontrado; criando veículos genéricos."))
                for i in range(5):
                    v = Veiculo.objects.create(empresa=emp, placa=placas[i], categoria="CAMINHAO", marca="GEN", modelo=f"X{i}", ano=2020+i, config_id=f"CFG{i+1}")
                    veiculos.append(v)

            # Posições por veículo a partir de mapa_posicoes
            try:
                mp = list(csv.DictReader(open(DATA_DIR/"mapa_posicoes_v05.csv", newline="", encoding="utf-8")))
                # agrupar por config_id de exemplo
                by_cfg = {}
                for r in mp:
                    by_cfg.setdefault(r["config_id"], []).append(r)
                for idx, v in enumerate(veiculos):
                    cfg = list(by_cfg.keys())[idx % len(by_cfg)] if by_cfg else None
                    rows = by_cfg.get(cfg, [])[:16]
                    for row in rows:
                        VeiculoPosicao.objects.create(
                            veiculo=v,
                            position_id=row.get("position_id") or f"P{row.get('eixo')}{row.get('lado')}{row.get('rodado')}",
                            posicao_tipo=row.get("posicao_tipo") or "DIANTEIRO",
                            eixo=int(row.get("eixo") or 1),
                            lado=(row.get("lado") or "E")[:1],
                            rodado=int(row.get("rodado") or 1),
                        )
                    self.stdout.write(self.style.SUCCESS(f"Posições criadas para {v.placa}: {len(rows)}"))
            except FileNotFoundError:
                self.stdout.write(self.style.WARNING("mapa_posicoes_v05.csv não encontrado; pulando posições."))

            # Pneus a partir de XBRI catálogo
            pneus_criados = 0
            cat_paths = [DATA_DIR/"xbri_catalogo_tbr_v0_7_norm.csv", DATA_DIR/"xbri_catalogo_tbr_v0_6.csv"]
            cat = None
            for p in cat_paths:
                if p.exists():
                    cat = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
                    break
            if cat:
                for i, row in enumerate(cat[:10]):
                    Pneu.objects.create(
                        empresa=emp,
                        numero_serie=f"SN{i+1:06d}",
                        medida=row.get("medida") or "295/80R22.5",
                        marca="XBRI",
                        linha=(row.get("linha_canonica") or row.get("linha") or "").upper()[:50] or None,
                        modelo=row.get("modelo"),
                        indice_carga=(row.get("li_single_num") or row.get("indice_carga") or "").strip() or None,
                        indice_velocidade=(row.get("indice_velocidade") or "").strip() or None,
                    )
                    pneus_criados += 1
                self.stdout.write(self.style.SUCCESS(f"Pneus criados: {pneus_criados}"))
            else:
                self.stdout.write(self.style.WARNING("catálogo XBRI não encontrado; sem pneus demo."))

            # Ordem de serviço exemplo
            if veiculos:
                os = OrdemServico.objects.create(
                    empresa=emp, veiculo=veiculos[0], titulo="Inspeção inicial", tipo="PREVENTIVA", prioridade="MEDIA"
                )
                ItemOS.objects.create(os=os, servico="Inspeção de torque", quantidade=1, custo_unitario=0)
                self.stdout.write(self.style.SUCCESS(f"OS criada: {os.id}"))

            self.stdout.write(self.style.SUCCESS("Seed concluído."))
