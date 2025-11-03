#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
Chatbot Avançado com Perguntas Contextuais e Linguagem Natural
"""

from typing import Dict, List, Optional
from datetime import datetime
import json

class ChatbotAvancado:
    """
    Chatbot inteligente que faz perguntas contextuais para coletar
    informações completas sobre o pneu
    """
    
    def __init__(self):
        # Estados da conversação
        self.estados = {
            'INICIAL': 'inicial',
            'COLETANDO_BASICO': 'coletando_basico',
            'ANALISANDO_FOTOS': 'analisando_fotos',
            'COLETANDO_DETALHES': 'coletando_detalhes',
            'CONFIRMANDO': 'confirmando',
            'FINALIZANDO': 'finalizando'
        }
        
        # Perguntas contextuais organizadas por categoria
        self.perguntas = {
            'identificacao': [
                {
                    'pergunta': '📋 Qual é a **marca e modelo** do pneu?',
                    'campo': 'marca_modelo',
                    'tipo': 'texto',
                    'exemplo': 'Ex: Michelin XZE2+, Bridgestone R268, etc.'
                },
                {
                    'pergunta': '📏 Qual a **medida** do pneu?',
                    'campo': 'medida',
                    'tipo': 'texto',
                    'exemplo': 'Ex: 295/80R22.5, 275/80R22.5, etc.'
                },
                {
                    'pergunta': '🏷️ Você consegue ver o código **DOT** no pneu?',
                    'campo': 'dot',
                    'tipo': 'texto',
                    'opcional': True,
                    'exemplo': 'Ex: 2421 (semana 24 de 2021)'
                }
            ],
            'uso': [
                {
                    'pergunta': '🚛 Em qual **posição** o pneu está instalado?',
                    'campo': 'posicao',
                    'tipo': 'opcao',
                    'opcoes': ['Dianteiro Esquerdo', 'Dianteiro Direito', 'Traseiro Esquerdo', 'Traseiro Direito', 'Reboque'],
                    'mapeamento': {
                        'dianteiro': 'DIRECAO',
                        'traseiro': 'TRACAO',
                        'reboque': 'REBOQUE'
                    }
                },
                {
                    'pergunta': '📊 Quantos **quilômetros** o pneu já rodou (aproximadamente)?',
                    'campo': 'km_rodados',
                    'tipo': 'numero',
                    'exemplo': 'Ex: 45000'
                },
                {
                    'pergunta': '🛣️ Qual o **tipo de estrada** predominante?',
                    'campo': 'tipo_estrada',
                    'tipo': 'opcao',
                    'opcoes': ['Asfalto', 'Terra', 'Pedras', 'Mista (asfalto + terra)']
                }
            ],
            'condicao': [
                {
                    'pergunta': '💨 Qual a **pressão atual** do pneu (em PSI)?',
                    'campo': 'pressao_atual',
                    'tipo': 'numero',
                    'exemplo': 'Ex: 110, 120, etc.',
                    'opcional': True
                },
                {
                    'pergunta': '📐 Qual a **profundidade do sulco** (em mm)?',
                    'campo': 'profundidade_sulco',
                    'tipo': 'numero',
                    'exemplo': 'Ex: 8.5, 12.0, etc.',
                    'opcional': True,
                    'ajuda': 'Use um profundímetro ou régua'
                },
                {
                    'pergunta': '⚖️ O veículo costuma rodar com **sobrecarga**?',
                    'campo': 'sobrecarga',
                    'tipo': 'opcao',
                    'opcoes': ['Não', 'Às vezes', 'Frequentemente']
                }
            ],
            'problema': [
                {
                    'pergunta': '🔍 Descreva o **problema** que você está observando:',
                    'campo': 'descricao_problema',
                    'tipo': 'texto_longo',
                    'exemplo': 'Ex: Desgaste no centro, corte na lateral, bolha, etc.'
                },
                {
                    'pergunta': '📅 **Quando** você notou o problema?',
                    'campo': 'quando_notou',
                    'tipo': 'opcao',
                    'opcoes': ['Hoje', 'Esta semana', 'Este mês', 'Há mais tempo']
                },
                {
                    'pergunta': '⚡ O problema está **piorando**?',
                    'campo': 'piorando',
                    'tipo': 'opcao',
                    'opcoes': ['Sim, rapidamente', 'Sim, aos poucos', 'Não, está estável', 'Não sei']
                }
            ]
        }
    
    def iniciar_conversa(self) -> Dict:
        """
        Inicia uma nova conversa
        """
        return {
            'estado': self.estados['INICIAL'],
            'dados_coletados': {},
            'perguntas_respondidas': [],
            'proxima_pergunta': None,
            'mensagem': self._gerar_mensagem_boas_vindas()
        }
    
    def _gerar_mensagem_boas_vindas(self) -> str:
        """
        Gera mensagem de boas-vindas personalizada
        """
        return """🤖 *Olá! Sou o assistente inteligente de análise de pneus.*

