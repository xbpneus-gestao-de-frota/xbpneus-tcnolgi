#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processamento de Linguagem Natural Avançado com GPT-4
Chatbot inteligente que entende contexto complexo
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime

class PLNAvancado:
    """
    Sistema avançado de PLN usando GPT-4 para interação natural
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o sistema de PLN
        
        Args:
            api_key: Chave da API OpenAI
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.modelo = 'gpt-4.1-mini'
        
        # Histórico de conversação
        self.historico_conversas = {}
        
        # Contexto do sistema
        self.system_prompt = """Você é um assistente especializado em análise de pneus de carga, com 30 anos de experiência técnica.

Suas características:
- Extremamente técnico e preciso
- Empático e prestativo
- Explica conceitos complexos de forma simples
- Faz perguntas relevantes para diagnóstico preciso
- Prioriza a segurança acima de tudo
- Conhece profundamente: marcas, modelos, especificações, defeitos, manutenção

Seu objetivo:
- Ajudar a diagnosticar problemas em pneus
- Coletar informações relevantes
- Fornecer recomendações técnicas precisas
- Educar sobre manutenção preventiva
- Identificar situações de risco

Sempre:
- Use emojis para tornar a conversa mais amigável
- Seja direto em situações de risco
- Pergunte uma coisa de cada vez
- Confirme entendimento antes de prosseguir
- Forneça explicações técnicas quando relevante"""
    
    def iniciar_conversa(self, usuario_id: str) -> Dict:
        """
        Inicia nova conversa com usuário
        
        Args:
            usuario_id: ID único do usuário
        
        Returns:
            Resposta inicial
        """
        self.historico_conversas[usuario_id] = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        mensagem_inicial = """👋 Olá! Sou o assistente especializado em análise de pneus.

Estou aqui para te ajudar a:
• 🔍 Diagnosticar problemas
• 📸 Analisar fotos de pneus
• 💡 Dar recomendações técnicas
• 🛡️ Garantir sua segurança

Como posso te ajudar hoje?"""
        
        return {
            'mensagem': mensagem_inicial,
            'usuario_id': usuario_id,
            'timestamp': datetime.now().isoformat()
        }
    
    def processar_mensagem(self, usuario_id: str, mensagem: str, contexto: Optional[Dict] = None) -> Dict:
        """
        Processa mensagem do usuário com PLN avançado
        
        Args:
            usuario_id: ID do usuário
            mensagem: Mensagem do usuário
            contexto: Contexto adicional (análises, dados, etc)
        
        Returns:
            Resposta do assistente
        """
        try:
            # Inicializar conversa se necessário
            if usuario_id not in self.historico_conversas:
                self.iniciar_conversa(usuario_id)
            
            # Adicionar contexto se fornecido
            mensagem_completa = mensagem
            if contexto:
                mensagem_completa = self._enriquecer_com_contexto(mensagem, contexto)
            
            # Adicionar mensagem ao histórico
            self.historico_conversas[usuario_id].append({
                "role": "user",
                "content": mensagem_completa
            })
            
            # Obter resposta do GPT-4
            try:
                if self.api_key and self.api_key != 'sua_chave_api_aqui':
                    resposta = self._chamar_gpt4(usuario_id)
                else:
                    resposta = self._resposta_simulada(mensagem, contexto)
            except Exception as e:
                print(f"Erro ao gerar resposta: {e}")
                resposta = self._resposta_simulada(mensagem, contexto)
            
            # Adicionar resposta ao histórico
            self.historico_conversas[usuario_id].append({
                "role": "assistant",
                "content": resposta
            })
            
            # Analisar intenção e extrair entidades
            intencao = self._analisar_intencao(mensagem)
            entidades = self._extrair_entidades(mensagem)
            
            return {
                'mensagem': resposta,
                'intencao': intencao,
                'entidades': entidades,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Erro geral: {e}")
            return {
                'erro': str(e),
                'mensagem': 'Desculpe, tive um problema ao processar sua mensagem. Pode reformular?',
                'timestamp': datetime.now().isoformat()
            }
    
    def _chamar_gpt4(self, usuario_id: str) -> str:
        """
        Chama GPT-4 para gerar resposta
        """
        try:
            from openai import OpenAI
            
            client = OpenAI()
            
            response = client.chat.completions.create(
                model=self.modelo,
                messages=self.historico_conversas[usuario_id],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Erro ao chamar GPT-4: {e}")
    
    def _resposta_simulada(self, mensagem: str, contexto: Optional[Dict]) -> str:
        """
        Gera resposta simulada inteligente
        """
        mensagem_lower = mensagem.lower()
        
        # Saudações
        if any(palavra in mensagem_lower for palavra in ['oi', 'olá', 'bom dia', 'boa tarde', 'boa noite']):
            return """👋 Olá! Prazer em ajudar!

