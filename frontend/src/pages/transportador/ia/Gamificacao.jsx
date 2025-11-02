import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function IAGamificacao() {
  const [perfil, setPerfil] = useState({
    pontos: 0,
    nivel: 'bronze',
    conquistas: [],
    posicao_ranking: 0
  });
  const [ranking, setRanking] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchGamificacao();
  }, []);

  async function fetchGamificacao() {
    try {
      // TODO: Implementar chamada à API
      // Simulação
      setPerfil({
        pontos: 1250,
        nivel: 'ouro',
        conquistas: [
          { id: 1, nome: 'Primeiro Passo', descricao: 'Primeira análise realizada', icone: '🎯' },
          { id: 2, nome: 'Cuidadoso', descricao: '10 análises realizadas', icone: '🏆' },
          { id: 3, nome: 'Especialista', descricao: '50 análises realizadas', icone: '⭐' }
        ],
        posicao_ranking: 3
      });

      setRanking([
        { posicao: 1, usuario: 'João Silva', pontos: 2500, nivel: 'platina' },
        { posicao: 2, usuario: 'Maria Santos', pontos: 1800, nivel: 'ouro' },
        { posicao: 3, usuario: 'Você', pontos: 1250, nivel: 'ouro' },
        { posicao: 4, usuario: 'Pedro Costa', pontos: 980, nivel: 'prata' },
        { posicao: 5, usuario: 'Ana Lima', pontos: 750, nivel: 'prata' }
      ]);

      setLoading(false);
    } catch (error) {
      console.error('Erro ao carregar gamificação:', error);
      setLoading(false);
    }
  }

  function getNivelColor(nivel) {
    const cores = {
      bronze: 'bg-orange-100 text-orange-800 border-orange-300',
      prata: 'bg-gray-100 text-gray-800 border-gray-300',
      ouro: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      platina: 'bg-purple-100 text-purple-800 border-purple-300'
    };
    return cores[nivel] || cores.bronze;
  }

  function getNivelIcon(nivel) {
    const icones = {
      bronze: '🥉',
      prata: '🥈',
      ouro: '🥇',
      platina: '💎'
    };
    return icones[nivel] || '🥉';
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
        <button
          onClick={() => navigate('/transportador/ia')}
          className="text-blue-600 hover:text-blue-800 mb-4 flex items-center"
        >
          ← Voltar ao Dashboard
        </button>
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          🎮 Gamificação
        </h1>
        <p className="text-gray-600">
          Acompanhe sua pontuação, conquistas e ranking
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Perfil do Usuário */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <div className="text-center">
              <div className="text-6xl mb-4">{getNivelIcon(perfil.nivel)}</div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Seu Perfil</h2>
              <div className={`inline-block px-4 py-2 rounded-full border-2 ${getNivelColor(perfil.nivel)} font-semibold mb-4`}>
                Nível {perfil.nivel.charAt(0).toUpperCase() + perfil.nivel.slice(1)}
              </div>
              <div className="text-4xl font-bold text-blue-600 mb-2">
                {perfil.pontos}
              </div>
              <p className="text-gray-600">pontos acumulados</p>
            </div>

            {/* Barra de Progresso */}
            <div className="mt-6">
              <div className="flex justify-between text-sm text-gray-600 mb-2">
                <span>Progresso para Platina</span>
                <span>62%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div className="bg-purple-600 h-3 rounded-full" style={{width: '62%'}}></div>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                Faltam 750 pontos para o próximo nível
              </p>
            </div>

            {/* Posição no Ranking */}
            <div className="mt-6 p-4 bg-blue-50 rounded-lg text-center">
              <p className="text-sm text-blue-800 mb-1">Sua Posição</p>
              <p className="text-3xl font-bold text-blue-600">#{perfil.posicao_ranking}</p>
            </div>
          </div>

          {/* Como Ganhar Pontos */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="font-bold text-gray-800 mb-4">💡 Como Ganhar Pontos</h3>
            <div className="space-y-3">
              <div className="flex items-start space-x-3">
                <span className="text-xl">📸</span>
                <div>
                  <p className="font-semibold text-sm">Análise de Imagem</p>
                  <p className="text-xs text-gray-600">+50 pontos</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <span className="text-xl">🎥</span>
                <div>
                  <p className="font-semibold text-sm">Análise de Vídeo</p>
                  <p className="text-xs text-gray-600">+100 pontos</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <span className="text-xl">🛡️</span>
                <div>
                  <p className="font-semibold text-sm">Garantia Aprovada</p>
                  <p className="text-xs text-gray-600">+200 pontos</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <span className="text-xl">🎯</span>
                <div>
                  <p className="font-semibold text-sm">Precisão Alta</p>
                  <p className="text-xs text-gray-600">+25 pontos bônus</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Conquistas e Ranking */}
        <div className="lg:col-span-2">
          {/* Conquistas */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              🏆 Conquistas Desbloqueadas
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {perfil.conquistas.map((conquista) => (
                <div
                  key={conquista.id}
                  className="border-2 border-green-300 bg-green-50 rounded-lg p-4"
                >
                  <div className="flex items-start space-x-3">
                    <span className="text-3xl">{conquista.icone}</span>
                    <div>
                      <h3 className="font-bold text-green-800">{conquista.nome}</h3>
                      <p className="text-sm text-green-700">{conquista.descricao}</p>
                    </div>
                  </div>
                </div>
              ))}

              {/* Conquistas Bloqueadas */}
              <div className="border-2 border-gray-300 bg-gray-50 rounded-lg p-4 opacity-50">
                <div className="flex items-start space-x-3">
                  <span className="text-3xl">🔒</span>
                  <div>
                    <h3 className="font-bold text-gray-600">Mestre</h3>
                    <p className="text-sm text-gray-500">100 análises realizadas</p>
                  </div>
                </div>
              </div>

              <div className="border-2 border-gray-300 bg-gray-50 rounded-lg p-4 opacity-50">
                <div className="flex items-start space-x-3">
                  <span className="text-3xl">🔒</span>
                  <div>
                    <h3 className="font-bold text-gray-600">Lenda</h3>
                    <p className="text-sm text-gray-500">Alcançar nível Platina</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Ranking */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              📊 Ranking Geral
            </h2>
            <div className="space-y-3">
              {ranking.map((item) => (
                <div
                  key={item.posicao}
                  className={`flex items-center justify-between p-4 rounded-lg ${
                    item.usuario === 'Você'
                      ? 'bg-blue-50 border-2 border-blue-300'
                      : 'bg-gray-50'
                  }`}
                >
                  <div className="flex items-center space-x-4">
                    <div className={`text-2xl font-bold ${
                      item.posicao === 1 ? 'text-yellow-500' :
                      item.posicao === 2 ? 'text-gray-400' :
                      item.posicao === 3 ? 'text-orange-500' :
                      'text-gray-600'
                    }`}>
                      #{item.posicao}
                    </div>
                    <div>
                      <p className={`font-semibold ${
                        item.usuario === 'Você' ? 'text-blue-800' : 'text-gray-800'
                      }`}>
                        {item.usuario}
                      </p>
                      <span className={`text-xs px-2 py-1 rounded-full ${getNivelColor(item.nivel)}`}>
                        {item.nivel}
                      </span>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold text-gray-800">{item.pontos}</p>
                    <p className="text-xs text-gray-500">pontos</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

