import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Eye } from 'lucide-react';
import axios from 'axios';
import { xbpneusClasses, xbpneusColors } from '../../styles/colors';

const RecapemListPage = () => {
  const [recapagens, setRecapagens] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchRecapagens();
  }, []);

  const fetchRecapagens = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await axios.get('/api/recapagem/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      setRecapagens(response.data.results || response.data || []);
    } catch (err) {
      console.error('Erro ao buscar recapagens:', err);
      setError(err.response?.data?.message || 'Erro ao carregar recapagens');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteRecapagem = async (id) => {
    if (window.confirm('Tem certeza que deseja deletar esta recapagem?')) {
      try {
        const token = localStorage.getItem('access_token');
        await axios.delete(`/api/recapagem/${id}/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        setSuccessMessage('Recapagem deletada com sucesso!');
        setRecapagens(recapagens.filter(r => r.id !== id));
        setTimeout(() => setSuccessMessage(null), 3000);
      } catch (err) {
        console.error('Erro ao deletar recapagem:', err);
        setError(err.response?.data?.message || 'Erro ao deletar recapagem');
      }
    }
  };

  const filteredRecapagens = recapagens.filter(recapagem => {
    return recapagem.nome_empresa?.toLowerCase().includes(searchTerm.toLowerCase()) ||
           recapagem.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
           recapagem.telefone?.includes(searchTerm);
  });

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Cabeçalho */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h1 className={`${xbpneusClasses.cardTitle} text-3xl mb-2`}>
                Gerenciamento de Recapagens
              </h1>
              <p className="text-gray-600">
                Gerencie as empresas de recapagem parceiras
              </p>
            </div>
            <button
              onClick={() => window.location.href = '/recapagem/novo'}
              className={`${xbpneusClasses.buttonPrimary} px-6 py-3 rounded-lg flex items-center gap-2`}
            >
              <Plus size={20} />
              Nova Recapagem
            </button>
          </div>
        </div>

        {/* Mensagens */}
        {successMessage && (
          <div className="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
            {successMessage}
          </div>
        )}
        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        {/* Filtros e Busca */}
        <div className={`${xbpneusClasses.card} p-6 mb-6`}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className={xbpneusClasses.inputLabel}>Buscar</label>
              <input
                type="text"
                placeholder="Nome, email ou telefone..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className={`${xbpneusClasses.input} w-full mt-1`}
              />
            </div>
            <div className="flex items-end">
              <button
                onClick={fetchRecapagens}
                className={`${xbpneusClasses.buttonPrimary} w-full px-4 py-2 rounded-lg`}
              >
                Atualizar
              </button>
            </div>
          </div>
        </div>

        {/* Tabela de Recapagens */}
        {loading ? (
          <div className="text-center py-12">
            <p className="text-gray-600">Carregando recapagens...</p>
          </div>
        ) : filteredRecapagens.length === 0 ? (
          <div className={`${xbpneusClasses.card} p-12 text-center`}>
            <p className="text-gray-600 mb-4">Nenhuma recapagem encontrada</p>
            <button
              onClick={() => window.location.href = '/recapagem/novo'}
              className={`${xbpneusClasses.buttonPrimary} px-6 py-2 rounded-lg inline-flex items-center gap-2`}
            >
              <Plus size={16} />
              Adicionar Recapagem
            </button>
          </div>
        ) : (
          <div className={xbpneusClasses.card}>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className={`${xbpneusColors.background.light} border-b`}>
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-semibold">Empresa</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold">Email</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold">Telefone</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold">Cidade</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold">Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredRecapagens.map((recapagem) => (
                    <tr key={recapagem.id} className="border-b hover:bg-gray-50">
                      <td className="px-6 py-4 text-sm">{recapagem.nome_empresa}</td>
                      <td className="px-6 py-4 text-sm">{recapagem.email}</td>
                      <td className="px-6 py-4 text-sm">{recapagem.telefone}</td>
                      <td className="px-6 py-4 text-sm">{recapagem.cidade}</td>
                      <td className="px-6 py-4 text-sm">
                        <div className="flex gap-2">
                          <button
                            onClick={() => window.location.href = `/recapagem/${recapagem.id}`}
                            className="p-2 text-blue-600 hover:bg-blue-100 rounded"
                            title="Visualizar"
                          >
                            <Eye size={16} />
                          </button>
                          <button
                            onClick={() => window.location.href = `/recapagem/${recapagem.id}/editar`}
                            className="p-2 text-green-600 hover:bg-green-100 rounded"
                            title="Editar"
                          >
                            <Edit size={16} />
                          </button>
                          <button
                            onClick={() => handleDeleteRecapagem(recapagem.id)}
                            className="p-2 text-red-600 hover:bg-red-100 rounded"
                            title="Deletar"
                          >
                            <Trash2 size={16} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecapemListPage;