Para fazer uma análise completa, vou precisar de algumas informações:

📸 Você já tem fotos do pneu?
Se sim, pode enviar agora. Se não, sem problema, podemos começar com uma descrição."""
        
        # Problema/defeito
        elif any(palavra in mensagem_lower for palavra in ['problema', 'defeito', 'dano', 'furado']):
            return """🔍 Entendi que há um problema com o pneu.

Para te ajudar melhor, preciso saber:

1️⃣ **Onde** está o problema? (banda de rodagem, lateral, etc)
2️⃣ **O que** você está vendo? (corte, bolha, desgaste, etc)
3️⃣ **Quando** notou o problema?

Pode descrever com suas palavras, vou entender! 😊"""
        
        # Desgaste
        elif 'desgaste' in mensagem_lower:
            if 'irregular' in mensagem_lower or 'desigual' in mensagem_lower:
                return """⚙️ Desgaste irregular é um sinal importante!

Geralmente indica problemas mecânicos:
• 🔧 Desalinhamento
• 🔩 Suspensão defeituosa  
• 💨 Pressão incorreta

**Onde está o desgaste?**
• No centro da banda?
• Nas laterais (ombros)?
• Mais de um lado?

Isso me ajuda a identificar a causa exata."""
            else:
                return """📊 Vamos avaliar o desgaste do pneu.

**Perguntas importantes:**
1️⃣ Qual a profundidade atual do sulco? (em mm)
2️⃣ O desgaste é uniforme ou irregular?
3️⃣ Quantos km o pneu já rodou?

💡 *Dica:* Use um profundímetro ou régua para medir."""
        
        # Bolha/hérnia
        elif any(palavra in mensagem_lower for palavra in ['bolha', 'hernia', 'inchaço', 'protuberância']):
            return """🚨 **ATENÇÃO: Bolha é um defeito GRAVE!**

Uma bolha indica que a estrutura interna do pneu está comprometida.

⚠️ **RISCO:** O pneu pode estourar a qualquer momento!

**Ação imediata:**
1️⃣ NÃO trafegue em alta velocidade
2️⃣ Substitua o pneu URGENTEMENTE
3️⃣ Tire fotos para possível garantia

**Pergunta importante:**
O veículo sofreu algum impacto recente? (meio-fio, buraco profundo?)

Isso determina se é defeito de fabricação ou uso."""
        
        # Garantia
        elif 'garantia' in mensagem_lower:
            return """📋 Sobre **garantia de pneus**:

**Defeitos cobertos:**
✅ Separação de cintas
✅ Bolhas sem impacto
✅ Defeitos de fabricação
✅ Falhas estruturais

**NÃO cobertos:**
❌ Cortes e perfurações
❌ Desgaste irregular por desalinhamento
❌ Danos por impacto
❌ Envelhecimento natural

**Para solicitar garantia, preciso:**
📸 Fotos claras do defeito
📸 Foto do código DOT
📄 Nota fiscal (se tiver)

Você tem essas informações?"""
        
        # Pressão
        elif 'pressão' in mensagem_lower or 'calibra' in mensagem_lower:
            return """💨 **Pressão correta é ESSENCIAL!**

**Problemas de pressão incorreta:**

🔻 **Pressão BAIXA:**
• Desgaste nos ombros
• Maior consumo de combustível
• Risco de dano estrutural

🔺 **Pressão ALTA:**
• Desgaste no centro
• Menos aderência
• Dirigibilidade comprometida

**Qual a pressão atual do seu pneu?**
E você sabe qual é a pressão recomendada?

