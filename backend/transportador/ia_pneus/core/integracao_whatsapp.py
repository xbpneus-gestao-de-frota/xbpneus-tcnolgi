#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Integração com WhatsApp Business API
Recebe fotos de pneus e processa automaticamente
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
from analise_imagem_garantia import AnalisadorImagemGarantia

class IntegracaoWhatsApp:
    """
    Integração com WhatsApp Business API para receber fotos de pneus
    e processar automaticamente análises de garantia
    """
    
    def __init__(self, config: Dict):
        """
        Inicializa a integração com WhatsApp
        
        Args:
            config: Configurações da API
                {
                    'phone_number_id': str,  # ID do número de telefone
                    'access_token': str,      # Token de acesso
                    'webhook_verify_token': str,  # Token de verificação
                    'numero_whatsapp': str,   # Número do WhatsApp (ex: +5547999999999)
                    'modo': str              # 'producao' ou 'desenvolvimento'
                }
        """
        self.config = config
        self.phone_number_id = config.get('phone_number_id', '')
        self.access_token = config.get('access_token', '')
        self.webhook_verify_token = config.get('webhook_verify_token', '')
        self.numero_whatsapp = config.get('numero_whatsapp', '+5547999999999')
        self.modo = config.get('modo', 'desenvolvimento')
        
        # URL base da API do WhatsApp Business
        self.api_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
        
        # Headers para requisições
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # Inicializar analisador de imagens
        self.analisador = AnalisadorImagemGarantia()
        
        # Diretório para salvar imagens recebidas
        self.dir_imagens = '/home/ubuntu/ia_analise_pneus/imagens_whatsapp'
        os.makedirs(self.dir_imagens, exist_ok=True)
        
        # Sessões de usuários (armazena contexto de conversas)
        self.sessoes = {}
    
    def processar_webhook(self, payload: Dict) -> Dict:
        """
        Processa webhook recebido do WhatsApp
        
        Args:
            payload: Dados do webhook
        
        Returns:
            Resposta processada
        """
        if self.modo == 'desenvolvimento':
            print(f"[WEBHOOK] Payload recebido: {json.dumps(payload, indent=2)}")
        
        # Verificar se é uma mensagem
        if 'entry' not in payload:
            return {'status': 'ignored', 'motivo': 'payload inválido'}
        
        for entry in payload['entry']:
            for change in entry.get('changes', []):
                if change.get('field') == 'messages':
                    value = change.get('value', {})
                    messages = value.get('messages', [])
                    
                    for message in messages:
                        return self._processar_mensagem(message, value)
        
        return {'status': 'processed'}
    
    def _processar_mensagem(self, message: Dict, value: Dict) -> Dict:
        """Processa uma mensagem individual"""
        msg_type = message.get('type')
        from_number = message.get('from')
        msg_id = message.get('id')
        
        # Obter ou criar sessão do usuário
        if from_number not in self.sessoes:
            self.sessoes[from_number] = {
                'imagens': [],
                'descricao': '',
                'dados_cliente': {},
                'iniciado_em': datetime.now().isoformat()
            }
        
        sessao = self.sessoes[from_number]
        
        # Processar baseado no tipo de mensagem
        if msg_type == 'text':
            texto = message.get('text', {}).get('body', '')
            return self._processar_texto(from_number, texto, sessao)
            
        elif msg_type == 'image':
            return self._processar_imagem(from_number, message, sessao)
        
        return {'status': 'tipo_nao_suportado', 'tipo': msg_type}
    
    def _processar_texto(self, from_number: str, texto: str, sessao: Dict) -> Dict:
        """Processa mensagem de texto"""
        texto_lower = texto.lower()
        
        # Comandos especiais
        if texto_lower in ['iniciar', 'começar', 'start']:
            self._enviar_mensagem(
                from_number,
                "🤖 *IA de Análise de Pneus - XBPNEUS*\n\n"
                "Olá! Sou a IA especializada em análise de pneus.\n\n"
                "📸 *Como funciona:*\n"
                "1. Envie fotos do pneu (banda, laterais, DOT, defeito)\n"
                "2. Descreva o problema\n"
                "3. Eu farei a análise e preencherei o formulário de garantia\n\n"
                "Envie as fotos para começar!"
            )
            return {'status': 'boas_vindas_enviadas'}
        
        elif texto_lower in ['ajuda', 'help']:
            self._enviar_mensagem(
                from_number,
                "📋 *Comandos disponíveis:*\n\n"
                "• *INICIAR* - Começar nova análise\n"
                "• *ANALISAR* - Processar fotos enviadas\n"
                "• *LIMPAR* - Limpar sessão atual\n"
                "• *STATUS* - Ver status da análise\n"
                "• *AJUDA* - Ver esta mensagem"
            )
            return {'status': 'ajuda_enviada'}
        
        elif texto_lower in ['analisar', 'processar']:
            return self._processar_analise_completa(from_number, sessao)
        
        elif texto_lower in ['limpar', 'reset']:
            self.sessoes[from_number] = {
                'imagens': [],
                'descricao': '',
                'dados_cliente': {},
                'iniciado_em': datetime.now().isoformat()
            }
            self._enviar_mensagem(from_number, "✅ Sessão limpa. Pode enviar novas fotos!")
            return {'status': 'sessao_limpa'}
        
        elif texto_lower == 'status':
            total_imgs = len(sessao['imagens'])
            self._enviar_mensagem(
                from_number,
                f"📊 *Status da Análise*\n\n"
                f"Imagens recebidas: {total_imgs}\n"
                f"Descrição: {'✓' if sessao['descricao'] else '✗'}\n\n"
                f"{'Pronto para análise! Digite ANALISAR' if total_imgs > 0 else 'Aguardando fotos...'}"
            )
            return {'status': 'status_enviado'}
        
        else:
            # Armazenar como descrição do problema
            sessao['descricao'] += f" {texto}"
            self._enviar_mensagem(
                from_number,
                "✅ Descrição registrada!\n\n"
                "Envie as fotos do pneu ou digite *ANALISAR* para processar."
            )
            return {'status': 'descricao_registrada'}
    
    def _processar_imagem(self, from_number: str, message: Dict, sessao: Dict) -> Dict:
        """Processa imagem recebida"""
        image_id = message.get('image', {}).get('id')
        caption = message.get('image', {}).get('caption', '')
        
        if self.modo == 'desenvolvimento':
            # Simular download de imagem
            img_path = os.path.join(
                self.dir_imagens,
                f"{from_number}_{len(sessao['imagens'])}_{image_id}.jpg"
            )
            
            # Criar arquivo vazio simulado
            with open(img_path, 'w') as f:
                f.write(f"Imagem simulada: {image_id}")
        else:
            # Baixar imagem real da API do WhatsApp
            img_path = self._baixar_imagem(image_id, from_number, len(sessao['imagens']))
        
        # Adicionar à sessão
        sessao['imagens'].append({
            'path': img_path,
            'id': image_id,
            'caption': caption,
            'timestamp': datetime.now().isoformat()
        })
        
        # Enviar confirmação
        total = len(sessao['imagens'])
        self._enviar_mensagem(
            from_number,
            f"✅ Imagem {total} recebida!\n\n"
            f"{'Continue enviando mais fotos ou digite *ANALISAR* para processar.' if total < 4 else '✨ Fotos suficientes! Digite *ANALISAR* para processar.'}"
        )
        
        return {'status': 'imagem_recebida', 'total_imagens': total}
    
    def _baixar_imagem(self, image_id: str, from_number: str, index: int) -> str:
        """Baixa imagem da API do WhatsApp"""
        # Obter URL da imagem
        url = f"https://graph.facebook.com/v18.0/{image_id}"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Erro ao obter URL da imagem: {response.status_code}")
        
        image_url = response.json().get('url')
        
        # Baixar imagem
        img_response = requests.get(image_url, headers=headers)
        if img_response.status_code != 200:
            raise Exception(f"Erro ao baixar imagem: {img_response.status_code}")
        
        # Salvar
        img_path = os.path.join(
            self.dir_imagens,
            f"{from_number}_{index}_{image_id}.jpg"
        )
        
        with open(img_path, 'wb') as f:
            f.write(img_response.content)
        
        return img_path
    
    def _processar_analise_completa(self, from_number: str, sessao: Dict) -> Dict:
        """Processa análise completa das imagens"""
        if not sessao['imagens']:
            self._enviar_mensagem(
                from_number,
                "⚠️ Nenhuma imagem recebida ainda.\n\nEnvie fotos do pneu primeiro!"
            )
            return {'status': 'sem_imagens'}
        
        # Enviar mensagem de processamento
        self._enviar_mensagem(
            from_number,
            "🔄 Processando análise...\n\nAguarde alguns instantes."
        )
        
        # Preparar dados para análise
        imagens_paths = [img['path'] for img in sessao['imagens']]
        contexto = {
            'numero_whatsapp': from_number,
            'descricao_usuario': sessao['descricao'],
            'total_imagens': len(imagens_paths),
            'data_recebimento': datetime.now().isoformat()
        }
        
        # Realizar análise
        analise = self.analisador.analisar_imagens_whatsapp(imagens_paths, contexto)
        
        # Gerar relatório
        output_dir = f'/home/ubuntu/ia_analise_pneus/relatorios/{from_number}'
        os.makedirs(output_dir, exist_ok=True)
        
        # Dados simulados do cliente (em produção, seria solicitado ou integrado)
        dados_completos = {
            'cliente': {
                'consumidor': {
                    'nome': 'Cliente via WhatsApp',
                    'telefone': from_number
                },
                'distribuidor': {
                    'nome': 'XBPNEUS',
                    'telefone': self.numero_whatsapp
                }
            },
            'produto': {
                'medida': 'A definir',
                'modelo': 'A definir',
                'marca': 'A definir'
            }
        }
        
        arquivos = self.analisador.gerar_relatorio_completo(
            analise,
            dados_completos,
            output_dir
        )
        
        # Enviar resultado
        diagnostico = analise['diagnostico_consolidado']
        problemas = diagnostico.get('problemas_principais', [])
        
        mensagem_resultado = (
            "✅ *Análise Concluída!*\n\n"
            f"📊 *Resultado:*\n"
            f"• Urgência: {analise['nivel_urgencia']}\n"
            f"• Problemas: {', '.join(problemas) if problemas else 'Nenhum crítico'}\n\n"
            f"📄 *Diagnóstico:*\n{diagnostico.get('descricao_tecnica', 'N/A')}\n\n"
            f"💡 *Recomendação:*\n{analise['recomendacao']}\n\n"
            f"📋 Formulário de garantia gerado!\n"
            f"Arquivo: {os.path.basename(arquivos['formulario_excel'])}"
        )
        
        self._enviar_mensagem(from_number, mensagem_resultado)
        
        # Limpar sessão
        self.sessoes[from_number] = {
            'imagens': [],
            'descricao': '',
            'dados_cliente': {},
            'iniciado_em': datetime.now().isoformat()
        }
        
        return {
            'status': 'analise_concluida',
            'arquivos': arquivos,
            'analise': analise
        }
    
    def _enviar_mensagem(self, to_number: str, texto: str) -> Dict:
        """Envia mensagem de texto via WhatsApp"""
        if self.modo == 'desenvolvimento':
            print(f"\n[WHATSAPP] Para: {to_number}")
            print(f"[WHATSAPP] Mensagem:\n{texto}\n")
            return {'status': 'enviado_simulado'}
        
        payload = {
            'messaging_product': 'whatsapp',
            'to': to_number,
            'type': 'text',
            'text': {'body': texto}
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                return {'status': 'enviado', 'response': response.json()}
            else:
                return {'status': 'erro', 'codigo': response.status_code}
        except Exception as e:
            return {'status': 'erro', 'mensagem': str(e)}
    
    def verificar_webhook(self, mode: str, token: str, challenge: str) -> Optional[str]:
        """
        Verifica webhook do WhatsApp (usado na configuração inicial)
        
        Returns:
            Challenge string se válido, None caso contrário
        """
        if mode == 'subscribe' and token == self.webhook_verify_token:
            return challenge
        return None

def exemplo_uso():
    """Exemplo de uso da integração WhatsApp"""
    print("="*70)
    print("INTEGRAÇÃO WHATSAPP - IA DE ANÁLISE DE PNEUS")
    print("="*70 + "\n")
    
    # Configuração
    config = {
        'phone_number_id': '123456789',
        'access_token': 'seu_token_aqui',
        'webhook_verify_token': 'seu_webhook_token',
        'numero_whatsapp': '+5547999999999',
        'modo': 'desenvolvimento'
    }
    
    # Inicializar integração
    whatsapp = IntegracaoWhatsApp(config)
    
    print(f"📱 Número WhatsApp configurado: {whatsapp.numero_whatsapp}")
    print(f"🔧 Modo: {whatsapp.modo}\n")
    
    # Simular recebimento de mensagens
    print("="*70)
    print("SIMULAÇÃO DE CONVERSAÇÃO")
    print("="*70 + "\n")
    
    # 1. Usuário inicia conversa
    print("👤 Usuário: INICIAR")
    payload1 = {
        'entry': [{
            'changes': [{
                'field': 'messages',
                'value': {
                    'messages': [{
                        'from': '+5547988887777',
                        'id': 'msg001',
                        'type': 'text',
                        'text': {'body': 'INICIAR'}
                    }]
                }
            }]
        }]
    }
    whatsapp.processar_webhook(payload1)
    
    # 2. Usuário envia descrição
    print("\n👤 Usuário: Pneu com desgaste irregular no centro")
    payload2 = {
        'entry': [{
            'changes': [{
                'field': 'messages',
                'value': {
                    'messages': [{
                        'from': '+5547988887777',
                        'id': 'msg002',
                        'type': 'text',
                        'text': {'body': 'Pneu com desgaste irregular no centro'}
                    }]
                }
            }]
        }]
    }
    whatsapp.processar_webhook(payload2)
    
    # 3. Usuário envia imagens
    print("\n👤 Usuário: [Envia 3 imagens]")
    for i in range(3):
        payload_img = {
            'entry': [{
                'changes': [{
                    'field': 'messages',
                    'value': {
                        'messages': [{
                            'from': '+5547988887777',
                            'id': f'msg00{i+3}',
                            'type': 'image',
                            'image': {
                                'id': f'img00{i+1}',
                                'caption': f'Foto {i+1}'
                            }
                        }]
                    }
                }]
            }]
        }
        whatsapp.processar_webhook(payload_img)
    
    # 4. Usuário solicita análise
    print("\n👤 Usuário: ANALISAR")
    payload4 = {
        'entry': [{
            'changes': [{
                'field': 'messages',
                'value': {
                    'messages': [{
                        'from': '+5547988887777',
                        'id': 'msg006',
                        'type': 'text',
                        'text': {'body': 'ANALISAR'}
                    }]
                }
            }]
        }]
    }
    resultado = whatsapp.processar_webhook(payload4)
    
    print("\n" + "="*70)
    print("✅ Integração WhatsApp funcionando!")
    print("="*70)
    print(f"\nStatus: {resultado.get('status')}")
    if 'arquivos' in resultado:
        print(f"Formulário gerado: {resultado['arquivos']['formulario_excel']}")

if __name__ == "__main__":
    exemplo_uso()