Vou te ajudar a analisar o pneu e preencher o formulário de garantia.

Para fazer uma análise completa, vou precisar de:
📸 **Fotos do pneu** (quanto mais, melhor!)
📋 **Algumas informações** sobre o pneu e seu uso

*Como funciona:*
1️⃣ Envie as fotos do pneu
2️⃣ Responda algumas perguntas rápidas
3️⃣ Receba o diagnóstico e formulário pronto!

📸 **Comece enviando as fotos do pneu agora!**

*Dica:* Tire fotos da banda de rodagem, laterais, código DOT e do defeito (se houver)."""
    
    def processar_resposta(self, sessao: Dict, resposta: str, tipo_entrada: str = 'texto') -> Dict:
        """
        Processa resposta do usuário e determina próxima ação
        
        Args:
            sessao: Estado atual da sessão
            resposta: Resposta do usuário
            tipo_entrada: 'texto', 'imagem', 'opcao'
        
        Returns:
            Sessão atualizada com próxima ação
        """
        estado_atual = sessao.get('estado', self.estados['INICIAL'])
        
        if tipo_entrada == 'imagem':
            return self._processar_imagem(sessao)
        
        elif estado_atual == self.estados['INICIAL']:
            return self._iniciar_coleta(sessao)
        
        elif estado_atual == self.estados['COLETANDO_BASICO']:
            return self._coletar_informacao_basica(sessao, resposta)
        
        elif estado_atual == self.estados['ANALISANDO_FOTOS']:
            return self._processar_analise_fotos(sessao, resposta)
        
        elif estado_atual == self.estados['COLETANDO_DETALHES']:
            return self._coletar_detalhes(sessao, resposta)
        
        elif estado_atual == self.estados['CONFIRMANDO']:
            return self._confirmar_dados(sessao, resposta)
        
        return sessao
    
    def _processar_imagem(self, sessao: Dict) -> Dict:
        """
        Processa recebimento de imagem
        """
        total_imagens = len(sessao.get('imagens', []))
        
        if total_imagens == 1:
            mensagem = """✅ *Primeira foto recebida!*

📸 **Envie mais fotos** para uma análise completa:
• Banda de rodagem (vista de cima)
• Lateral esquerda
• Lateral direita  
• Código DOT
• Defeito específico (se houver)

Ou digite *CONTINUAR* se já enviou todas as fotos."""
        
        elif total_imagens < 4:
            mensagem = f"""✅ *{total_imagens} fotos recebidas!*

Continue enviando mais fotos ou digite *CONTINUAR* para prosseguir."""
        
        else:
            mensagem = f"""✅ *{total_imagens} fotos recebidas - Ótimo!*

Agora vou fazer algumas perguntas rápidas para completar a análise.

