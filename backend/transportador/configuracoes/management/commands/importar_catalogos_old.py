"""
Comando Django para importar dados dos catálogos CSV
Sistema XBPneus - Gestão de Frotas de Transporte
"""

import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from backend.transportador.configuracoes.models import (
    CatalogoModeloVeiculo,
    MapaPosicaoPneu,
    OperacaoConfiguracao,
    MedidaPorPosicao,
    PressaoRecomendada,
    CatalogoPneuXBRI
)


class Command(BaseCommand):
    help = 'Importa dados dos catálogos CSV para o banco de dados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-dir',
            type=str,
            default='/home/ubuntu/upload/banco de dados',
            help='Diretório contendo os arquivos CSV'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpar dados existentes antes de importar'
        )

    def handle(self, *args, **options):
        csv_dir = options['csv_dir']
        clear = options['clear']

        self.stdout.write(self.style.SUCCESS(f'Iniciando importação de catálogos...'))
        self.stdout.write(f'Diretório CSV: {csv_dir}')

        try:
            with transaction.atomic():
                if clear:
                    self.limpar_dados()

                self.importar_catalogo_modelos(csv_dir)
                self.importar_mapa_posicoes(csv_dir)
                self.importar_operacoes(csv_dir)
                self.importar_medidas_posicao(csv_dir)
                self.importar_pressao_recomendada(csv_dir)
                self.importar_catalogo_xbri(csv_dir)

            self.stdout.write(self.style.SUCCESS('✅ Importação concluída com sucesso!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro na importação: {str(e)}'))
            raise

    def limpar_dados(self):
        self.stdout.write('Limpando dados existentes...')
        CatalogoModeloVeiculo.objects.all().delete()
        MapaPosicaoPneu.objects.all().delete()
        OperacaoConfiguracao.objects.all().delete()
        MedidaPorPosicao.objects.all().delete()
        PressaoRecomendada.objects.all().delete()
        CatalogoPneuXBRI.objects.all().delete()
        self.stdout.write(self.style.WARNING('Dados existentes removidos.'))

    def importar_catalogo_modelos(self, csv_dir):
        arquivo = os.path.join(csv_dir, 'catalogo_modelos_v05.csv')
        self.stdout.write(f'Importando catálogo de modelos de {arquivo}...')

        categoria_map = {
            'Caminhão/Trator': 'CAMINHAO_TRATOR',
            'Caminhão Rígido': 'CAMINHAO_RIGIDO',
            'Ônibus (Chassi)': 'ONIBUS_CHASSI',
            'Vans': 'VANS',
        }

        count = 0
        with open(arquivo, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                CatalogoModeloVeiculo.objects.create(
                    categoria=categoria_map.get(row['categoria'], 'CAMINHAO_TRATOR'),
                    marca=row['marca'],
                    familia_modelo=row['familia_modelo'],
                    variante=row['variante'],
                    ano_inicio=int(row['ano_inicio']),
                    ano_fim=int(row['ano_fim']),
                    configuracoes=row['configuracoes'],
                    observacoes=row.get('observacoes', '')
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ {count} modelos de veículos importados'))

    def importar_mapa_posicoes(self, csv_dir):
        arquivo = os.path.join(csv_dir, 'mapa_posicoes_v05.csv')
        self.stdout.write(f'Importando mapa de posições de {arquivo}...')

        count = 0
        with open(arquivo, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                MapaPosicaoPneu.objects.create(
                    config_id=row['config_id'],
                    componente=row['componente'],
                    eixo=int(row['eixo']),
                    lado=row['lado'],
                    rodado=row['rodado'],
                    posicao_tipo=row['posicao_tipo'],
                    position_id=row['position_id']
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ {count} posições de pneus importadas'))

    def importar_operacoes(self, csv_dir):
        arquivo = os.path.join(csv_dir, 'operacao_config_map_v06.csv')
        self.stdout.write(f'Importando operações de {arquivo}...')

        count = 0
        with open(arquivo, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                OperacaoConfiguracao.objects.create(
                    op_code=row['op_code'],
                    config_ids_recomendados=row['config_ids_recomendados'],
                    implementos_recomendados=row['implementos_recomendados'],
                    eixos_tipicos=row['eixos_tipicos'],
                    pbtc_faixa_aprox_t=row['pbtc_faixa_aprox_t'],
                    observacoes=row.get('observacoes', '')
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ {count} operações importadas'))

    def importar_medidas_posicao(self, csv_dir):
        arquivo = os.path.join(csv_dir, 'medidas_por_posicao_v05.csv')
        self.stdout.write(f'Importando medidas por posição de {arquivo}...')

        count = 0
        with open(arquivo, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                MedidaPorPosicao.objects.create(
                    config_id=row['config_id'],
                    posicao_tipo=row['posicao_tipo'],
                    medidas_tipicas=row['medidas_tipicas']
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ {count} medidas por posição importadas'))

    def importar_pressao_recomendada(self, csv_dir):
        arquivo = os.path.join(csv_dir, 'pressao_recomendada_v05.csv')
        self.stdout.write(f'Importando pressões recomendadas de {arquivo}...')

        categoria_map = {
            'Caminhão/Trator': 'CAMINHAO_TRATOR',
            'Caminhão Rígido': 'CAMINHAO_RIGIDO',
            'Implemento (SR)': 'IMPLEMENTO_SR',
            'Combinado': 'COMBINADO',
            'Ônibus': 'ONIBUS',
            'Vans': 'VANS',
        }

        count = 0
        with open(arquivo, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                PressaoRecomendada.objects.create(
                    categoria=categoria_map.get(row['categoria'], 'CAMINHAO_TRATOR'),
                    config_id=row.get('config_id', ''),
                    posicao_tipo=row['posicao_tipo'],
                    medida_exemplo=row['medida_exemplo'],
                    faixa_psi_min=int(row['faixa_psi_min']),
                    faixa_psi_max=int(row['faixa_psi_max']),
                    observacoes=row.get('observacoes', '')
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ {count} pressões recomendadas importadas'))

    def importar_catalogo_xbri(self, csv_dir):
        arquivo = os.path.join(csv_dir, 'xbri_catalogo_tbr_v0_7_norm.csv')
        self.stdout.write(f'Importando catálogo XBRI de {arquivo}...')

        count = 0
        with open(arquivo, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Função auxiliar para converter valores vazios em None
                def get_decimal(value):
                    if not value or value.strip() == '':
                        return None
                    return float(value.replace(',', '.'))

                def get_int(value):
                    if not value or value.strip() == '':
                        return None
                    return int(float(value))

                CatalogoPneuXBRI.objects.create(
                    linha=row['linha'],
                    modelo=row['modelo'],
                    medida=row['medida'],
                    ply_rating=row['ply_rating'],
                    aro_recomendado=row['aro_recomendado'],
                    indice_carga=row['indice_carga'],
                    indice_velocidade=row['indice_velocidade'],
                    largura_banda_mm=get_decimal(row.get('largura_banda_mm', '')),
                    largura_secao_mm=get_decimal(row.get('largura_secao_mm', '')),
                    profundidade_sulco_mm=get_decimal(row.get('profundidade_sulco_mm', '')),
                    diametro_externo_mm=get_int(row.get('diametro_externo_mm', '')),
                    pressao_max_psi=get_decimal(row.get('pressao_max_psi', '')),
                    fonte=row.get('fonte', ''),
                    li_single_num=get_int(row.get('li_single_num', '')),
                    li_dual_num=get_int(row.get('li_dual_num', '')),
                    linha_canonica=row['linha_canonica']
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ {count} pneus XBRI importados'))

