import React, { useState, useEffect } from 'react';
import { Settings, Plus, ToggleLeft, ToggleRight } from 'lucide-react';
import axios from 'axios';
import { xbpneusClasses, xbpneusColors } from '../../styles/colors';

const IntegrationsManagementPage = () => {
  const [integrations, setIntegrations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  useEffect(() => {
    fetchIntegrations();
  }, []);

  const fetchIntegrations = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await axios.get('/api/integrations/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      setIntegrations(response.data.results || response.data || []);
    } catch (err) {
      console.error('Erro ao buscar integrações:', err);
      setError(err.response?.data?.message || 'Erro ao carregar integrações');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleIntegration = async (integrationId) => {
    try {
      const token = localStorage.getItem('access_token');
      const integration = integrations.find(i => i.id === integrationId);
      
      const response = await axios.post(
        `/api/integrations/${integrationId}/toggle/`,
        { active: !integration.active },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      setSuccessMessage('Integração atualizada com sucesso!');
      setIntegrations(
        integrations.map((int) =>
          int.id === integrationId
            ? { ...int, active: !int.active }
            : int
        )
      );
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      console.error('Erro ao atualizar integração:', err);
      setError(err.response?.data?.message || 'Erro ao atualizar integração');
    }
  };

  const handleConfigureIntegration = async (integrationId) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get(
        `/api/integrations/${integrationId}/`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      // Abrir modal com dados da integração
      console.log('Dados da integração:', response.data);
      setSuccessMessage('Carregando configurações...');
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      console.error('Erro ao carregar configurações:', err);
      setError(err.response?.data?.message || 'Erro ao carregar configurações');
    }
  };

  const handleAddIntegration = () => {
    // Abrir modal ou navegar para página de adição de integração
    setSuccessMessage('Função de adicionar integração em desenvolvimento');
    setTimeout(() => setSuccessMessage(null), 3000);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Cabeçalho */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h1 className={`${xbpneusClasses.cardTitle} text-3xl mb-2`}>
                Gerenciamento de Integrações
              </h1>
              <p className="text-gray-600">
                Configure e gerencie integrações com outros sistemas
              </p>
            </div>
            <button
              onClick={handleAddIntegration}
              className={`${xbpneusClasses.buttonPrimary} px-6 py-3 rounded-lg flex items-center gap-2`}
            >
              <Plus size={20} />
              Adicionar Integração
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

        {/* Conteúdo */}
        {loading ? (
          <div className="text-center py-12">
            <p className="text-gray-600">Carregando integrações...</p>
          </div>
        ) : error && !successMessage ? (
          <div className="text-center py-12">
            <p className="text-red-600">{error}</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {integrations.map((integration) => (
              <div key={integration.id} className={xbpneusClasses.card + ' p-6'}>
                {/* Ícone e Título */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="text-3xl">{integration.icon}</div>
                    <div>
                      <h3 className={`${xbpneusClasses.cardTitle} text-lg`}>
                        {integration.name}
                      </h3>
                      <p className="text-sm text-gray-600">{integration.description}</p>
                    </div>
                  </div>
                </div>

                {/* Status */}
                <div className="mb-4">
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-600">Status:</span>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        integration.active
                          ? xbpneusClasses.badgeSuccess
                          : xbpneusClasses.badgeWarning
                      }`}
                    >
                      {integration.active ? 'Ativa' : 'Inativa'}
                    </span>
                  </div>
                </div>

                {/* Botões de Ação */}
                <div className="flex gap-2">
                  <button
                    onClick={() => handleConfigureIntegration(integration.id)}
                    className={`${xbpneusClasses.buttonPrimary} flex-1 px-4 py-2 rounded-lg flex items-center justify-center gap-2 text-sm`}
                  >
                    <Settings size={16} />
                    Configurar
                  </button>
                  <button
                    onClick={() => handleToggleIntegration(integration.id)}
                    className={`flex-1 px-4 py-2 rounded-lg flex items-center justify-center gap-2 text-sm ${
                      integration.active
                        ? 'bg-red-100 text-red-700 hover:bg-red-200'
                        : 'bg-green-100 text-green-700 hover:bg-green-200'
                    }`}
                  >
                    {integration.active ? (
                      <>
                        <ToggleRight size={16} />
                        Desativar
                      </>
                    ) : (
                      <>
                        <ToggleLeft size={16} />
                        Ativar
                      </>
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default IntegrationsManagementPage;