💡 *Dica:* A pressão recomendada está na porta do motorista ou manual."""
        
        # Recapagem
        elif 'recapa' in mensagem_lower:
            return """♻️ **Recapagem de pneus:**

**Pode recapar quando:**
✅ Estrutura interna íntegra
✅ Sem cortes profundos
✅ Sem bolhas ou separações
✅ Carcaça em bom estado

**NÃO pode recapar:**
❌ Defeitos estruturais
❌ Separação de cintas
❌ Múltiplas recapagens anteriores
❌ Idade superior a 10 anos

**Seu pneu:**
• Tem algum defeito estrutural?
• Já foi recapado antes?
• Quantos km rodou?

Com essas infos posso te dizer se vale a pena recapar."""
        
        # Resposta genérica inteligente
        else:
            return """🤔 Entendi sua mensagem.

Para te ajudar da melhor forma, pode me contar:

• 📸 Você tem fotos do pneu?
• 🔍 Qual é a sua principal preocupação?
• 🚛 É para qual tipo de veículo?

Quanto mais detalhes, melhor posso te ajudar! 😊"""
    
    def _enriquecer_com_contexto(self, mensagem: str, contexto: Dict) -> str:
        """
        Enriquece mensagem com contexto adicional
        """
        contexto_str = f"\n\n[CONTEXTO ADICIONAL]\n"
        
        if 'analise_imagem' in contexto:
            analise = contexto['analise_imagem']
            contexto_str += f"Análise de imagem realizada:\n"
            contexto_str += f"- Defeito: {analise.get('nome_defeito', 'N/A')}\n"
            contexto_str += f"- Severidade: {analise.get('severidade', 'N/A')}\n"
            contexto_str += f"- Confiança: {analise.get('confianca', 0):.1%}\n"
        
        if 'dados_pneu' in contexto:
            dados = contexto['dados_pneu']
            contexto_str += f"Dados do pneu:\n"
            contexto_str += f"- Marca/Modelo: {dados.get('marca_modelo', 'N/A')}\n"
            contexto_str += f"- KM Rodados: {dados.get('km_rodados', 'N/A')}\n"
            contexto_str += f"- Posição: {dados.get('posicao', 'N/A')}\n"
        
        return mensagem + contexto_str
    
    def _analisar_intencao(self, mensagem: str) -> str:
        """
        Analisa intenção do usuário
        """
        mensagem_lower = mensagem.lower()
        
        if any(palavra in mensagem_lower for palavra in ['oi', 'olá', 'bom dia']):
            return 'saudacao'
        elif any(palavra in mensagem_lower for palavra in ['problema', 'defeito', 'dano']):
            return 'relatar_problema'
        elif any(palavra in mensagem_lower for palavra in ['garantia', 'reclamar']):
            return 'solicitar_garantia'
        elif any(palavra in mensagem_lower for palavra in ['quanto custa', 'preço', 'valor']):
            return 'consultar_preco'
        elif any(palavra in mensagem_lower for palavra in ['como', 'quando', 'por que']):
            return 'pedir_explicacao'
        elif any(palavra in mensagem_lower for palavra in ['recapa', 'reformar']):
            return 'consultar_recapagem'
        else:
            return 'geral'
    
    def _extrair_entidades(self, mensagem: str) -> Dict:
        """
        Extrai entidades da mensagem
        """
        entidades = {
            'marca': None,
            'modelo': None,
            'medida': None,
            'posicao': None,
            'problema': None,
            'km': None
        }
        
        mensagem_lower = mensagem.lower()
        
        # Marcas comuns
        marcas = ['michelin', 'bridgestone', 'goodyear', 'pirelli', 'continental', 'xbri', 'vipal']
        for marca in marcas:
            if marca in mensagem_lower:
                entidades['marca'] = marca.title()
        
        # Medidas (padrão: 295/80R22.5)
        import re
        medida_match = re.search(r'\d{3}/\d{2}R\d{2}\.?\d?', mensagem)
        if medida_match:
            entidades['medida'] = medida_match.group()
        
        # Posição
        if 'dianteiro' in mensagem_lower:
            entidades['posicao'] = 'DIRECAO'
        elif 'traseiro' in mensagem_lower or 'tração' in mensagem_lower:
            entidades['posicao'] = 'TRACAO'
        elif 'reboque' in mensagem_lower:
            entidades['posicao'] = 'REBOQUE'
        
        # Problemas
        problemas = ['bolha', 'corte', 'desgaste', 'rachadura', 'separação', 'furado']
        for problema in problemas:
            if problema in mensagem_lower:
                entidades['problema'] = problema
        
        # Quilometragem
        km_match = re.search(r'(\d+\.?\d*)\s*(mil|k|km)', mensagem_lower)
        if km_match:
            valor = float(km_match.group(1).replace('.', ''))
            if 'mil' in km_match.group(2) or 'k' in km_match.group(2):
                valor *= 1000
            entidades['km'] = int(valor)
        
        return entidades
    
    def gerar_relatorio_conversa(self, usuario_id: str) -> Dict:
        """
        Gera relatório da conversa
        """
        if usuario_id not in self.historico_conversas:
            return {'erro': 'Conversa não encontrada'}
        
        historico = self.historico_conversas[usuario_id]
        
        # Contar mensagens (excluir system prompt)
        msgs_usuario = len([m for m in historico if m.get('role') == 'user'])
        msgs_assistente = len([m for m in historico if m.get('role') == 'assistant'])
        
        # Extrair todas as entidades mencionadas
        todas_entidades = {}
        for msg in historico:
            if msg['role'] == 'user':
                entidades = self._extrair_entidades(msg['content'])
                for chave, valor in entidades.items():
                    if valor and not todas_entidades.get(chave):
                        todas_entidades[chave] = valor
        
        return {
            'usuario_id': usuario_id,
            'total_mensagens': len(historico) - 1,  # -1 para excluir system prompt
            'mensagens_usuario': msgs_usuario,
            'mensagens_assistente': msgs_assistente,
            'entidades_extraidas': todas_entidades,
            'timestamp': datetime.now().isoformat()
        }

def exemplo_uso():
    """Exemplo de uso do PLN avançado"""
    print("="*70)
    print("PROCESSAMENTO DE LINGUAGEM NATURAL AVANÇADO COM GPT-4")
    print("="*70 + "\n")
    
    pln = PLNAvancado()
    usuario_id = "usuario_teste_001"
    
    # Iniciar conversa
    print("🤖 INICIANDO CONVERSA")
    print("-" * 70)
    resposta = pln.iniciar_conversa(usuario_id)
    print(resposta['mensagem'])
    
    # Simular conversa
    mensagens_usuario = [
        "Oi, preciso de ajuda com um pneu",
        "Tem uma bolha na lateral do pneu",
        "É um Michelin 295/80R22.5 no eixo dianteiro",
        "Não lembro de ter batido em nada"
    ]
    
    for msg in mensagens_usuario:
        print(f"\n\n👤 Usuário: {msg}")
        print("-" * 70)
        
        resposta = pln.processar_mensagem(usuario_id, msg)
        print(f"🤖 Assistente: {resposta['mensagem']}")
        
        if resposta.get('entidades'):
            ent = resposta['entidades']
            ent_encontradas = {k: v for k, v in ent.items() if v}
            if ent_encontradas:
                print(f"\n📊 Entidades extraídas: {ent_encontradas}")
    
    # Gerar relatório
    print("\n\n" + "="*70)
    print("RELATÓRIO DA CONVERSA")
    print("="*70)
    
    relatorio = pln.gerar_relatorio_conversa(usuario_id)
    print(f"\n📊 Total de mensagens: {relatorio['total_mensagens']}")
    print(f"👤 Mensagens do usuário: {relatorio['mensagens_usuario']}")
    print(f"🤖 Mensagens do assistente: {relatorio['mensagens_assistente']}")
    print(f"\n📋 Informações coletadas:")
    for chave, valor in relatorio['entidades_extraidas'].items():
        if valor:
            print(f"   • {chave.title()}: {valor}")
    
    print("\n" + "="*70)
    print("✅ Sistema de PLN avançado funcionando!")
    print("="*70)

if __name__ == "__main__":
    exemplo_uso()

