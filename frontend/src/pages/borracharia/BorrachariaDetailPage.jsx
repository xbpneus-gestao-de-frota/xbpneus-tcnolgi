import React, { useState, useEffect } from 'react';
import { ArrowLeft, Edit, Trash2 } from 'lucide-react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { xbpneusClasses } from '../../styles/colors';

const BorrachariaDetailPage = () => {
  const { id } = useParams();
  const [borracharia, setBorracharia] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchBorracharia();
  }, [id]);

  const fetchBorracharia = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await axios.get(`/api/borracharia/${id}/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      setBorracharia(response.data);
    } catch (err) {
      console.error('Erro ao buscar borracharia:', err);
      setError(err.response?.data?.message || 'Erro ao carregar borracharia');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Tem certeza que deseja deletar esta borracharia?')) {
      try {
        const token = localStorage.getItem('access_token');
        await axios.delete(`/api/borracharia/${id}/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        window.location.href = '/borracharia';
      } catch (err) {
        console.error('Erro ao deletar borracharia:', err);
        setError(err.response?.data?.message || 'Erro ao deletar borracharia');
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-6 flex items-center justify-center">
        <p className="text-gray-600">Carregando borracharia...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto">
          <button
            onClick={() => window.location.href = '/borracharia'}
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
            onClick={() => window.location.href = '/borracharia'}
            className={`${xbpneusClasses.buttonSecondary} px-4 py-2 rounded-lg flex items-center gap-2 mb-4`}
          >
            <ArrowLeft size={16} />
            Voltar
          </button>
          <div className="flex justify-between items-start">
            <div>
              <h1 className={`${xbpneusClasses.cardTitle} text-3xl mb-2`}>
                {borracharia?.nome_empresa}
              </h1>
              <p className="text-gray-600">
                Detalhes da borracharia
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => window.location.href = `/borracharia/${id}/editar`}
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
        <div className={`${xbpneusClasses.card} p-6 mb-6`}>
          <h2 className={`${xbpneusClasses.cardTitle} text-xl mb-6`}>
            Informações da Empresa
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <p className="text-sm text-gray-600 mb-1">Nome da Empresa</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{borracharia?.nome_empresa}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">CNPJ</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{borracharia?.cnpj}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Email</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{borracharia?.email}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Telefone</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{borracharia?.telefone}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Cidade</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{borracharia?.cidade}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Estado</p>
              <p className={`${xbpneusClasses.cardTitle}`}>{borracharia?.estado}</p>
            </div>
          </div>
        </div>

        {/* Informações de Contato */}
        {borracharia?.contato_responsavel && (
          <div className={`${xbpneusClasses.card} p-6`}>
            <h2 className={`${xbpneusClasses.cardTitle} text-xl mb-6`}>
              Contato Responsável
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <p className="text-sm text-gray-600 mb-1">Nome</p>
                <p className={`${xbpneusClasses.cardTitle}`}>{borracharia?.contato_responsavel?.nome}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Email</p>
                <p className={`${xbpneusClasses.cardTitle}`}>{borracharia?.contato_responsavel?.email}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BorrachariaDetailPage;

