import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function IAAnalise() {
  const [arquivo, setArquivo] = useState(null);
  const [tipoAnalise, setTipoAnalise] = useState('imagem');
  const [loading, setLoading] = useState(false);
  const [resultado, setResultado] = useState(null);
  const navigate = useNavigate();

  function handleFileChange(e) {
    const file = e.target.files[0];
    if (file) {
      setArquivo(file);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    
    if (!arquivo) {
      alert('Por favor, selecione um arquivo');
      return;
    }

    setLoading(true);
    
    try {
      const formData = new FormData();
      formData.append('arquivo', arquivo);
      formData.append('tipo_analise', tipoAnalise);

      // TODO: Implementar chamada à API
      // const response = await fetch('/api/transportador/ia/analises/analisar/', {
      //   method: 'POST',
      //   body: formData,
      //   headers: {
      //     'Authorization': `Bearer ${localStorage.getItem('token')}`
      //   }
      // });
      
      // const data = await response.json();
      // setResultado(data);
      
      // Simulação
      setTimeout(() => {
        setResultado({
          status: 'concluído',
          precisao: 98.5,
          defeitos: [
            { tipo: 'Desgaste irregular', gravidade: 'Médio', confianca: 95 },
            { tipo: 'Pressão baixa', gravidade: 'Baixo', confianca: 88 }
          ],
          recomendacao: 'Recomenda-se calibrar o pneu e verificar alinhamento do veículo.'
        });
        setLoading(false);
      }, 2000);
      
    } catch (error) {
      console.error('Erro ao analisar:', error);
      alert('Erro ao processar análise');
      setLoading(false);
    }
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
          📸 Nova Análise de Pneu
        </h1>
        <p className="text-gray-600">
          Faça upload de imagem, vídeo ou áudio para análise inteligente
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Formulário de Upload */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <form onSubmit={handleSubmit}>
            {/* Tipo de Análise */}
            <div className="mb-6">
              <label className="block text-gray-700 font-semibold mb-2">
                Tipo de Análise
              </label>
              <select
                value={tipoAnalise}
                onChange={(e) => setTipoAnalise(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="imagem">📸 Imagem</option>
                <option value="video">🎥 Vídeo 360°</option>
                <option value="audio">🔊 Áudio</option>
              </select>
            </div>

            {/* Upload de Arquivo */}
            <div className="mb-6">
              <label className="block text-gray-700 font-semibold mb-2">
                Arquivo
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors">
                <input
                  type="file"
                  onChange={handleFileChange}
                  accept={tipoAnalise === 'imagem' ? 'image/*' : tipoAnalise === 'video' ? 'video/*' : 'audio/*'}
                  className="hidden"
                  id="file-upload"
                />
                <label
                  htmlFor="file-upload"
                  className="cursor-pointer"
                >
                  {arquivo ? (
                    <div>
                      <div className="text-4xl mb-2">✅</div>
                      <p className="text-gray-700 font-semibold">{arquivo.name}</p>
                      <p className="text-gray-500 text-sm mt-1">
                        {(arquivo.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  ) : (
                    <div>
                      <div className="text-4xl mb-2">📁</div>
                      <p className="text-gray-700 font-semibold">
                        Clique para selecionar arquivo
                      </p>
                      <p className="text-gray-500 text-sm mt-1">
                        ou arraste e solte aqui
                      </p>
                    </div>
                  )}
                </label>
              </div>
            </div>

            {/* Botão de Envio */}
            <button
              type="submit"
              disabled={loading || !arquivo}
              className={`w-full py-3 rounded-lg font-semibold text-white transition-colors ${
                loading || !arquivo
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700'
              }`}
            >
              {loading ? '🔄 Analisando...' : '🚀 Iniciar Análise'}
            </button>
          </form>

          {/* Informações */}
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-800">
              <strong>💡 Dica:</strong> Para melhores resultados, tire fotos nítidas
              e bem iluminadas do pneu. Para vídeos, grave uma volta completa de 360°.
            </p>
          </div>
        </div>

        {/* Resultado da Análise */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            📊 Resultado da Análise
          </h2>

          {!resultado && !loading && (
            <div className="text-center py-12 text-gray-400">
              <div className="text-6xl mb-4">🤖</div>
              <p>Aguardando análise...</p>
            </div>
          )}

          {loading && (
            <div className="text-center py-12">
              <div className="text-6xl mb-4 animate-spin">⚙️</div>
              <p className="text-gray-600">Processando com IA...</p>
              <div className="mt-4 w-full bg-gray-200 rounded-full h-2">
                <div className="bg-blue-600 h-2 rounded-full animate-pulse" style={{width: '60%'}}></div>
              </div>
            </div>
          )}

          {resultado && (
            <div>
              {/* Precisão */}
              <div className="mb-6 p-4 bg-green-50 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="text-gray-700 font-semibold">Precisão da Análise</span>
                  <span className="text-2xl font-bold text-green-600">
                    {resultado.precisao}%
                  </span>
                </div>
              </div>

              {/* Defeitos Encontrados */}
              <div className="mb-6">
                <h3 className="font-semibold text-gray-800 mb-3">
                  ⚠️ Defeitos Encontrados
                </h3>
                {resultado.defeitos.map((defeito, index) => (
                  <div
                    key={index}
                    className="mb-3 p-4 border border-gray-200 rounded-lg"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold text-gray-800">
                        {defeito.tipo}
                      </span>
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                        defeito.gravidade === 'Alto' ? 'bg-red-100 text-red-800' :
                        defeito.gravidade === 'Médio' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {defeito.gravidade}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">
                      Confiança: {defeito.confianca}%
                    </p>
                  </div>
                ))}
              </div>

              {/* Recomendação */}
              <div className="p-4 bg-blue-50 rounded-lg">
                <h3 className="font-semibold text-blue-800 mb-2">
                  💡 Recomendação
                </h3>
                <p className="text-blue-700">
                  {resultado.recomendacao}
                </p>
              </div>

              {/* Ações */}
              <div className="mt-6 flex space-x-3">
                <button
                  onClick={() => navigate('/transportador/ia/garantias/nova')}
                  className="flex-1 bg-purple-600 hover:bg-purple-700 text-white py-2 rounded-lg font-semibold transition-colors"
                >
                  🛡️ Abrir Garantia
                </button>
                <button
                  onClick={() => {
                    setResultado(null);
                    setArquivo(null);
                  }}
                  className="flex-1 bg-gray-600 hover:bg-gray-700 text-white py-2 rounded-lg font-semibold transition-colors"
                >
                  🔄 Nova Análise
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

