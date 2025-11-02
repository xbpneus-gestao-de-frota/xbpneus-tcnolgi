import React, { useState, useEffect } from 'react';
import { ArrowLeft, Edit, Trash2 } from 'lucide-react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { xbpneusClasses, xbpneusColors } from '../../styles/colors';

const MotoristasDetailPage = () => {
  const { id } = useParams();
  const [motorista, setMotorista] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMotorista();
  }, [id]);

  const fetchMotorista = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await axios.get(`/api/motorista/${id}/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      setMotorista(response.data);
    } catch (err) {
      console.error('Erro ao buscar motorista:', err);
      setError(err.response?.data?.message || 'Erro ao carregar motorista');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Tem certeza que deseja deletar este motorista?')) {
      try {
        const token = localStorage.getItem('access_token');
        await axios.delete(`/api/motorista/${id}/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        window.location.href = '/motorista';
      } catch (err) {
        console.error('Erro ao deletar motorista:', err);
        setError(err.response?.data?.message || 'Erro ao deletar motorista');
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-6 flex items-center justify-center">
        <p className="text-gray-600">Carregando motorista...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto">
          <button
            onClick={() => window.location.href = '/motorista'}
            className={`${xbpneusClasses.buttonSecondary} px-4 py-2 rounded-lg flex items-center gap-2 mb-4`}
          >
            <ArrowLeft size={16} />
            Voltar
          </button>
          <div className={`${xbpneusClasses.card} p-6`}>
            <p className="text-red-600">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Cabeçalho */}
        <div className="mb-8">
          <button
            onClick={() => window.location.href = '/motorista'}
            className={`${xbpneusClasses.buttonSecondary} px-4 py-2 rounded-lg flex items-center gap-2 mb-4`}
          >
            <ArrowLeft size={16} />
            Voltar
          </button>
          <div className="flex justify-between items-start">
            <div>
              <h1 className={`${xbpneusClasses.cardTitle} text-3xl mb-2`}>
                {motorista?.nome_completo}
              </h1>
              <p className="text-gray-600">
                Detalhes do motorista
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => window.location.href = `/motorista/${id}/editar`}
                className={`${xbpneusClasses.buttonPrimary} px-4 py-2 rounded-lg flex items-center gap-2`}
              >
                <Edit size={16} />
                Editar
              </button>
              <button
                onClick={handleDelete}
                className="bg-red-100 text-red-700 hover:bg-red-200 px-4 py-2 rounded-lg flex items-center gap-2"
              >
                <Trash2 size={16} />
                Deletar
              </button>
            </div>
          </div>
        </div>

        {/* Informações Pessoais */}
        <div className={`${xbpneusClasses.card} p-6 mb-6`}>
          <h2 className={`${xbpneusClasses.cardTitle} text-xl mb-6`}>
            Informações Pessoais
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <p className="text-sm text-gray-600 mb-1">Nome Completo</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{motorista?.nome_completo}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Email</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{motorista?.email}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Telefone</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{motorista?.telefone}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">CPF</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{motorista?.cpf}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">CNH</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{motorista?.cnh}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Status</p>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                motorista?.ativo
                  ? xbpneusClasses.badgeSuccess
                  : xbpneusClasses.badgeWarning
              }`}>
                {motorista?.ativo ? 'Ativo' : 'Inativo'}
              </span>
            </div>
          </div>
        </div>

        {/* Informações de Endereço */}
        {motorista?.endereco && (
          <div className={`${xbpneusClasses.card} p-6 mb-6`}>
            <h2 className={`${xbpneusClasses.cardTitle} text-xl mb-6`}>
              Endereço
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <p className="text-sm text-gray-600 mb-1">Rua</p>
                <p className={`${xbpneusClasses.cardTitle}`}>{motorista?.endereco?.rua}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Número</p>
                <p className={`${xbpneusClasses.cardTitle}`}>{motorista?.endereco?.numero}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Cidade</p>
                <p className={`${xbpneusClasses.cardTitle}`}>{motorista?.endereco?.cidade}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Estado</p>
                <p className={`${xbpneusClasses.cardTitle}`}>{motorista?.endereco?.estado}</p>
              </div>
            </div>
          </div>
        )}

        {/* Informações de Veículos */}
        {motorista?.veiculos && motorista.veiculos.length > 0 && (
          <div className={`${xbpneusClasses.card} p-6`}>
            <h2 className={`${xbpneusClasses.cardTitle} text-xl mb-6`}>
              Veículos Associados
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {motorista.veiculos.map((veiculo) => (
                <div key={veiculo.id} className="p-4 border rounded-lg">
                  <p className="font-semibold">{veiculo.placa}</p>
                  <p className="text-sm text-gray-600">{veiculo.modelo}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MotoristasDetailPage;

