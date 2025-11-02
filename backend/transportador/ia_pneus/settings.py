"""
Configurações do módulo de IA
"""
import os
from pathlib import Path

# Diretório base do módulo
BASE_DIR = Path(__file__).resolve().parent

# Configurações da IA
IA_CONFIG = {
    # OpenAI API
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', ''),
    
    # Caminhos
    'MODEL_PATH': BASE_DIR / 'models',
    'DATABASE_PATH': BASE_DIR / 'database',
    
    # Funcionalidades
    'ENABLE_LEARNING': os.getenv('IA_ENABLE_LEARNING', 'True') == 'True',
    'ENABLE_GAMIFICATION': os.getenv('IA_ENABLE_GAMIFICATION', 'True') == 'True',
    'ENABLE_BLOCKCHAIN': os.getenv('IA_ENABLE_BLOCKCHAIN', 'True') == 'True',
    
    # Limites
    'MAX_FILE_SIZE': 10 * 1024 * 1024,  # 10MB
    'MAX_VIDEO_DURATION': 60,  # segundos
}

