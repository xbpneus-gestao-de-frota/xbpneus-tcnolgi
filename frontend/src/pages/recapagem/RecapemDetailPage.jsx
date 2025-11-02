import React, { useState, useEffect } from 'react';
import { ArrowLeft, Edit, Trash2 } from 'lucide-react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { xbpneusClasses } from '../../styles/colors';

const RecapemDetailPage = () => {
  const { id } = useParams();
  const [recapagem, setRecapagem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRecapagem();
  }, [id]);

  const fetchRecapagem = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await axios.get(`/api/recapagem/${id}/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      setRecapagem(response.data);
    } catch (err) {
      console.error('Erro ao buscar recapagem:', err);
      setError(err.response?.data?.message || 'Erro ao carregar recapagem');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Tem certeza que deseja deletar esta recapagem?')) {
      try {
        const token = localStorage.getItem('access_token');
        await axios.delete(`/api/recapagem/${id}/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        window.location.href = '/recapagem';
      } catch (err) {
        console.error('Erro ao deletar recapagem:', err);
        setError(err.response?.data?.message || 'Erro ao deletar recapagem');
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-6 flex items-center justify-center">
        <p className="text-gray-600">Carregando recapagem...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto">
          <button
            onClick={() => window.location.href = '/recapagem'}
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
            onClick={() => window.location.href = '/recapagem'}
            className={`${xbpneusClasses.buttonSecondary} px-4 py-2 rounded-lg flex items-center gap-2 mb-4`}
          >
            <ArrowLeft size={16} />
            Voltar
          </button>
          <div className="flex justify-between items-start">
            <div>
              <h1 className={`${xbpneusClasses.cardTitle} text-3xl mb-2`}>
                {recapagem?.nome_empresa}
              </h1>
              <p className="text-gray-600">
                Detalhes da recapagem
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => window.location.href = `/recapagem/${id}/editar`}
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

        {/* Informações da Empresa */}
        <div className={`${xbpneusClasses.card} p-6`}>
          <h2 className={`${xbpneusClasses.cardTitle} text-xl mb-6`}>
            Informações da Empresa
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <p className="text-sm text-gray-600 mb-1">Nome da Empresa</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{recapagem?.nome_empresa}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">CNPJ</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{recapagem?.cnpj}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Email</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{recapagem?.email}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Telefone</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{recapagem?.telefone}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Cidade</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{recapagem?.cidade}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Estado</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{recapagem?.estado}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecapemDetailPage;

