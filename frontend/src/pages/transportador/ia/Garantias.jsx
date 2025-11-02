import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function IAGarantias() {
  const [garantias, setGarantias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filtro, setFiltro] = useState('todas');
  const navigate = useNavigate();

  useEffect(() => {
    fetchGarantias();
  }, []);

  async function fetchGarantias() {
    try {
      // TODO: Implementar chamada à API
      // Simulação
      setGarantias([
        {
          id: 1,
          protocolo: 'GAR-2025-001',
          status: 'aprovada',
          data_abertura: '2025-10-01',
          defeito: 'Desgaste irregular',
          hash_blockchain: 'a3f5d9e2...'
        },
        {
          id: 2,
          protocolo: 'GAR-2025-002',
          status: 'em_analise',
          data_abertura: '2025-10-05',
          defeito: 'Separação de cintas',
          hash_blockchain: 'b7c2e1f8...'
        },
        {
          id: 3,
          protocolo: 'GAR-2025-003',
          status: 'aberta',
          data_abertura: '2025-10-08',
          defeito: 'Bolha lateral',
          hash_blockchain: 'c9d4a6b3...'
        }
      ]);
      setLoading(false);
    } catch (error) {
      console.error('Erro ao carregar garantias:', error);
      setLoading(false);
    }
  }

  function getStatusColor(status) {
    const cores = {
      aberta: 'bg-blue-100 text-blue-800',
      em_analise: 'bg-yellow-100 text-yellow-800',
      aprovada: 'bg-green-100 text-green-800',
      negada: 'bg-red-100 text-red-800'
    };
    return cores[status] || cores.aberta;
  }

  function getStatusLabel(status) {
    const labels = {
      aberta: 'Aberta',
      em_analise: 'Em Análise',
      aprovada: 'Aprovada',
      negada: 'Negada'
    };
    return labels[status] || 'Desconhecido';
  }

  const garantiasFiltradas = filtro === 'todas'
    ? garantias
    : garantias.filter(g => g.status === filtro);

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
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">
              🛡️ Gestão de Garantias
            </h1>
            <p className="text-gray-600">
              Gerencie garantias com segurança blockchain
            </p>
          </div>
          <button
            onClick={() => navigate('/transportador/ia/garantias/nova')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
          >
            + Nova Garantia
          </button>
        </div>
      </div>

      {/* Filtros */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="flex space-x-4">
          <button
            onClick={() => setFiltro('todas')}
            className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
              filtro === 'todas'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Todas ({garantias.length})
          </button>
          <button
            onClick={() => setFiltro('aberta')}
            className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
              filtro === 'aberta'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Abertas ({garantias.filter(g => g.status === 'aberta').length})
          </button>
          <button
            onClick={() => setFiltro('em_analise')}
            className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
              filtro === 'em_analise'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Em Análise ({garantias.filter(g => g.status === 'em_analise').length})
          </button>
          <button
            onClick={() => setFiltro('aprovada')}
            className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
              filtro === 'aprovada'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Aprovadas ({garantias.filter(g => g.status === 'aprovada').length})
          </button>
        </div>
      </div>

      {/* Lista de Garantias */}
      <div className="space-y-4">
        {garantiasFiltradas.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="text-6xl mb-4">📋</div>
            <p className="text-gray-600">Nenhuma garantia encontrada</p>
          </div>
        ) : (
          garantiasFiltradas.map((garantia) => (
            <div
              key={garantia.id}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-3">
                    <h3 className="text-xl font-bold text-gray-800">
                      {garantia.protocolo}
                    </h3>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(garantia.status)}`}>
                      {getStatusLabel(garantia.status)}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div>
                      <p className="text-sm text-gray-500">Data de Abertura</p>
                      <p className="font-semibold text-gray-800">
                        {new Date(garantia.data_abertura).toLocaleDateString('pt-BR')}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Defeito</p>
                      <p className="font-semibold text-gray-800">{garantia.defeito}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Hash Blockchain</p>
                      <p className="font-mono text-sm text-blue-600">{garantia.hash_blockchain}</p>
                    </div>
                  </div>

                  {/* Blockchain Badge */}
                  <div className="inline-flex items-center space-x-2 bg-purple-50 px-3 py-1 rounded-full">
                    <span className="text-purple-600">🔗</span>
                    <span className="text-sm text-purple-800 font-semibold">
                      Registrado na Blockchain
                    </span>
                  </div>
                </div>

                <div className="flex flex-col space-y-2 ml-4">
                  <button
                    onClick={() => navigate(`/transportador/ia/garantias/${garantia.id}`)}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
                  >
                    Ver Detalhes
                  </button>
                  <button
                    className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
                  >
                    Verificar Hash
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Informações sobre Blockchain */}
      <div className="mt-8 bg-purple-50 rounded-lg p-6">
        <h3 className="font-bold text-purple-800 mb-3 flex items-center">
          <span className="text-2xl mr-2">🔒</span>
          Segurança com Blockchain
        </h3>
        <p className="text-purple-700 mb-4">
          Todas as garantias são registradas em blockchain, garantindo:
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex items-start space-x-2">
            <span className="text-xl">✅</span>
            <div>
              <p className="font-semibold text-purple-800">Imutabilidade</p>
              <p className="text-sm text-purple-600">Registros não podem ser alterados</p>
            </div>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-xl">✅</span>
            <div>
              <p className="font-semibold text-purple-800">Transparência</p>
              <p className="text-sm text-purple-600">Auditoria completa disponível</p>
            </div>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-xl">✅</span>
            <div>
              <p className="font-semibold text-purple-800">Segurança</p>
              <p className="text-sm text-purple-600">Proteção contra fraudes</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