Digite *CONTINUAR* quando estiver pronto."""
            sessao['estado'] = self.estados['ANALISANDO_FOTOS']
        
        sessao['mensagem'] = mensagem
        return sessao
    
    def _iniciar_coleta(self, sessao: Dict) -> Dict:
        """
        Inicia coleta de informações básicas
        """
        sessao['estado'] = self.estados['COLETANDO_BASICO']
        sessao['categoria_atual'] = 'identificacao'
        sessao['indice_pergunta'] = 0
        
        return self._fazer_proxima_pergunta(sessao)
    
    def _coletar_informacao_basica(self, sessao: Dict, resposta: str) -> Dict:
        """
        Coleta informações básicas do pneu
        """
        # Salvar resposta anterior
        if 'pergunta_atual' in sessao:
            campo = sessao['pergunta_atual']['campo']
            sessao['dados_coletados'][campo] = resposta
            sessao['perguntas_respondidas'].append(campo)
        
        # Próxima pergunta
        return self._fazer_proxima_pergunta(sessao)
    
    def _fazer_proxima_pergunta(self, sessao: Dict) -> Dict:
        """
        Determina e faz a próxima pergunta contextual
        """
        categoria = sessao.get('categoria_atual', 'identificacao')
        indice = sessao.get('indice_pergunta', 0)
        
        perguntas_categoria = self.perguntas.get(categoria, [])
        
        # Se ainda há perguntas nesta categoria
        if indice < len(perguntas_categoria):
            pergunta = perguntas_categoria[indice]
            sessao['pergunta_atual'] = pergunta
            sessao['indice_pergunta'] = indice + 1
            
            # Gerar mensagem da pergunta
            mensagem = pergunta['pergunta']
            
            if 'exemplo' in pergunta:
                mensagem += f"\n\n💡 {pergunta['exemplo']}"
            
            if pergunta.get('opcional'):
                mensagem += "\n\n_(Digite PULAR se não souber)_"
            
            if pergunta.get('tipo') == 'opcao':
                mensagem += "\n\n*Opções:*\n"
                for i, opcao in enumerate(pergunta['opcoes'], 1):
                    mensagem += f"{i}. {opcao}\n"
            
            sessao['mensagem'] = mensagem
            return sessao
        
        # Passar para próxima categoria
        categorias = list(self.perguntas.keys())
        idx_atual = categorias.index(categoria)
        
        if idx_atual < len(categorias) - 1:
            # Próxima categoria
            sessao['categoria_atual'] = categorias[idx_atual + 1]
            sessao['indice_pergunta'] = 0
            return self._fazer_proxima_pergunta(sessao)
        else:
            # Todas as perguntas respondidas
            return self._finalizar_coleta(sessao)
    
    def _processar_analise_fotos(self, sessao: Dict, resposta: str) -> Dict:
        """
        Processa comando para analisar fotos
        """
        if resposta.upper() in ['CONTINUAR', 'SIM', 'OK']:
            return self._iniciar_coleta(sessao)
        else:
            sessao['mensagem'] = "Digite *CONTINUAR* quando estiver pronto para prosseguir."
            return sessao
    
    def _coletar_detalhes(self, sessao: Dict, resposta: str) -> Dict:
        """
        Coleta detalhes adicionais baseado na análise
        """
        # Lógica para perguntas contextuais baseadas nas fotos
        return sessao
    
    def _confirmar_dados(self, sessao: Dict, resposta: str) -> Dict:
        """
        Confirma dados coletados com o usuário
        """
        if resposta.upper() in ['SIM', 'CONFIRMAR', 'OK']:
            sessao['estado'] = self.estados['FINALIZANDO']
            sessao['mensagem'] = """✅ *Dados confirmados!*

🔄 Processando análise completa...

Aguarde alguns instantes."""
        else:
            sessao['mensagem'] = "Digite *SIM* para confirmar ou *CORRIGIR* para alterar alguma informação."
        
        return sessao
    
    def _finalizar_coleta(self, sessao: Dict) -> Dict:
        """
        Finaliza coleta e prepara para análise
        """
        sessao['estado'] = self.estados['CONFIRMANDO']
        
        # Gerar resumo dos dados coletados
        resumo = self._gerar_resumo_dados(sessao['dados_coletados'])
        
        sessao['mensagem'] = f"""📋 *Resumo das Informações Coletadas:*

{resumo}

