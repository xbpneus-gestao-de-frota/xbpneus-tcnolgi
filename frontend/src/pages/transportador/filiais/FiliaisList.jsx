import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Plus, MapPin, Edit, Trash2 } from 'lucide-react';
import api from '../../../api/http';

export default function FiliaisList() {
  const [filiais, setFiliais] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [selectedEmpresa, setSelectedEmpresa] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchEmpresas();
  }, []);

  useEffect(() => {
    if (selectedEmpresa) {
      fetchFiliais();
    } else {
      fetchFiliais();
    }
  }, [selectedEmpresa]);

  const fetchEmpresas = async () => {
    try {
      const response = await api.get('/api/empresas/');
      setEmpresas(response.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchFiliais = async () => {
    try {
      setLoading(true);
      const url = selectedEmpresa
        ? `/api/filiais/?empresa_id=${selectedEmpresa}`
        : '/api/filiais/';
      const response = await api.get(url);
      setFiliais(response.data);
      setError(null);
    } catch (err) {
      setError('Erro ao carregar filiais');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Tem certeza que deseja excluir esta filial?')) {
      return;
    }

    try {
      await api.delete(`/api/filiais/${id}/`);
      fetchFiliais();
    } catch (err) {
      alert('Erro ao excluir filial');
      console.error(err);
    }
  };

  const getTipoLabel = (tipo) => {
    const tipos = {
      OPERACIONAL: 'Operacional',
      ADMINISTRATIVO: 'Administrativo',
      OFICINA_INTERNA: 'Oficina Interna',
      PONTO_APOIO: 'Ponto de Apoio',
    };
    return tipos[tipo] || tipo;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Filiais / Unidades</h1>
          <p className="text-gray-600 mt-1">Gerencie as filiais das empresas</p>
        </div>
        <Link
          to="/dashboard/filiais/create"
          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-5 h-5 mr-2" />
          Nova Filial
        </Link>
      </div>

      {/* Filtro por Empresa */}
      <div className="bg-white rounded-lg shadow p-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Filtrar por Empresa
        </label>
        <select
          value={selectedEmpresa}
          onChange={(e) => setSelectedEmpresa(e.target.value)}
          className="w-full md:w-64 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">Todas as Empresas</option>
          {empresas.map((empresa) => (
            <option key={empresa.id} value={empresa.id}>
              {empresa.nome_fantasia || empresa.razao_social}
            </option>
          ))}
        </select>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Filial
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Empresa
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Tipo
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Cidade/UF
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Contato
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Ações
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filiais.length === 0 ? (
              <tr>
                <td colSpan="7" className="px-6 py-12 text-center text-gray-500">
                  <MapPin className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                  <p>Nenhuma filial cadastrada</p>
                </td>
              </tr>
            ) : (
              filiais.map((filial) => (
                <tr key={filial.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="flex items-center">
                      <MapPin className="w-5 h-5 text-gray-400 mr-3" />
                      <div>
                        <div className="text-sm font-medium text-gray-900">{filial.nome}</div>
                        <div className="text-sm text-gray-500">Código: {filial.codigo}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {filial.empresa_matriz_nome || `Empresa #${filial.empresa_matriz}`}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {getTipoLabel(filial.tipo)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {filial.cidade}/{filial.uf}
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-gray-900">{filial.telefone}</div>
                    <div className="text-sm text-gray-500">{filial.email}</div>
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        filial.ativo
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {filial.ativo ? 'Ativo' : 'Inativo'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right text-sm font-medium space-x-2">
                    <Link
                      to={`/dashboard/filiais/${filial.id}/edit`}
                      className="inline-flex items-center text-blue-600 hover:text-blue-900"
                    >
                      <Edit className="w-4 h-4" />
                    </Link>
                    <button
                      onClick={() => handleDelete(filial.id)}
                      className="inline-flex items-center text-red-600 hover:text-red-900"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

