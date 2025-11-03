#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
Sistema de Banco de Dados de Problemas em Pneus de Carga
Criado para integração com XBPNEUS
"""

import sqlite3
import json
from datetime import datetime

class BancoDadosPneus:
    def __init__(self, db_path='problemas_pneus.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def conectar(self):
        """Conecta ao banco de dados SQLite"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print(f"✓ Conectado ao banco de dados: {self.db_path}")
        
    def criar_tabelas(self):
        """Cria todas as tabelas necessárias"""
        
        # Tabela de Categorias de Problemas
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT,
            codigo_vipal TEXT
        )
        ''')
        
        # Tabela Principal de Problemas
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS problemas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            nome TEXT NOT NULL,
            categoria_id INTEGER,
            severidade TEXT CHECK(severidade IN ('BAIXA', 'MEDIA', 'ALTA', 'CRITICA')),
            localizacao TEXT,
            descricao TEXT,
            aparencia TEXT,
            imagem_referencia TEXT,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
        ''')
        
        # Tabela de Causas
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS causas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problema_id INTEGER,
            tipo TEXT CHECK(tipo IN ('OPERACIONAL', 'MECANICA', 'FABRICACAO', 'AMBIENTAL', 'MANUTENCAO')),
            descricao TEXT NOT NULL,
            probabilidade TEXT CHECK(probabilidade IN ('BAIXA', 'MEDIA', 'ALTA')),
            FOREIGN KEY (problema_id) REFERENCES problemas(id)
        )
        ''')
        
        # Tabela de Ações Corretivas
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS acoes_corretivas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problema_id INTEGER,
            tipo_acao TEXT CHECK(tipo_acao IN ('IMEDIATA', 'PREVENTIVA', 'CORRETIVA', 'DESCARTE')),
            descricao TEXT NOT NULL,
            prioridade INTEGER,
            FOREIGN KEY (problema_id) REFERENCES problemas(id)
        )
        ''')
        
        # Tabela de Precauções
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS precaucoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problema_id INTEGER,
            descricao TEXT NOT NULL,
            tipo TEXT CHECK(tipo IN ('INSPECAO', 'CALIBRAGEM', 'MANUTENCAO', 'OPERACAO', 'ARMAZENAMENTO')),
            FOREIGN KEY (problema_id) REFERENCES problemas(id)
        )
        ''')
        
        # Tabela de Problemas Mecânicos do Veículo
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS problemas_mecanicos_veiculo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            componente TEXT NOT NULL,
            descricao TEXT,
            sintomas_pneu TEXT,
            padrao_desgaste TEXT
        )
        ''')
        
        # Tabela de Relação Problema-Mecânico
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS problema_mecanico_relacao (
            problema_id INTEGER,
            mecanico_id INTEGER,
            PRIMARY KEY (problema_id, mecanico_id),
            FOREIGN KEY (problema_id) REFERENCES problemas(id),
            FOREIGN KEY (mecanico_id) REFERENCES problemas_mecanicos_veiculo(id)
        )
        ''')
        
        # Tabela de Defeitos de Fabricação
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS defeitos_fabricacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            componente_afetado TEXT,
            processo_falho TEXT,
            detectabilidade TEXT
        )
        ''')
        
        # Tabela de Padrões de Desgaste
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS padroes_desgaste (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            nome_tecnico TEXT,
            aparencia TEXT,
            localizacao TEXT,
            causas_principais TEXT,
            posicao_pneu TEXT CHECK(posicao_pneu IN ('DIRECAO', 'TRACAO', 'REBOQUE', 'QUALQUER'))
        )
        ''')
        
        # Tabela de Condições Ambientais
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS condicoes_ambientais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fator TEXT NOT NULL,
            descricao TEXT,
            impacto TEXT,
            mitigacao TEXT
        )
        ''')
        
        # Tabela de Histórico e Fontes
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS fontes_informacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT CHECK(tipo IN ('FABRICANTE', 'TECNICO', 'ACADEMICO', 'NORMATIVO')),
            nome TEXT NOT NULL,
            url TEXT,
            data_consulta DATE,
            confiabilidade TEXT CHECK(confiabilidade IN ('BAIXA', 'MEDIA', 'ALTA'))
        )
        ''')
        
        self.conn.commit()
        print("✓ Tabelas criadas com sucesso")
        
    def popular_categorias(self):
        """Popula a tabela de categorias"""
        categorias = [
            ('BANDA_RODAGEM', 'Danos na Banda de Rodagem', '1-29'),
            ('CARCACA', 'Danos na Carcaça', '30-49'),
            ('FLANCO_OMBRO', 'Danos no Flanco e Ombro', '50-69'),
            ('TALAO', 'Danos no Talão', '70-79'),
            ('ESPECIAIS', 'Danos Especiais', '90-99'),
            ('DESGASTE_IRREGULAR', 'Padrões de Desgaste Irregular', None),
            ('FABRICACAO', 'Defeitos de Fabricação', None),
            ('MECANICO', 'Problemas Mecânicos do Veículo', None),
            ('OPERACIONAL', 'Problemas Operacionais', None),
            ('AMBIENTAL', 'Problemas Ambientais', None)
        ]
        
        for nome, descricao, codigo in categorias:
            try:
                self.cursor.execute('''
                INSERT INTO categorias (nome, descricao, codigo_vipal)
                VALUES (?, ?, ?)
                ''', (nome, descricao, codigo))
            except sqlite3.IntegrityError:
                pass  # Categoria já existe
                
        self.conn.commit()
        print(f"✓ {len(categorias)} categorias inseridas")
        
    def popular_problemas_banda_rodagem(self):
        """Popula problemas da banda de rodagem baseado no guia Vipal"""
        
        # Obter ID da categoria
        self.cursor.execute("SELECT id FROM categorias WHERE nome = 'BANDA_RODAGEM'")
        cat_id = self.cursor.fetchone()[0]
        
        problemas = [
            {
                'codigo': 'BR-01',
                'nome': 'Descolamento/Separação das Cintas',
                'severidade': 'CRITICA',
                'localizacao': 'Extremidades das cintas',
                'descricao': 'Extremidades das cinturas do pneu soltas e/ou separadas',
                'aparencia': 'Cintas visíveis e separadas da estrutura'
            },
            {
                'codigo': 'BR-02',
                'nome': 'Desgaste Irregular Acentuado no Ombro',
                'severidade': 'ALTA',
                'localizacao': 'Ombro da banda',
                'descricao': 'Ombro do pneu apresentando excesso de desgaste, resultando em extremidade de cintura exposta',
                'aparencia': 'Desgaste acentuado em um dos ombros'
            },
            {
                'codigo': 'BR-03',
                'nome': 'Arrancamento/Descolamento da Banda de Rodagem',
                'severidade': 'CRITICA',
                'localizacao': 'Banda de rodagem completa',
                'descricao': 'Arrancamento parcial e/ou total da banda de rodagem',
                'aparencia': 'Banda solta ou arrancada'
            },
            {
                'codigo': 'BR-04',
                'nome': 'Excesso de Picotamento na Banda de Rodagem',
                'severidade': 'MEDIA',
                'localizacao': 'Superfície da banda',
                'descricao': 'Numerosos cortes na banda de rodagem, podendo alcançar as cinturas',
                'aparencia': 'Múltiplos pequenos cortes'
            },
            {
                'codigo': 'BR-05',
                'nome': 'Lacerações Circunferenciais',
                'severidade': 'MEDIA',
                'localizacao': 'Banda de rodagem',
                'descricao': 'Excesso de cortes no sentido circunferencial na banda de rodagem',
                'aparencia': 'Cortes circulares ao redor do pneu'
            },
            {
                'codigo': 'BR-06',
                'nome': 'Roçamento na Banda de Rodagem',
                'severidade': 'ALTA',
                'localizacao': 'Banda de rodagem',
                'descricao': 'Avaria circunferencial por contato com partes do veículo',
                'aparencia': 'Marca de roçamento circular'
            },
            {
                'codigo': 'BR-07',
                'nome': 'Arrancamento da Raia/Ribe',
                'severidade': 'ALTA',
                'localizacao': 'Fundo do sulco',
                'descricao': 'Soltura/laceração no fundo do sulco com arrancamento parcial ou total',
                'aparencia': 'Raia solta ou arrancada'
            },
            {
                'codigo': 'BR-08',
                'nome': 'Desgaste Diagonal',
                'severidade': 'MEDIA',
                'localizacao': 'Banda completa',
                'descricao': 'Desgastes localizados e acentuados em toda circunferência em sentido diagonal',
                'aparencia': 'Padrão diagonal de desgaste'
            },
            {
                'codigo': 'BR-09',
                'nome': 'Desgaste Irregular Assimétrico',
                'severidade': 'MEDIA',
                'localizacao': 'Banda de rodagem',
                'descricao': 'Áreas da banda desgastadas em pontos alternados',
                'aparencia': 'Desgaste em manchas alternadas'
            },
            {
                'codigo': 'BR-10',
                'nome': 'Rachadura no Sulco (Pneus Diagonais)',
                'severidade': 'MEDIA',
                'localizacao': 'Sulcos da banda',
                'descricao': 'Rachadura no sulco da banda de rodagem',
                'aparencia': 'Rachaduras visíveis nos sulcos'
            },
            {
                'codigo': 'BR-11',
                'nome': 'Picotamento na Banda',
                'severidade': 'BAIXA',
                'localizacao': 'Banda de rodagem',
                'descricao': 'Numerosos pequenos cortes na banda',
                'aparencia': 'Múltiplos pequenos furos'
            },
            {
                'codigo': 'BR-12',
                'nome': 'Dano Localizado (Flat Spot)',
                'severidade': 'ALTA',
                'localizacao': 'Área específica da banda',
                'descricao': 'Desgaste localizado por freada brusca',
                'aparencia': 'Área plana de desgaste'
            },
            {
                'codigo': 'BR-13',
                'nome': 'Desgaste Centralizado',
                'severidade': 'MEDIA',
                'localizacao': 'Centro da banda',
                'descricao': 'Desgaste acentuado na região central',
                'aparencia': 'Centro mais desgastado que ombros'
            },
            {
                'codigo': 'BR-14',
                'nome': 'Arrancamento de Blocos',
                'severidade': 'ALTA',
                'localizacao': 'Blocos da banda trativa',
                'descricao': 'Rachaduras na base, rupturas parciais ou completas dos blocos',
                'aparencia': 'Blocos quebrados ou arrancados'
            }
        ]
        
        for p in problemas:
            self.cursor.execute('''
            INSERT OR IGNORE INTO problemas 
            (codigo, nome, categoria_id, severidade, localizacao, descricao, aparencia)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (p['codigo'], p['nome'], cat_id, p['severidade'], 
                  p['localizacao'], p['descricao'], p['aparencia']))
        
        self.conn.commit()
        print(f"✓ {len(problemas)} problemas de banda de rodagem inseridos")
        
    def popular_problemas_carcaca(self):
        """Popula problemas da carcaça"""
        
        self.cursor.execute("SELECT id FROM categorias WHERE nome = 'CARCACA'")
        cat_id = self.cursor.fetchone()[0]
        
        problemas = [
            {
                'codigo': 'CA-31',
                'nome': 'Penetração de Objeto',
                'severidade': 'ALTA',
                'localizacao': 'Carcaça',
                'descricao': 'Perfuração passante com objeto na região da banda',
                'aparencia': 'Objeto perfurante visível'
            },
            {
                'codigo': 'CA-32',
                'nome': 'Quebra Circunferencial na Zona de Flexão',
                'severidade': 'CRITICA',
                'localizacao': 'Lateral do pneu',
                'descricao': 'Ruptura circunferencial em formato de zíper',
                'aparencia': 'Rachadura em zíper na lateral'
            },
            {
                'codigo': 'CA-33',
                'nome': 'Ruptura Circunferencial no Flanco',
                'severidade': 'CRITICA',
                'localizacao': 'Flanco',
                'descricao': 'Avaria e/ou deformação na lateral do pneu',
                'aparencia': 'Ruptura circular no flanco'
            },
            {
                'codigo': 'CA-34',
                'nome': 'Dano Interno no Liner',
                'severidade': 'CRITICA',
                'localizacao': 'Interior do pneu',
                'descricao': 'Estrutura do pneu com liner danificado',
                'aparencia': 'Dano interno visível'
            },
            {
                'codigo': 'CA-35',
                'nome': 'Ruptura Radial do Pneu',
                'severidade': 'CRITICA',
                'localizacao': 'Estrutura radial',
                'descricao': 'Pneu com ruptura radial por forte impacto',
                'aparencia': 'Ruptura no sentido radial'
            },
            {
                'codigo': 'CA-36',
                'nome': 'Descolamento entre Liner e Carcaça',
                'severidade': 'ALTA',
                'localizacao': 'Interior',
                'descricao': 'Bolha ou separação entre liner e estrutura',
                'aparencia': 'Bolha interna visível'
            },
            {
                'codigo': 'CA-37',
                'nome': 'Separação dos Cabos da Carcaça',
                'severidade': 'CRITICA',
                'localizacao': 'Carcaça',
                'descricao': 'Fios da carcaça espaçados ou aparentes',
                'aparencia': 'Cabos de aço visíveis'
            },
            {
                'codigo': 'CA-38',
                'nome': 'Dano por Infiltração',
                'severidade': 'CRITICA',
                'localizacao': 'Flanco',
                'descricao': 'Descolamento da borracha por infiltração',
                'aparencia': 'Separação de camadas'
            }
        ]
        
        for p in problemas:
            self.cursor.execute('''
            INSERT OR IGNORE INTO problemas 
            (codigo, nome, categoria_id, severidade, localizacao, descricao, aparencia)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (p['codigo'], p['nome'], cat_id, p['severidade'], 
                  p['localizacao'], p['descricao'], p['aparencia']))
        
        self.conn.commit()
        print(f"✓ {len(problemas)} problemas de carcaça inseridos")

    def popular_problemas_mecanicos_veiculo(self):
        """Popula problemas mecânicos do veículo que afetam pneus"""
        
        problemas_mecanicos = [
            {
                'componente': 'Alinhamento/Geometria',
                'descricao': 'Desalinhamento do eixo (convergência/divergência/camber)',
                'sintomas_pneu': 'Desgaste irregular, desgaste unilateral',
                'padrao_desgaste': 'One-sided wear, Feathering'
            },
            {
                'componente': 'Balanceamento',
                'descricao': 'Rodas desbalanceadas',
                'sintomas_pneu': 'Desgaste em formato de concha, vibrações',
                'padrao_desgaste': 'Cupping, Multiple flat spotting'
            },
            {
                'componente': 'Suspensão',
                'descricao': 'Amortecedores desgastados ou molas fracas',
                'sintomas_pneu': 'Desgaste desigual, padrão de ondas',
                'padrao_desgaste': 'Cupping, Scallop wear'
            },
            {
                'componente': 'Rolamentos de Roda',
                'descricao': 'Rolamentos frouxos ou desgastados',
                'sintomas_pneu': 'Desgaste irregular, movimento lateral excessivo',
                'padrao_desgaste': 'Diagonal wear, Depression wear'
            },
            {
                'componente': 'Eixo',
                'descricao': 'Eixo empenado ou danificado',
                'sintomas_pneu': 'Desgaste interno em ambos os lados',
                'padrao_desgaste': 'Desgaste simétrico anormal'
            },
            {
                'componente': 'Sistema de Freios',
                'descricao': 'Freios travados, desajustados ou novos não assentados',
                'sintomas_pneu': 'Desgaste localizado, pontos planos',
                'padrao_desgaste': 'Flat spots, Brake skid damage'
            },
            {
                'componente': 'Terminal de Direção',
                'descricao': 'Terminais de direção danificados ou frouxos',
                'sintomas_pneu': 'Desgaste acentuado no ombro',
                'padrao_desgaste': 'Shoulder wear'
            },
            {
                'componente': 'Roda/Aro',
                'descricao': 'Roda inadequada, danificada ou com runout',
                'sintomas_pneu': 'Desgaste irregular, montagem inadequada',
                'padrao_desgaste': 'Diagonal wear, Depression wear'
            }
        ]
        
        for pm in problemas_mecanicos:
            self.cursor.execute('''
            INSERT INTO problemas_mecanicos_veiculo 
            (componente, descricao, sintomas_pneu, padrao_desgaste)
            VALUES (?, ?, ?, ?)
            ''', (pm['componente'], pm['descricao'], pm['sintomas_pneu'], pm['padrao_desgaste']))
        
        self.conn.commit()
        print(f"✓ {len(problemas_mecanicos)} problemas mecânicos inseridos")

    def popular_padroes_desgaste(self):
        """Popula padrões de desgaste irregular"""
        
        padroes = [
            {
                'nome': 'Desgaste Unilateral',
                'nome_tecnico': 'One-Sided Wear',
                'aparencia': 'Desgaste aumentando de um lado para o outro',
                'localizacao': 'Lateral da banda',
                'causas_principais': 'Desalinhamento (camber, convergência, paralelismo)',
                'posicao_pneu': 'DIRECAO'
            },
            {
                'nome': 'Desgaste em Degrau no Ombro',
                'nome_tecnico': 'Shoulder Step Wear',
                'aparencia': 'Depressão parcial ou total da nervura do ombro',
                'localizacao': 'Ombro',
                'causas_principais': 'Comum em pneus radiais de desgaste lento',
                'posicao_pneu': 'DIRECAO'
            },
            {
                'nome': 'Erosão/Desgaste em Rio',
                'nome_tecnico': 'Erosion/River Wear',
                'aparencia': 'Área desgastada circunferencial nas laterais das nervuras',
                'localizacao': 'Laterais das nervuras',
                'causas_principais': 'Pneus radiais de desgaste lento em rolamento livre',
                'posicao_pneu': 'DIRECAO'
            },
            {
                'nome': 'Desgaste Diagonal',
                'nome_tecnico': 'Diagonal Wear',
                'aparencia': 'Manchas de desgaste oblíquo',
                'localizacao': 'Banda completa',
                'causas_principais': 'Desalinhamento, runout, desbalanceamento, rolamentos frouxos',
                'posicao_pneu': 'DIRECAO'
            },
            {
                'nome': 'Serrilhado',
                'nome_tecnico': 'Feathering',
                'aparencia': 'Serrilhado na borda das nervuras',
                'localizacao': 'Bordas das nervuras',
                'causas_principais': 'Exposição contínua à força lateral, convergência excessiva',
                'posicao_pneu': 'DIRECAO'
            },
            {
                'nome': 'Desgaste em Concha',
                'nome_tecnico': 'Cupping/Scallop',
                'aparencia': 'Áreas localizadas em forma de concha',
                'localizacao': 'Banda completa',
                'causas_principais': 'Amortecedores defeituosos, rolamentos frouxos, desbalanceamento',
                'posicao_pneu': 'QUALQUER'
            },
            {
                'nome': 'Múltiplos Pontos Planos',
                'nome_tecnico': 'Multiple Flat Spotting',
                'aparencia': 'Múltiplas áreas radialmente desgastadas',
                'localizacao': 'Circunferência completa',
                'causas_principais': 'Amortecedores defeituosos, desbalanceamento severo',
                'posicao_pneu': 'DIRECAO'
            },
            {
                'nome': 'Desgaste Calcanhar/Ponta',
                'nome_tecnico': 'Heel/Toe Wear',
                'aparencia': 'Cada garra desgastada alto para baixo',
                'localizacao': 'Blocos da banda',
                'causas_principais': 'Pressão incompatível, alto torque, terrenos montanhosos',
                'posicao_pneu': 'TRACAO'
            },
            {
                'nome': 'Desgaste Centralizado',
                'nome_tecnico': 'Center Depression Wear',
                'aparencia': 'Centro mais desgastado que ombros',
                'localizacao': 'Centro da banda',
                'causas_principais': 'Pressão excessiva',
                'posicao_pneu': 'QUALQUER'
            },
            {
                'nome': 'Desgaste nos Ombros',
                'nome_tecnico': 'Shoulder Wear',
                'aparencia': 'Ombros mais desgastados que centro',
                'localizacao': 'Ombros',
                'causas_principais': 'Baixa pressão, excesso de carga',
                'posicao_pneu': 'QUALQUER'
            }
        ]
        
        for padrao in padroes:
            self.cursor.execute('''
            INSERT OR IGNORE INTO padroes_desgaste 
            (nome, nome_tecnico, aparencia, localizacao, causas_principais, posicao_pneu)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (padrao['nome'], padrao['nome_tecnico'], padrao['aparencia'],
                  padrao['localizacao'], padrao['causas_principais'], padrao['posicao_pneu']))
        
        self.conn.commit()
        print(f"✓ {len(padroes)} padrões de desgaste inseridos")

    def popular_defeitos_fabricacao(self):
        """Popula defeitos de fabricação"""
        
        defeitos = [
            {
                'nome': 'Separação de Banda de Rodagem',
                'descricao': 'Descolamento entre camadas do pneu',
                'componente_afetado': 'Banda de rodagem',
                'processo_falho': 'Vulcanização inadequada',
                'detectabilidade': 'Visível após uso'
            },
            {
                'nome': 'Separação de Cintas de Aço',
                'descricao': 'Falha na adesão das cintas de aço à carcaça',
                'componente_afetado': 'Cintas de aço',
                'processo_falho': 'Uso de solvente inadequado antes da vulcanização',
                'detectabilidade': 'Visível após desgaste'
            },
            {
                'nome': 'Erros de Cura/Vulcanização',
                'descricao': 'Temperatura ou tempo inadequado no processo',
                'componente_afetado': 'Estrutura completa',
                'processo_falho': 'Controle de temperatura/tempo',
                'detectabilidade': 'Difícil detecção inicial'
            },
            {
                'nome': 'Pneu Incompleto',
                'descricao': 'Fabricado sem todos os componentes especificados',
                'componente_afetado': 'Camadas de reforço',
                'processo_falho': 'Controle de qualidade',
                'detectabilidade': 'Raio-X ou falha prematura'
            },
            {
                'nome': 'Deslocamento de Lona',
                'descricao': 'Movimentação das lonas internas',
                'componente_afetado': 'Lonas',
                'processo_falho': 'Montagem/vulcanização',
                'detectabilidade': 'Bolhas e deformações'
            },
            {
                'nome': 'Borracha Desatualizada',
                'descricao': 'Uso de borracha degradada ou fora do prazo',
                'componente_afetado': 'Composto de borracha',
                'processo_falho': 'Controle de estoque',
                'detectabilidade': 'Rachaduras prematuras'
            },
            {
                'nome': 'Contaminação por Objetos Estranhos',
                'descricao': 'Objetos estranhos incorporados durante fabricação',
                'componente_afetado': 'Estrutura interna',
                'processo_falho': 'Limpeza/controle de processo',
                'detectabilidade': 'Falha súbita'
            }
        ]
        
        for defeito in defeitos:
            self.cursor.execute('''
            INSERT INTO defeitos_fabricacao 
            (nome, descricao, componente_afetado, processo_falho, detectabilidade)
            VALUES (?, ?, ?, ?, ?)
            ''', (defeito['nome'], defeito['descricao'], defeito['componente_afetado'],
                  defeito['processo_falho'], defeito['detectabilidade']))
        
        self.conn.commit()
        print(f"✓ {len(defeitos)} defeitos de fabricação inseridos")

    def popular_condicoes_ambientais(self):
        """Popula condições ambientais que afetam pneus"""
        
        condicoes = [
            {
                'fator': 'Temperatura Alta',
                'descricao': 'Exposição a temperaturas acima de 50°C',
                'impacto': 'Aceleração do envelhecimento, aumento de pressão interna, desgaste prematuro',
                'mitigacao': 'Calibragem a frio, evitar estacionamento ao sol, verificar pressão regularmente'
            },
            {
                'fator': 'Temperatura Baixa',
                'descricao': 'Exposição a temperaturas muito baixas',
                'impacto': 'Redução de pressão (1 PSI por 10°F), endurecimento da borracha',
                'mitigacao': 'Ajustar pressão conforme temperatura, usar compostos adequados'
            },
            {
                'fator': 'Radiação UV/Solar',
                'descricao': 'Exposição prolongada ao sol',
                'impacto': 'Degradação da borracha, rachaduras, ressecamento',
                'mitigacao': 'Armazenar em local coberto, usar protetores de pneus'
            },
            {
                'fator': 'Ozônio',
                'descricao': 'Exposição a ozônio atmosférico',
                'impacto': 'Rachaduras superficiais, envelhecimento acelerado',
                'mitigacao': 'Armazenamento adequado, uso regular dos pneus'
            },
            {
                'fator': 'Umidade',
                'descricao': 'Exposição a umidade excessiva',
                'impacto': 'Oxidação de componentes metálicos, infiltração',
                'mitigacao': 'Armazenar em local seco, inspecionar regularmente'
            },
            {
                'fator': 'Produtos Químicos',
                'descricao': 'Contato com óleos, solventes, ácidos',
                'impacto': 'Degradação da borracha, rachaduras',
                'mitigacao': 'Evitar contato, limpar imediatamente se ocorrer'
            },
            {
                'fator': 'Estradas Agressivas',
                'descricao': 'Superfícies ásperas, cascalho, pedras',
                'impacto': 'Cortes, perfurações, desgaste acelerado',
                'mitigacao': 'Escolher pneus adequados, ajustar velocidade e pressão'
            },
            {
                'fator': 'Armazenamento Prolongado',
                'descricao': 'Pneus sem uso por períodos longos',
                'impacto': 'Envelhecimento, deformação, perda de propriedades',
                'mitigacao': 'Armazenar corretamente (vertical ou horizontal), em local fresco e seco'
            }
        ]
        
        for cond in condicoes:
            self.cursor.execute('''
            INSERT INTO condicoes_ambientais 
            (fator, descricao, impacto, mitigacao)
            VALUES (?, ?, ?, ?)
            ''', (cond['fator'], cond['descricao'], cond['impacto'], cond['mitigacao']))
        
        self.conn.commit()
        print(f"✓ {len(condicoes)} condições ambientais inseridas")

    def adicionar_fontes(self):
        """Adiciona fontes de informação utilizadas"""
        
        fontes = [
            {
                'tipo': 'FABRICANTE',
                'nome': 'Vipal - Guia de Danos e Desgastes Pneus de Carga 2024',
                'url': 'https://vipal.com/download/vipal-guia-de-danos-e-desgastes-carga-2024-baixa-compactado.pdf',
                'data_consulta': '2025-10-08',
                'confiabilidade': 'ALTA'
            },
            {
                'tipo': 'FABRICANTE',
                'nome': 'Michelin - Irregular Tire Wear 101',
                'url': 'https://business.michelinman.com/tips-suggestions/irregular-tire-wear-101',
                'data_consulta': '2025-10-08',
                'confiabilidade': 'ALTA'
            },
            {
                'tipo': 'TECNICO',
                'nome': 'CLVehicles - 12 Grandes Danos Estruturais',
                'url': 'https://pt.clvehicles.com/blog/12-major-structural-damages-to-truck-tires_b110',
                'data_consulta': '2025-10-08',
                'confiabilidade': 'MEDIA'
            },
            {
                'tipo': 'FABRICANTE',
                'nome': 'Continental - Tire Damages',
                'url': 'https://www.continental-tires.com/pt/pt/tire-knowledge/tire-damages/',
                'data_consulta': '2025-10-08',
                'confiabilidade': 'ALTA'
            },
            {
                'tipo': 'TECNICO',
                'nome': 'Robson Forensic - Commercial Truck Tire Failure',
                'url': 'https://www.robsonforensic.com/articles/commercial-truck-tire-failure-expert',
                'data_consulta': '2025-10-08',
                'confiabilidade': 'ALTA'
            }
        ]
        
        for fonte in fontes:
            self.cursor.execute('''
            INSERT INTO fontes_informacao 
            (tipo, nome, url, data_consulta, confiabilidade)
            VALUES (?, ?, ?, ?, ?)
            ''', (fonte['tipo'], fonte['nome'], fonte['url'], 
                  fonte['data_consulta'], fonte['confiabilidade']))
        
        self.conn.commit()
        print(f"✓ {len(fontes)} fontes de informação registradas")

    def gerar_estatisticas(self):
        """Gera estatísticas do banco de dados"""
        
        print("\n" + "="*60)
        print("ESTATÍSTICAS DO BANCO DE DADOS DE PROBLEMAS EM PNEUS")
        print("="*60)
        
        # Total de categorias
        self.cursor.execute("SELECT COUNT(*) FROM categorias")
        print(f"\n📊 Categorias: {self.cursor.fetchone()[0]}")
        
        # Total de problemas
        self.cursor.execute("SELECT COUNT(*) FROM problemas")
        print(f"📊 Problemas catalogados: {self.cursor.fetchone()[0]}")
        
        # Problemas por categoria
        self.cursor.execute('''
        SELECT c.nome, COUNT(p.id) 
        FROM categorias c 
        LEFT JOIN problemas p ON c.id = p.categoria_id 
        GROUP BY c.nome
        ''')
        print("\n📋 Problemas por Categoria:")
        for cat, count in self.cursor.fetchall():
            print(f"   • {cat}: {count}")
        
        # Problemas mecânicos
        self.cursor.execute("SELECT COUNT(*) FROM problemas_mecanicos_veiculo")
        print(f"\n🔧 Problemas mecânicos do veículo: {self.cursor.fetchone()[0]}")
        
        # Padrões de desgaste
        self.cursor.execute("SELECT COUNT(*) FROM padroes_desgaste")
        print(f"📐 Padrões de desgaste: {self.cursor.fetchone()[0]}")
        
        # Defeitos de fabricação
        self.cursor.execute("SELECT COUNT(*) FROM defeitos_fabricacao")
        print(f"🏭 Defeitos de fabricação: {self.cursor.fetchone()[0]}")
        
        # Condições ambientais
        self.cursor.execute("SELECT COUNT(*) FROM condicoes_ambientais")
        print(f"🌡️  Condições ambientais: {self.cursor.fetchone()[0]}")
        
        # Fontes
        self.cursor.execute("SELECT COUNT(*) FROM fontes_informacao")
        print(f"📚 Fontes de informação: {self.cursor.fetchone()[0]}")
        
        print("\n" + "="*60)
        
    def fechar(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            print("\n✓ Conexão com banco de dados fechada")

def main():
    print("="*60)
    print("CRIAÇÃO DO BANCO DE DADOS DE PROBLEMAS EM PNEUS DE CARGA")
    print("Sistema para integração com XBPNEUS")
    print("="*60 + "\n")
    
    # Criar instância do banco
    db = BancoDadosPneus()
    
    try:
        # Conectar
        db.conectar()
        
        # Criar estrutura
        print("\n📦 Criando estrutura do banco de dados...")
        db.criar_tabelas()
        
        # Popular dados
        print("\n📝 Populando banco de dados...")
        db.popular_categorias()
        db.popular_problemas_banda_rodagem()
        db.popular_problemas_carcaca()
        db.popular_problemas_mecanicos_veiculo()
        db.popular_padroes_desgaste()
        db.popular_defeitos_fabricacao()
        db.popular_condicoes_ambientais()
        db.adicionar_fontes()
        
        # Gerar estatísticas
        db.gerar_estatisticas()
        
        print("\n✅ Banco de dados criado com sucesso!")
        print(f"📁 Localização: {db.db_path}")
        
    except Exception as e:
        print(f"\n❌ Erro ao criar banco de dados: {e}")
        raise
    finally:
        db.fechar()

if __name__ == "__main__":
    main()

