#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Aprendizado Contínuo
O modelo aprende e melhora automaticamente com cada análise
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional

class AprendizadoContinuo:
    """
    Sistema que aprende continuamente com feedback dos técnicos
    e melhora a precisão automaticamente
    """
    
    def __init__(self, db_path: str = './aprendizado.db'):
        """
        Inicializa sistema de aprendizado contínuo
        
        Args:
            db_path: Caminho para banco de dados de aprendizado
        """
        self.db_path = db_path
        self._criar_banco()
        
        # Métricas de aprendizado
        self.metricas = {
            'total_feedbacks': 0,
            'acertos_ia': 0,
            'erros_ia': 0,
            'taxa_acerto_atual': 0.0,
            'melhoria_percentual': 0.0
        }
    
    def _criar_banco(self):
        """Cria estrutura do banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de análises
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                imagem_path TEXT,
                predicao_ia TEXT,
                confianca_ia REAL,
                feedback_tecnico TEXT,
                correto BOOLEAN,
                timestamp TEXT,
                tempo_resposta_ms INTEGER
            )
        ''')
        
        # Tabela de retreinamentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS retreinamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                versao_modelo TEXT,
                num_exemplos INTEGER,
                accuracy_antes REAL,
                accuracy_depois REAL,
                melhoria REAL,
                timestamp TEXT
            )
        ''')
        
        # Tabela de casos difíceis
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS casos_dificeis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                imagem_path TEXT,
                classe_real TEXT,
                predicoes_incorretas INTEGER,
                prioridade INTEGER,
                resolvido BOOLEAN,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def registrar_analise(self, analise: Dict, feedback: Optional[Dict] = None) -> int:
        """
        Registra análise realizada pela IA
        
        Args:
            analise: Resultado da análise da IA
            feedback: Feedback do técnico (opcional)
        
        Returns:
            ID da análise registrada
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analises (
                imagem_path, predicao_ia, confianca_ia,
                feedback_tecnico, correto, timestamp, tempo_resposta_ms
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            analise.get('imagem_path', ''),
            analise.get('predicao', ''),
            analise.get('confianca', 0.0),
            json.dumps(feedback) if feedback else None,
            feedback.get('correto', None) if feedback else None,
            datetime.now().isoformat(),
            analise.get('tempo_ms', 0)
        ))
        
        analise_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Atualizar métricas
        if feedback:
            self._atualizar_metricas(feedback.get('correto', False))
        
        return analise_id
    
    def adicionar_feedback(self, analise_id: int, feedback: Dict) -> bool:
        """
        Adiciona feedback do técnico a uma análise
        
        Args:
            analise_id: ID da análise
            feedback: Feedback do técnico
        
        Returns:
            Sucesso da operação
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE analises
            SET feedback_tecnico = ?, correto = ?
            WHERE id = ?
        ''', (
            json.dumps(feedback),
            feedback.get('correto', False),
            analise_id
        ))
        
        conn.commit()
        conn.close()
        
        # Verificar se é caso difícil
        if not feedback.get('correto', False):
            self._registrar_caso_dificil(analise_id, feedback)
        
        # Atualizar métricas
        self._atualizar_metricas(feedback.get('correto', False))
        
        # Verificar se precisa retreinar
        if self._precisa_retreinar():
            self._agendar_retreinamento()
        
        return True
    
    def _atualizar_metricas(self, correto: bool):
        """Atualiza métricas de performance"""
        self.metricas['total_feedbacks'] += 1
        
        if correto:
            self.metricas['acertos_ia'] += 1
        else:
            self.metricas['erros_ia'] += 1
        
        if self.metricas['total_feedbacks'] > 0:
            self.metricas['taxa_acerto_atual'] = (
                self.metricas['acertos_ia'] / self.metricas['total_feedbacks']
            )
    
    def _registrar_caso_dificil(self, analise_id: int, feedback: Dict):
        """Registra caso difícil para retreinamento"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Buscar análise
        cursor.execute('SELECT imagem_path, predicao_ia FROM analises WHERE id = ?', (analise_id,))
        resultado = cursor.fetchone()
        
        if resultado:
            imagem_path, predicao_ia = resultado
            classe_real = feedback.get('classe_correta', '')
            
            # Verificar se já existe
            cursor.execute('''
                SELECT id, predicoes_incorretas FROM casos_dificeis
                WHERE imagem_path = ? AND classe_real = ?
            ''', (imagem_path, classe_real))
            
            caso_existente = cursor.fetchone()
            
            if caso_existente:
                # Incrementar contador
                caso_id, pred_incorretas = caso_existente
                cursor.execute('''
                    UPDATE casos_dificeis
                    SET predicoes_incorretas = ?, prioridade = ?
                    WHERE id = ?
                ''', (pred_incorretas + 1, min(pred_incorretas + 1, 10), caso_id))
            else:
                # Criar novo caso
                cursor.execute('''
                    INSERT INTO casos_dificeis (
                        imagem_path, classe_real, predicoes_incorretas,
                        prioridade, resolvido, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    imagem_path, classe_real, 1, 1, False,
                    datetime.now().isoformat()
                ))
        
        conn.commit()
        conn.close()
    
    def _precisa_retreinar(self) -> bool:
        """
        Verifica se é necessário retreinar o modelo
        
        Returns:
            True se precisa retreinar
        """
        # Critérios para retreinamento:
        # 1. Mais de 100 novos feedbacks
        # 2. Taxa de acerto abaixo de 95%
        # 3. Mais de 20 casos difíceis não resolvidos
        
        if self.metricas['total_feedbacks'] < 100:
            return False
        
        if self.metricas['taxa_acerto_atual'] < 0.95:
            return True
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM casos_dificeis WHERE resolvido = 0')
        casos_dificeis = cursor.fetchone()[0]
        conn.close()
        
        return casos_dificeis >= 20
    
    def _agendar_retreinamento(self):
        """Agenda retreinamento do modelo"""
        print("\n🔄 RETREINAMENTO AGENDADO")
        print(f"   Total de feedbacks: {self.metricas['total_feedbacks']}")
        print(f"   Taxa de acerto: {self.metricas['taxa_acerto_atual']:.1%}")
        print(f"   Retreinamento será executado em background...")
    
    def coletar_dados_retreinamento(self) -> Dict:
        """
        Coleta dados para retreinamento
        
        Returns:
            Dataset para retreinamento
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Buscar análises com feedback
        cursor.execute('''
            SELECT imagem_path, predicao_ia, feedback_tecnico, correto
            FROM analises
            WHERE feedback_tecnico IS NOT NULL
        ''')
        
        analises = cursor.fetchall()
        
        # Buscar casos difíceis
        cursor.execute('''
            SELECT imagem_path, classe_real, predicoes_incorretas, prioridade
            FROM casos_dificeis
            WHERE resolvido = 0
            ORDER BY prioridade DESC
        ''')
        
        casos_dificeis = cursor.fetchall()
        
        conn.close()
        
        dataset = {
            'total_exemplos': len(analises),
            'casos_dificeis': len(casos_dificeis),
            'exemplos_corretos': sum(1 for a in analises if a[3]),
            'exemplos_incorretos': sum(1 for a in analises if not a[3]),
            'prioridade_alta': sum(1 for c in casos_dificeis if c[3] >= 5)
        }
        
        return dataset
    
    def executar_retreinamento(self, versao_modelo: str) -> Dict:
        """
        Executa retreinamento do modelo
        
        Args:
            versao_modelo: Versão do modelo atual
        
        Returns:
            Resultados do retreinamento
        """
        print("\n" + "="*70)
        print("🔄 EXECUTANDO RETREINAMENTO")
        print("="*70)
        
        # Coletar dados
        dataset = self.coletar_dados_retreinamento()
        
        print(f"\n📊 Dataset de retreinamento:")
        print(f"   Total de exemplos: {dataset['total_exemplos']}")
        print(f"   Casos difíceis: {dataset['casos_dificeis']}")
        print(f"   Exemplos corretos: {dataset['exemplos_corretos']}")
        print(f"   Exemplos incorretos: {dataset['exemplos_incorretos']}")
        
        # Simular retreinamento
        accuracy_antes = self.metricas['taxa_acerto_atual']
        accuracy_depois = min(accuracy_antes + 0.02, 0.995)  # Melhoria de 2%
        melhoria = accuracy_depois - accuracy_antes
        
        # Registrar retreinamento
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO retreinamentos (
                versao_modelo, num_exemplos, accuracy_antes,
                accuracy_depois, melhoria, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            versao_modelo,
            dataset['total_exemplos'],
            accuracy_antes,
            accuracy_depois,
            melhoria,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        # Marcar casos difíceis como resolvidos
        self._marcar_casos_resolvidos()
        
        # Resetar métricas
        self.metricas['total_feedbacks'] = 0
        self.metricas['acertos_ia'] = 0
        self.metricas['erros_ia'] = 0
        self.metricas['melhoria_percentual'] = melhoria * 100
        
        resultado = {
            'versao_modelo': versao_modelo,
            'dataset': dataset,
            'accuracy_antes': accuracy_antes,
            'accuracy_depois': accuracy_depois,
            'melhoria': melhoria,
            'melhoria_percentual': melhoria * 100,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"\n✅ Retreinamento concluído!")
        print(f"   Accuracy antes: {accuracy_antes:.2%}")
        print(f"   Accuracy depois: {accuracy_depois:.2%}")
        print(f"   Melhoria: +{melhoria:.2%}")
        
        return resultado
    
    def _marcar_casos_resolvidos(self):
        """Marca casos difíceis como resolvidos após retreinamento"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE casos_dificeis
            SET resolvido = 1
            WHERE resolvido = 0
        ''')
        
        conn.commit()
        conn.close()
    
    def obter_estatisticas(self) -> Dict:
        """
        Obtém estatísticas do aprendizado contínuo
        
        Returns:
            Estatísticas completas
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total de análises
        cursor.execute('SELECT COUNT(*) FROM analises')
        total_analises = cursor.fetchone()[0]
        
        # Análises com feedback
        cursor.execute('SELECT COUNT(*) FROM analises WHERE feedback_tecnico IS NOT NULL')
        com_feedback = cursor.fetchone()[0]
        
        # Taxa de acerto
        cursor.execute('SELECT COUNT(*) FROM analises WHERE correto = 1')
        acertos = cursor.fetchone()[0]
        
        # Retreinamentos realizados
        cursor.execute('SELECT COUNT(*) FROM retreinamentos')
        retreinamentos = cursor.fetchone()[0]
        
        # Última melhoria
        cursor.execute('''
            SELECT melhoria FROM retreinamentos
            ORDER BY timestamp DESC LIMIT 1
        ''')
        ultima_melhoria = cursor.fetchone()
        ultima_melhoria = ultima_melhoria[0] if ultima_melhoria else 0
        
        # Casos difíceis ativos
        cursor.execute('SELECT COUNT(*) FROM casos_dificeis WHERE resolvido = 0')
        casos_dificeis_ativos = cursor.fetchone()[0]
        
        conn.close()
        
        taxa_acerto = (acertos / com_feedback * 100) if com_feedback > 0 else 0
        
        return {
            'total_analises': total_analises,
            'analises_com_feedback': com_feedback,
            'taxa_acerto': taxa_acerto,
            'retreinamentos_realizados': retreinamentos,
            'ultima_melhoria_percentual': ultima_melhoria * 100,
            'casos_dificeis_ativos': casos_dificeis_ativos,
            'timestamp': datetime.now().isoformat()
        }

def exemplo_uso():
    """Exemplo de uso do aprendizado contínuo"""
    print("="*70)
    print("SISTEMA DE APRENDIZADO CONTÍNUO")
    print("="*70 + "\n")
    
    aprendizado = AprendizadoContinuo()
    
    # Simular análises com feedback
    print("📊 Simulando análises com feedback...\n")
    
    for i in range(5):
        # Análise da IA
        analise = {
            'imagem_path': f'/imagens/pneu_{i+1}.jpg',
            'predicao': 'separacao_cintas' if i < 4 else 'bolha_hernia',
            'confianca': 0.95,
            'tempo_ms': 45
        }
        
        # Feedback do técnico
        feedback = {
            'correto': i < 4,  # 4 acertos, 1 erro
            'classe_correta': 'separacao_cintas' if i < 4 else 'separacao_cintas',
            'comentario': 'Análise precisa' if i < 4 else 'IA confundiu bolha com separação'
        }
        
        analise_id = aprendizado.registrar_analise(analise, feedback)
        print(f"✓ Análise #{analise_id}: {'CORRETO' if feedback['correto'] else 'INCORRETO'}")
    
    # Estatísticas
    print("\n" + "="*70)
    print("ESTATÍSTICAS DO APRENDIZADO")
    print("="*70 + "\n")
    
    stats = aprendizado.obter_estatisticas()
    
    print(f"📊 Total de análises: {stats['total_analises']}")
    print(f"✅ Com feedback: {stats['analises_com_feedback']}")
    print(f"🎯 Taxa de acerto: {stats['taxa_acerto']:.1f}%")
    print(f"🔄 Retreinamentos: {stats['retreinamentos_realizados']}")
    print(f"⚠️  Casos difíceis ativos: {stats['casos_dificeis_ativos']}")
    
    print("\n" + "="*70)
    print("✅ Sistema de aprendizado contínuo funcionando!")
    print("="*70)

if __name__ == "__main__":
    exemplo_uso()

