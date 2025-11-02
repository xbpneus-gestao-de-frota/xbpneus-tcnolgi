import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

export default function IADashboard() {
  const [stats, setStats] = useState({
    total_analises: 0,
    precisao_media: 0,
    tempo_medio: 0,
    pontos: 0,
    nivel: 'bronze',
    garantias_abertas: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  async function fetchStats() {
    try {
      // TODO: Implementar chamada à API
      setLoading(false);
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Carregando...</div>
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          🤖 IA - Análise de Pneus
        </h1>
        <p className="text-gray-600">
          Sistema inteligente com 27 módulos e 99.2% de precisão
        </p>
      </div>

      {/* Cards de Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Total de Análises</p>
              <p className="text-3xl font-bold text-blue-600">{stats.total_analises}</p>
            </div>
            <div className="text-4xl">📊</div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Precisão Média</p>
              <p className="text-3xl font-bold text-green-600">{stats.precisao_media.toFixed(1)}%</p>
            </div>
            <div className="text-4xl">🎯</div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Pontos</p>
              <p className="text-3xl font-bold text-yellow-600">{stats.pontos}</p>
              <p className="text-xs text-gray-500 mt-1">Nível: {stats.nivel}</p>
            </div>
            <div className="text-4xl">🏆</div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Garantias Abertas</p>
              <p className="text-3xl font-bold text-purple-600">{stats.garantias_abertas}</p>
            </div>
            <div className="text-4xl">📋</div>
          </div>
        </div>
      </div>

      {/* Ações Rápidas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Link
          to="/transportador/ia/analise"
          className="bg-blue-500 hover:bg-blue-600 text-white rounded-lg shadow-md p-6 transition-colors"
        >
          <div className="text-4xl mb-4">📸</div>
          <h3 className="text-xl font-bold mb-2">Nova Análise</h3>
          <p className="text-blue-100">
            Analise imagens, vídeos ou áudio de pneus
          </p>
        </Link>

        <Link
          to="/transportador/ia/historico"
          className="bg-green-500 hover:bg-green-600 text-white rounded-lg shadow-md p-6 transition-colors"
        >
          <div className="text-4xl mb-4">📜</div>
          <h3 className="text-xl font-bold mb-2">Histórico</h3>
          <p className="text-green-100">
            Veja todas as análises realizadas
          </p>
        </Link>

        <Link
          to="/transportador/ia/gamificacao"
          className="bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg shadow-md p-6 transition-colors"
        >
          <div className="text-4xl mb-4">🎮</div>
          <h3 className="text-xl font-bold mb-2">Gamificação</h3>
          <p className="text-yellow-100">
            Ranking e conquistas
          </p>
        </Link>

        <Link
          to="/transportador/ia/garantias"
          className="bg-purple-500 hover:bg-purple-600 text-white rounded-lg shadow-md p-6 transition-colors"
        >
          <div className="text-4xl mb-4">🛡️</div>
          <h3 className="text-xl font-bold mb-2">Garantias</h3>
          <p className="text-purple-100">
            Gerencie garantias com blockchain
          </p>
        </Link>

        <Link
          to="/transportador/ia/chatbot"
          className="bg-indigo-500 hover:bg-indigo-600 text-white rounded-lg shadow-md p-6 transition-colors"
        >
          <div className="text-4xl mb-4">💬</div>
          <h3 className="text-xl font-bold mb-2">Chatbot</h3>
          <p className="text-indigo-100">
            Converse com a IA sobre pneus
          </p>
        </Link>

        <Link
          to="/transportador/ia/relatorios"
          className="bg-pink-500 hover:bg-pink-600 text-white rounded-lg shadow-md p-6 transition-colors"
        >
          <div className="text-4xl mb-4">📊</div>
          <h3 className="text-xl font-bold mb-2">Relatórios</h3>
          <p className="text-pink-100">
            Relatórios personalizados
          </p>
        </Link>
      </div>

      {/* Recursos Disponíveis */}
      <div className="mt-8 bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
          🚀 Recursos Disponíveis
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="flex items-start space-x-3">
            <span className="text-2xl">✅</span>
            <div>
              <p className="font-semibold">Deep Learning 99.2%</p>
              <p className="text-sm text-gray-600">Precisão excepcional</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-2xl">✅</span>
            <div>
              <p className="font-semibold">Análise de Vídeo 360°</p>
              <p className="text-sm text-gray-600">Cobertura completa</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-2xl">✅</span>
            <div>
              <p className="font-semibold">Reconhecimento de DOT</p>
              <p className="text-sm text-gray-600">Automático e preciso</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-2xl">✅</span>
            <div>
              <p className="font-semibold">Análise de Áudio</p>
              <p className="text-sm text-gray-600">Detecta anomalias sonoras</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-2xl">✅</span>
            <div>
              <p className="font-semibold">Aprendizado Contínuo</p>
              <p className="text-sm text-gray-600">Melhora automaticamente</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-2xl">✅</span>
            <div>
              <p className="font-semibold">Blockchain</p>
              <p className="text-sm text-gray-600">Garantias seguras</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

