import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Eye } from 'lucide-react';
import axios from 'axios';
import { xbpneusClasses, xbpneusColors } from '../../styles/colors';

const MotoristasListPage = () => {
  const [motoristas, setMotoristas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('todos');

  useEffect(() => {
    fetchMotoristas();
  }, []);

  const fetchMotoristas = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await axios.get('/api/motorista/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      setMotoristas(response.data.results || response.data || []);
    } catch (err) {
      console.error('Erro ao buscar motoristas:', err);
      setError(err.response?.data?.message || 'Erro ao carregar motoristas');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteMotorista = async (id) => {
    if (window.confirm('Tem certeza que deseja deletar este motorista?')) {
      try {
        const token = localStorage.getItem('access_token');
        await axios.delete(`/api/motorista/${id}/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        setSuccessMessage('Motorista deletado com sucesso!');
        setMotoristas(motoristas.filter(m => m.id !== id));
        setTimeout(() => setSuccessMessage(null), 3000);
      } catch (err) {
        console.error('Erro ao deletar motorista:', err);
        setError(err.response?.data?.message || 'Erro ao deletar motorista');
      }
    }
  };

  const filteredMotoristas = motoristas.filter(motorista => {
    const matchesSearch = motorista.nome_completo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         motorista.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         motorista.telefone?.includes(searchTerm);
    
    if (filterStatus === 'todos') return matchesSearch;
    if (filterStatus === 'ativo') return matchesSearch && motorista.ativo;
    if (filterStatus === 'inativo') return matchesSearch && !motorista.ativo;
    
    return matchesSearch;
  });

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Cabeçalho */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h1 className={`${xbpneusClasses.cardTitle} text-3xl mb-2`}>
                Gerenciamento de Motoristas
              </h1>
              <p className="text-gray-600">
                Gerencie os motoristas da sua frota
              </p>
            </div>
            <button
              onClick={() => window.location.href = '/motorista/novo'}
              className={`${xbpneusClasses.buttonPrimary} px-6 py-3 rounded-lg flex items-center gap-2`}
            >
              <Plus size={20} />
              Novo Motorista
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
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
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
            <div>
              <label className={xbpneusClasses.inputLabel}>Status</label>
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className={`${xbpneusClasses.input} w-full mt-1`}
              >
                <option value="todos">Todos</option>
                <option value="ativo">Ativos</option>
                <option value="inativo">Inativos</option>
              </select>
            </div>
            <div className="flex items-end">
              <button
                onClick={fetchMotoristas}
                className={`${xbpneusClasses.buttonPrimary} w-full px-4 py-2 rounded-lg`}
              >
                Atualizar
              </button>
            </div>
          </div>
        </div>

        {/* Tabela de Motoristas */}
        {loading ? (
          <div className="text-center py-12">
            <p className="text-gray-600">Carregando motoristas...</p>
          </div>
        ) : filteredMotoristas.length === 0 ? (
          <div className={`${xbpneusClasses.card} p-12 text-center`}>
            <p className="text-gray-600 mb-4">Nenhum motorista encontrado</p>
            <button
              onClick={() => window.location.href = '/motorista/novo'}
              className={`${xbpneusClasses.buttonPrimary} px-6 py-2 rounded-lg inline-flex items-center gap-2`}
            >
              <Plus size={16} />
              Adicionar Motorista
            </button>
          </div>
        ) : (
          <div className={xbpneusClasses.card}>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className={`${xbpneusColors.background.light} border-b`}>
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-semibold">Nome</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold">Email</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold">Telefone</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold">Status</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold">Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredMotoristas.map((motorista) => (
                    <tr key={motorista.id} className="border-b hover:bg-gray-50">
                      <td className="px-6 py-4 text-sm">{motorista.nome_completo}</td>
                      <td className="px-6 py-4 text-sm">{motorista.email}</td>
                      <td className="px-6 py-4 text-sm">{motorista.telefone}</td>
                      <td className="px-6 py-4 text-sm">
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                          motorista.ativo
                            ? xbpneusClasses.badgeSuccess
                            : xbpneusClasses.badgeWarning
                        }`}>
                          {motorista.ativo ? 'Ativo' : 'Inativo'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <div className="flex gap-2">
                          <button
                            onClick={() => window.location.href = `/motorista/${motorista.id}`}
                            className="p-2 text-blue-600 hover:bg-blue-100 rounded"
                            title="Visualizar"
                          >
                            <Eye size={16} />
                          </button>
                          <button
                            onClick={() => window.location.href = `/motorista/${motorista.id}/editar`}
                            className="p-2 text-green-600 hover:bg-green-100 rounded"
                            title="Editar"
                          >
                            <Edit size={16} />
                          </button>
                          <button
                            onClick={() => handleDeleteMotorista(motorista.id)}
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

export default MotoristasListPage;

