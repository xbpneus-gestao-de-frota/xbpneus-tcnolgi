#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de IA para Análise de Pneus de Carga
Integração com XBPNEUS
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from ..settings import IA_CONFIG
from .criar_banco_dados import BancoDadosPneus

class IAnalisePneus:
    """
    Sistema de Inteligência Artificial para análise de problemas em pneus de carga
    """
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = self._resolve_db_path(db_path)
        self.conn = None
        self.cursor = None
        self.conectar_db()

    def conectar_db(self):
        """Conecta ao banco de dados"""
        if not self.db_path.exists():
            self._seed_database()

        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
        self.cursor = self.conn.cursor()

    def _resolve_db_path(self, db_path: Optional[str]) -> Path:
        base_path = Path(IA_CONFIG.get('DATABASE_PATH'))
        base_path.mkdir(parents=True, exist_ok=True)

        if db_path:
            candidate = Path(db_path)
            if not candidate.is_absolute():
                candidate = base_path / candidate
        else:
            candidate = base_path / 'problemas_pneus.db'

        candidate.parent.mkdir(parents=True, exist_ok=True)
        return candidate

    def _seed_database(self):
        banco = BancoDadosPneus(str(self.db_path))
        banco.conectar()
        try:
            banco.criar_tabelas()
            banco.popular_categorias()
            banco.popular_problemas_banda_rodagem()
            banco.popular_problemas_carcaca()
            banco.popular_problemas_mecanicos_veiculo()
            banco.popular_padroes_desgaste()
            banco.popular_defeitos_fabricacao()
            banco.popular_condicoes_ambientais()
            banco.adicionar_fontes()
        finally:
            banco.fechar()
        
    def analisar_sintomas(self, sintomas: Dict) -> Dict:
        """
        Analisa sintomas fornecidos e retorna diagnóstico
        
        Args:
            sintomas: Dicionário com informações do pneu
                {
                    'tipo_desgaste': str,
                    'localizacao': str,
                    'severidade': str,
                    'posicao_pneu': str,
                    'sintomas_adicionais': List[str]
                }
        
        Returns:
            Dicionário com diagnóstico completo
        """
        resultado = {
            'problemas_identificados': [],
            'causas_provaveis': [],
            'problemas_mecanicos': [],
            'acoes_recomendadas': [],
            'nivel_urgencia': 'BAIXA',
            'timestamp': datetime.now().isoformat()
        }
        
        # Buscar problemas correspondentes
        problemas = self._buscar_problemas_por_sintomas(sintomas)
        resultado['problemas_identificados'] = problemas
        
        # Buscar causas
        for problema in problemas:
            causas = self._buscar_causas(problema['id'])
            resultado['causas_provaveis'].extend(causas)
        
        # Buscar problemas mecânicos relacionados
        if sintomas.get('tipo_desgaste'):
            mecanicos = self._buscar_problemas_mecanicos(sintomas['tipo_desgaste'])
            resultado['problemas_mecanicos'] = mecanicos
        
        # Determinar nível de urgência
        severidades = [p.get('severidade', 'BAIXA') for p in problemas]
        if 'CRITICA' in severidades:
            resultado['nivel_urgencia'] = 'CRITICA'
        elif 'ALTA' in severidades:
            resultado['nivel_urgencia'] = 'ALTA'
        elif 'MEDIA' in severidades:
            resultado['nivel_urgencia'] = 'MEDIA'
        
        # Gerar recomendações
        resultado['acoes_recomendadas'] = self._gerar_recomendacoes(resultado)
        
        return resultado
    
    def _buscar_problemas_por_sintomas(self, sintomas: Dict) -> List[Dict]:
        """Busca problemas no banco de dados baseado nos sintomas"""
        problemas = []
        
        query = "SELECT * FROM problemas WHERE 1=1"
        params = []
        
        if sintomas.get('localizacao'):
            query += " AND localizacao LIKE ?"
            params.append(f"%{sintomas['localizacao']}%")
        
        if sintomas.get('severidade'):
            query += " AND severidade = ?"
            params.append(sintomas['severidade'])
        
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        
        for row in rows:
            problemas.append(dict(row))
        
        return problemas
    
    def _buscar_causas(self, problema_id: int) -> List[Dict]:
        """Busca causas de um problema específico"""
        self.cursor.execute('''
        SELECT * FROM causas WHERE problema_id = ?
        ORDER BY probabilidade DESC
        ''', (problema_id,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def _buscar_problemas_mecanicos(self, tipo_desgaste: str) -> List[Dict]:
        """Busca problemas mecânicos relacionados ao padrão de desgaste"""
        self.cursor.execute('''
        SELECT * FROM problemas_mecanicos_veiculo 
        WHERE padrao_desgaste LIKE ?
        ''', (f'%{tipo_desgaste}%',))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def _gerar_recomendacoes(self, resultado: Dict) -> List[Dict]:
        """Gera recomendações baseadas no diagnóstico"""
        recomendacoes = []
        
        nivel = resultado['nivel_urgencia']
        
        if nivel == 'CRITICA':
            recomendacoes.append({
                'tipo': 'IMEDIATA',
                'acao': 'RETIRAR PNEU DE OPERAÇÃO IMEDIATAMENTE',
                'prioridade': 1,
                'descricao': 'Pneu apresenta risco crítico de falha. Descarte ou análise especializada necessária.'
            })
        elif nivel == 'ALTA':
            recomendacoes.append({
                'tipo': 'URGENTE',
                'acao': 'Inspecionar e avaliar extensão do dano',
                'prioridade': 2,
                'descricao': 'Solicitar análise de profissional especializado antes de continuar operação.'
            })
        
        # Recomendações baseadas em problemas mecânicos
        if resultado['problemas_mecanicos']:
            recomendacoes.append({
                'tipo': 'MANUTENCAO',
                'acao': 'Verificar componentes mecânicos do veículo',
                'prioridade': 3,
                'descricao': 'Problemas mecânicos identificados que podem estar causando desgaste irregular.'
            })
        
        # Recomendações gerais
        recomendacoes.append({
            'tipo': 'PREVENTIVA',
            'acao': 'Realizar inspeção periódica',
            'prioridade': 4,
            'descricao': 'Manter rotina de inspeção visual e calibragem dos pneus.'
        })
        
        return recomendacoes
    
    def diagnosticar_por_imagem(self, descricao_visual: str) -> Dict:
        """
        Diagnóstico baseado em descrição visual do pneu
        
        Args:
            descricao_visual: Descrição textual do que é visto no pneu
        
        Returns:
            Dicionário com possíveis diagnósticos
        """
        # Palavras-chave para identificação
        keywords_mapping = {
            'desgaste centro': ['Desgaste Centralizado', 'pressão excessiva'],
            'desgaste ombro': ['Desgaste nos Ombros', 'baixa pressão', 'excesso carga'],
            'desgaste lateral': ['Desgaste Unilateral', 'desalinhamento'],
            'bolha': ['Bolha/Saliência', 'impacto', 'dano estrutural'],
            'corte': ['Cortes', 'perfuração', 'objeto cortante'],
            'rachadura': ['Rachaduras', 'envelhecimento', 'produtos químicos'],
            'separação': ['Separação de Cintas', 'superaquecimento'],
            'desgaste diagonal': ['Desgaste Diagonal', 'desalinhamento', 'desbalanceamento'],
            'serrilhado': ['Serrilhado/Feathering', 'convergência excessiva'],
            'concha': ['Desgaste em Concha', 'amortecedores', 'balanceamento']
        }
        
        descricao_lower = descricao_visual.lower()
        diagnosticos = []
        
        for keyword, termos in keywords_mapping.items():
            if keyword in descricao_lower:
                diagnosticos.append({
                    'problema': termos[0],
                    'causas_possiveis': termos[1:],
                    'confianca': 'ALTA' if len([k for k in keyword.split() if k in descricao_lower]) > 1 else 'MEDIA'
                })
        
        return {
            'diagnosticos_possiveis': diagnosticos,
            'recomendacao': 'Realizar inspeção detalhada e medições para confirmar diagnóstico',
            'timestamp': datetime.now().isoformat()
        }
    
    def buscar_padroes_desgaste(self, posicao_pneu: Optional[str] = None) -> List[Dict]:
        """
        Busca padrões de desgaste catalogados
        
        Args:
            posicao_pneu: 'DIRECAO', 'TRACAO', 'REBOQUE' ou None para todos
        
        Returns:
            Lista de padrões de desgaste
        """
        if posicao_pneu:
            self.cursor.execute('''
            SELECT * FROM padroes_desgaste 
            WHERE posicao_pneu = ? OR posicao_pneu = 'QUALQUER'
            ''', (posicao_pneu,))
        else:
            self.cursor.execute('SELECT * FROM padroes_desgaste')
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def verificar_condicoes_ambientais(self, condicoes: List[str]) -> Dict:
        """
        Verifica impacto de condições ambientais
        
        Args:
            condicoes: Lista de condições ambientais (ex: ['temperatura alta', 'umidade'])
        
        Returns:
            Análise de impacto e mitigações
        """
        resultado = {
            'condicoes_identificadas': [],
            'impactos': [],
            'mitigacoes': []
        }
        
        for condicao in condicoes:
            self.cursor.execute('''
            SELECT * FROM condicoes_ambientais 
            WHERE LOWER(fator) LIKE ?
            ''', (f'%{condicao.lower()}%',))
            
            rows = self.cursor.fetchall()
            for row in rows:
                cond_dict = dict(row)
                resultado['condicoes_identificadas'].append(cond_dict['fator'])
                resultado['impactos'].append(cond_dict['impacto'])
                resultado['mitigacoes'].append(cond_dict['mitigacao'])
        
        return resultado
    
    def gerar_relatorio_completo(self, dados_pneu: Dict) -> Dict:
        """
        Gera relatório completo de análise do pneu
        
        Args:
            dados_pneu: Dicionário completo com todas as informações do pneu
        
        Returns:
            Relatório completo formatado
        """
        relatorio = {
            'identificacao': dados_pneu.get('identificacao', {}),
            'data_analise': datetime.now().isoformat(),
            'diagnostico': None,
            'historico': dados_pneu.get('historico', []),
            'recomendacoes_finais': [],
            'proxima_acao': None,
            'estimativa_vida_util': None
        }
        
        # Realizar diagnóstico
        if 'sintomas' in dados_pneu:
            relatorio['diagnostico'] = self.analisar_sintomas(dados_pneu['sintomas'])
        
        # Determinar próxima ação
        if relatorio['diagnostico']:
            nivel = relatorio['diagnostico']['nivel_urgencia']
            if nivel == 'CRITICA':
                relatorio['proxima_acao'] = 'DESCARTE IMEDIATO'
                relatorio['estimativa_vida_util'] = '0 km - FIM DE VIDA'
            elif nivel == 'ALTA':
                relatorio['proxima_acao'] = 'ANÁLISE ESPECIALIZADA'
                relatorio['estimativa_vida_util'] = 'Depende de avaliação'
            elif nivel == 'MEDIA':
                relatorio['proxima_acao'] = 'MONITORAMENTO INTENSIVO'
                relatorio['estimativa_vida_util'] = 'Reduzida - avaliar a cada 1000 km'
            else:
                relatorio['proxima_acao'] = 'MANUTENÇÃO PREVENTIVA'
                relatorio['estimativa_vida_util'] = 'Normal com manutenção adequada'
        
        return relatorio
    
    def consultar_problema_por_codigo(self, codigo: str) -> Optional[Dict]:
        """Consulta problema específico por código"""
        self.cursor.execute('SELECT * FROM problemas WHERE codigo = ?', (codigo,))
        row = self.cursor.fetchone()
        
        if row:
            problema = dict(row)
            # Buscar informações adicionais
            problema['causas'] = self._buscar_causas(problema['id'])
            return problema
        return None
    
    def listar_problemas_por_severidade(self, severidade: str) -> List[Dict]:
        """Lista todos os problemas de uma determinada severidade"""
        self.cursor.execute('''
        SELECT p.*, c.nome as categoria
        FROM problemas p
        JOIN categorias c ON p.categoria_id = c.id
        WHERE p.severidade = ?
        ORDER BY p.codigo
        ''', (severidade,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def buscar_por_texto(self, texto_busca: str) -> Dict:
        """
        Busca textual em todo o banco de dados
        
        Args:
            texto_busca: Texto a ser buscado
        
        Returns:
            Resultados encontrados em diferentes tabelas
        """
        resultados = {
            'problemas': [],
            'padroes_desgaste': [],
            'problemas_mecanicos': [],
            'defeitos_fabricacao': []
        }
        
        # Buscar em problemas
        self.cursor.execute('''
        SELECT * FROM problemas 
        WHERE nome LIKE ? OR descricao LIKE ? OR aparencia LIKE ?
        ''', (f'%{texto_busca}%', f'%{texto_busca}%', f'%{texto_busca}%'))
        resultados['problemas'] = [dict(row) for row in self.cursor.fetchall()]
        
        # Buscar em padrões de desgaste
        self.cursor.execute('''
        SELECT * FROM padroes_desgaste 
        WHERE nome LIKE ? OR nome_tecnico LIKE ? OR aparencia LIKE ?
        ''', (f'%{texto_busca}%', f'%{texto_busca}%', f'%{texto_busca}%'))
        resultados['padroes_desgaste'] = [dict(row) for row in self.cursor.fetchall()]
        
        # Buscar em problemas mecânicos
        self.cursor.execute('''
        SELECT * FROM problemas_mecanicos_veiculo 
        WHERE componente LIKE ? OR descricao LIKE ?
        ''', (f'%{texto_busca}%', f'%{texto_busca}%'))
        resultados['problemas_mecanicos'] = [dict(row) for row in self.cursor.fetchall()]
        
        # Buscar em defeitos de fabricação
        self.cursor.execute('''
        SELECT * FROM defeitos_fabricacao 
        WHERE nome LIKE ? OR descricao LIKE ?
        ''', (f'%{texto_busca}%', f'%{texto_busca}%'))
        resultados['defeitos_fabricacao'] = [dict(row) for row in self.cursor.fetchall()]
        
        return resultados
    
    def fechar(self):
        """Fecha conexão com banco de dados"""
        if self.conn:
            self.conn.close()

def exemplo_uso():
    """Exemplo de uso do sistema"""
    print("="*70)
    print("SISTEMA DE IA PARA ANÁLISE DE PNEUS DE CARGA")
    print("="*70 + "\n")
    
    # Inicializar sistema
    ia = IAnalisePneus()
    
    # Exemplo 1: Análise por sintomas
    print("📊 EXEMPLO 1: Análise por Sintomas")
    print("-" * 70)
    sintomas = {
        'tipo_desgaste': 'desgaste central',
        'localizacao': 'Centro da banda',
        'severidade': 'MEDIA',
        'posicao_pneu': 'TRACAO'
    }
    
    resultado = ia.analisar_sintomas(sintomas)
    print(f"Nível de Urgência: {resultado['nivel_urgencia']}")
    print(f"Problemas Identificados: {len(resultado['problemas_identificados'])}")
    print(f"Ações Recomendadas: {len(resultado['acoes_recomendadas'])}")
    
    # Exemplo 2: Diagnóstico por descrição visual
    print("\n\n📷 EXEMPLO 2: Diagnóstico por Descrição Visual")
    print("-" * 70)
    descricao = "Pneu apresenta desgaste acentuado no centro da banda, ombros praticamente intactos"
    diagnostico = ia.diagnosticar_por_imagem(descricao)
    print(f"Diagnósticos Possíveis: {len(diagnostico['diagnosticos_possiveis'])}")
    for diag in diagnostico['diagnosticos_possiveis']:
        print(f"  • {diag['problema']} (Confiança: {diag['confianca']})")
    
    # Exemplo 3: Buscar padrões de desgaste
    print("\n\n📐 EXEMPLO 3: Padrões de Desgaste para Pneus de Direção")
    print("-" * 70)
    padroes = ia.buscar_padroes_desgaste('DIRECAO')
    print(f"Total de padrões catalogados: {len(padroes)}")
    for padrao in padroes[:3]:
        print(f"  • {padrao['nome']} ({padrao['nome_tecnico']})")
    
    # Exemplo 4: Busca textual
    print("\n\n🔍 EXEMPLO 4: Busca Textual")
    print("-" * 70)
    resultados = ia.buscar_por_texto("desalinhamento")
    total = sum(len(v) for v in resultados.values())
    print(f"Resultados encontrados: {total}")
    for categoria, items in resultados.items():
        if items:
            print(f"  • {categoria}: {len(items)} resultado(s)")
    
    # Exemplo 5: Verificar condições ambientais
    print("\n\n🌡️  EXEMPLO 5: Análise de Condições Ambientais")
    print("-" * 70)
    condicoes = ['temperatura alta', 'radiação']
    analise = ia.verificar_condicoes_ambientais(condicoes)
    print(f"Condições identificadas: {len(analise['condicoes_identificadas'])}")
    for cond in analise['condicoes_identificadas']:
        print(f"  • {cond}")
    
    print("\n" + "="*70)
    print("✅ Sistema funcionando corretamente!")
    print("="*70)
    
    ia.fechar()

if __name__ == "__main__":
    exemplo_uso()