*Está tudo correto?*
Digite *SIM* para confirmar ou *CORRIGIR* para alterar."""
        
        return sessao
    
    def _gerar_resumo_dados(self, dados: Dict) -> str:
        """
        Gera resumo formatado dos dados coletados
        """
        resumo = ""
        
        if 'marca_modelo' in dados:
            resumo += f"🏷️ Marca/Modelo: {dados['marca_modelo']}\n"
        if 'medida' in dados:
            resumo += f"📏 Medida: {dados['medida']}\n"
        if 'posicao' in dados:
            resumo += f"🚛 Posição: {dados['posicao']}\n"
        if 'km_rodados' in dados:
            resumo += f"📊 KM Rodados: {dados['km_rodados']}\n"
        if 'tipo_estrada' in dados:
            resumo += f"🛣️ Tipo de Estrada: {dados['tipo_estrada']}\n"
        if 'descricao_problema' in dados:
            resumo += f"🔍 Problema: {dados['descricao_problema']}\n"
        
        return resumo if resumo else "Nenhum dado coletado ainda."
    
    def gerar_pergunta_contextual(self, analise_fotos: Dict, dados_parciais: Dict) -> Optional[str]:
        """
        Gera pergunta contextual baseada na análise das fotos
        
        Args:
            analise_fotos: Resultado da análise de imagens
            dados_parciais: Dados já coletados
        
        Returns:
            Pergunta contextual ou None
        """
        # Se detectou desgaste irregular, perguntar sobre manutenção
        if 'desgaste_irregular' in analise_fotos.get('problemas', []):
            if 'ultima_manutencao' not in dados_parciais:
                return """🔧 Notei um desgaste irregular no pneu.

**Quando foi a última vez** que o veículo passou por manutenção (alinhamento, balanceamento)?

Isso me ajuda a identificar a causa do problema."""
        
        # Se detectou pressão baixa, perguntar sobre calibragem
        if analise_fotos.get('pressao_aparente') == 'baixa':
            if 'frequencia_calibragem' not in dados_parciais:
                return """💨 O pneu parece estar com pressão baixa.

**Com que frequência** você calibra os pneus?

1. Semanalmente
2. Quinzenalmente  
3. Mensalmente
4. Raramente"""
        
        # Se detectou defeito estrutural, perguntar sobre impactos
        if 'defeito_estrutural' in analise_fotos.get('tipo_problema', ''):
            if 'impacto_recente' not in dados_parciais:
                return """⚠️ Detectei um possível dano estrutural.

**O veículo sofreu algum impacto recentemente?**
(batida em meio-fio, buraco profundo, etc.)

Isso é importante para determinar se é defeito de fabricação ou uso."""
        
        return None
    
    def sugerir_proximo_passo(self, sessao: Dict) -> str:
        """
        Sugere próximo passo baseado no contexto
        """
        total_imagens = len(sessao.get('imagens', []))
        dados = sessao.get('dados_coletados', {})
        
        if total_imagens == 0:
            return "📸 Envie fotos do pneu para começar a análise."
        
        elif total_imagens < 3:
            return "📸 Envie mais fotos para uma análise mais precisa."
        
        elif not dados.get('marca_modelo'):
            return "📋 Me informe a marca e modelo do pneu."
        
        elif not dados.get('km_rodados'):
            return "📊 Me informe quantos km o pneu já rodou."
        
        else:
            return "✅ Pronto para análise! Digite ANALISAR."

def exemplo_uso():
    """Exemplo de uso do chatbot avançado"""
    print("="*70)
    print("CHATBOT AVANÇADO COM PERGUNTAS CONTEXTUAIS")
    print("="*70 + "\n")
    
    chatbot = ChatbotAvancado()
    
    # Iniciar conversa
    print("🤖 INICIANDO CONVERSA")
    print("-" * 70)
    sessao = chatbot.iniciar_conversa()
    print(sessao['mensagem'])
    
    # Simular recebimento de fotos
    print("\n\n👤 [Usuário envia 3 fotos]")
    print("-" * 70)
    sessao['imagens'] = ['foto1.jpg', 'foto2.jpg', 'foto3.jpg']
    sessao = chatbot._processar_imagem(sessao)
    print(sessao['mensagem'])
    
    # Simular início da coleta
    print("\n\n👤 Usuário: CONTINUAR")
    print("-" * 70)
    sessao = chatbot.processar_resposta(sessao, 'CONTINUAR', 'texto')
    print(sessao['mensagem'])
    
    # Simular resposta
    print("\n\n👤 Usuário: Michelin XZE2+")
    print("-" * 70)
    sessao = chatbot.processar_resposta(sessao, 'Michelin XZE2+', 'texto')
    print(sessao['mensagem'])
    
    print("\n" + "="*70)
    print("✅ Chatbot avançado funcionando!")
    print("="*70)

if __name__ == "__main__":
    exemplo_uso()

